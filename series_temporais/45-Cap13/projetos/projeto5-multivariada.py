# Projeto 5 - Previsão da Demanda Mensal de Energia Elétrica em Indústria de Alimentos
# Trabalhando com Série Multivariada

# Imports
import pmdarima as pm
import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Iniciar a Spark session
spark = SparkSession.builder \
    .appName("Projeto 5 - Série Multivariada") \
    .getOrCreate()

# Caminho do arquivo CSV
csv_file_path = "/opt/spark/dados/dataset2.csv"

# Lê o arquivo CSV usando PySpark
df = spark.read.csv(csv_file_path, header = True, inferSchema = True)
df = df.withColumn("Data", to_date(df.Data))
df.show()

# Converte Spark DataFrame para Pandas DataFrame
pdf = df.toPandas()
pdf.set_index('Data', inplace = True)

# Separa a variável exógena
exog = pdf[['Temperatura']]

# Dividindo os dados em treino e teste (80% treino, 20% teste)
train_size = int(len(pdf) * 0.8)
dsa_treino, dsa_teste = pdf.iloc[:train_size], pdf.iloc[train_size:]
exog_train, exog_test = exog.iloc[:train_size], exog.iloc[train_size:]

# Otimização dos hiperparâmetros usando Auto ARIMA com variável exógena nos dados de treino
auto_modelo_dsa = pm.auto_arima(dsa_treino['ConsumoEnergia'], 
                                exogenous = exog_train,
                                seasonal = True, 
                                m = 12, 
                                start_p = 0, 
                                start_d = 0, 
                                start_q = 0,
                                max_p = 3, 
                                max_d = 3, 
                                max_q = 3, 
                                start_P = 0, 
                                start_D = 0, 
                                start_Q = 0,
                                max_P = 3, 
                                max_D = 3,
                                max_Q = 3,
                                max_order = 10,
                                information_criterion = 'aic',
                                trace = True, 
                                stepwise = False,
                                error_action = 'ignore')

# Mostra o melhor conjunto de parâmetros
print(auto_modelo_dsa.summary())

# Previsões usando os dados históricos (in-sample)
previsoes_treino = auto_modelo_dsa.predict_in_sample(exogenous = exog_train)

# Calcula o MAE e o MSE entre as previsões históricas e os valores reais
mae_train = mean_absolute_error(dsa_treino['ConsumoEnergia'], previsoes_treino)
mse_train = mean_squared_error(dsa_treino['ConsumoEnergia'], previsoes_treino)

print(f'Mean Absolute Error (MAE) com dados de treino: {mae_train}')
print(f'Mean Squared Error (MSE) com dados de treino: {mse_train}')

# Previsões usando os dados de teste (out-of-sample)
previsoes_teste = auto_modelo_dsa.predict(n_periods = len(dsa_teste), exogenous = exog_test)

# Calcula o MAE e o MSE entre as previsões de teste e os valores reais de teste
mae_test = mean_absolute_error(dsa_teste['ConsumoEnergia'], previsoes_teste)
mse_test = mean_squared_error(dsa_teste['ConsumoEnergia'], previsoes_teste)

print(f'Mean Absolute Error (MAE) com dados de teste: {mae_test}')
print(f'Mean Squared Error (MSE) com dados de teste: {mse_test}')

# Reajustando o modelo com todos os dados para preparar para previsão futura
auto_modelo_dsa.fit(pdf['ConsumoEnergia'], exogenous = exog)

# Simulação de temperatura futura para os próximos 12 meses (2025)
future_exog = np.random.normal(loc = 20, scale = 5, size = 12).reshape(-1, 1)  

# Gerando previsões para os próximos 12 meses de 2025
pred_forecast = auto_modelo_dsa.predict(n_periods = 12, exogenous = future_exog, return_conf_int = True)

# Gerando datas para 2025
future_dates_2025 = pd.date_range(start="2025-01-01", periods = 12, freq = 'MS')

# Criando uma série com as previsões e ajustando os índices para 2025
previsoes_2025 = pd.Series(pred_forecast[0], index = future_dates_2025)
intervalos_conf_2025 = pd.DataFrame(pred_forecast[1], index = future_dates_2025, columns = ['limite_inferior', 'limite_superior'])

print(f"Previsões para 2025:\n{previsoes_2025}")  # Previsões
print(f"Intervalos de confiança para as previsões:\n{intervalos_conf_2025}")  # Intervalos de confiança
