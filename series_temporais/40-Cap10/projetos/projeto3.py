# Projeto 3 - Otimização de Cadeias de Suprimentos com Modelagem de Séries Temporais

# Imports
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, acf, pacf
from pmdarima import auto_arima
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Inicializa a sessão Spark
spark = SparkSession.builder \
    .appName("Projeto 3") \
    .getOrCreate()

# Carrega os dados de séries temporais
df_dsa = spark.read.csv('/opt/spark/dados/dataset.csv', header = True, inferSchema = True)

print("\nSessão Spark Criada e Dados Carregados.")

# Seleciona colunas de interesse e converte para o formato de dataframe
time_series_data = df_dsa.select("data", col("demanda_insumos_kg").alias("value")).orderBy("data").toPandas()
time_series_data['data'] = pd.to_datetime(time_series_data['data'])
time_series_data.set_index("data", inplace = True)

# Decomposição da série temporal
resultado_decomp = seasonal_decompose(time_series_data, model = 'multiplicative', period = 7)

# No videobook do Capítulo 10 você encontra detalhes sobre a decomposição.

# Para uma série temporal diária (nosso caso), o valor de period deve ser escolhido com base na sazonalidade esperada nos dados. 
# Aqui estão alguns exemplos comuns de períodos para séries temporais diárias:

# Sazonalidade Semanal: Se você espera que a série tenha um padrão semanal (por exemplo, vendas que variam consistentemente de segunda a domingo), 
# o valor de period deve ser 7.

# Sazonalidade Mensal: Se você espera que a série tenha um padrão mensal, a escolha do período pode ser um pouco mais complexa 
# devido ao número variável de dias nos meses. Em média, um mês tem cerca de 30,44 dias, mas um valor comum para simplificação é usar 30.

# Sazonalidade Anual: Se você espera que a série tenha um padrão anual, o valor de period deve ser 365 (ou 366 para incluir anos bissextos).

# Salva o resultado da decomposição em disco
resultado_decomp.trend.to_csv('/opt/spark/dados/01-trend.csv')
resultado_decomp.seasonal.to_csv('/opt/spark/dados/02-seasonal.csv')
resultado_decomp.resid.to_csv('/opt/spark/dados/03-residual.csv')

print("\nDecomposição da Série Temporal Realizada com Sucesso.\n")

# Determina os melhores valores de ordem (hiperparâmetros p, d e q) do modelo ARIMA
# Veja a definição no videobook do Capítulo 10 do curso
modelo_auto_arima = auto_arima(time_series_data, seasonal = False, trace = True)
best_order = modelo_auto_arima.order

print("\nEstes São os Melhores Valores de order:")

print(best_order)

# Ajusta (treina) o modelo ARIMA com os melhores hiperparâmetros
modelo_dsa = ARIMA(time_series_data, order = best_order)
modelo_dsa_fit = modelo_dsa.fit()

# Previsões com o modelo para horizonte de 10 dias
forecast = modelo_dsa_fit.forecast(steps = 10)

# Converte forecast para uma série 
forecast_series = pd.Series(forecast, 
                            name = 'forecast', 
                            index = pd.date_range(start = time_series_data.index[-1] + pd.Timedelta(days = 1), periods = 10, freq = 'D'))

# Cria DataFrame de previsões com índice de datas e salva em disco
forecast_df = forecast_series.to_frame()
forecast_df.to_csv('/opt/spark/dados/04-forecast.csv')

print("\nModelo ARIMA Criado, Treinado e Previsões Salvas em Disco.")

# Exibe previsão
print("\nPrevisões Para Horizonte de 10 Dias:\n")
print(forecast_df)

# Veja a definição no videobook do Capítulo 10 do curso

# Salva os resíduos do modelo
residuals = pd.DataFrame(modelo_dsa_fit.resid)
residuals.to_csv('/opt/spark/dados/05-residuos.csv')

# Teste de Dickey-Fuller Aumentado
adf_test = adfuller(residuals)
print("\nEstatísticas do Modelo:\n")
print('ADF Statistic:', adf_test[0])
print('p-value:', adf_test[1])

# Veja a definição no videobook do Capítulo 10 do curso

# Função de Autocorrelação e Função de Autocorrelação Parcial
acf_values = acf(residuals)
pacf_values = pacf(residuals)

# Salva os valores de ACF e PACF em disco
pd.DataFrame(acf_values, columns = ['ACF']).to_csv('/opt/spark/dados/06-acf_values.csv')
pd.DataFrame(pacf_values, columns = ['PACF']).to_csv('/opt/spark/dados/07-pacf_values.csv')

# Os valores de ACF e PACF indicam que os resíduos do modelo ARIMA não apresentam autocorrelação significativa. 
# Isso é um bom sinal, pois sugere que o modelo ARIMA ajustado está capturando bem as estruturas temporais dos dados 
# e que os resíduos podem ser considerados como ruído branco (sem padrões ou dependências temporais remanescentes).

print("\nProcessamento Concluído com Sucesso.\n")

# Encerra sessão do Spark
spark.stop()


