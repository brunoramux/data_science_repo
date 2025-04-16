# Projeto 7 - Machine Learning em Tempo Real Para Previsão de Tráfego de Um Web Site de E-Commerce
# Módulo de Treinamento e Avaliação do Modelo

# Imports
import joblib
import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Inicia uma sessão Spark
spark = SparkSession.builder \
    .appName("Projeto7") \
    .getOrCreate()

# Carrega o dataset
df = pd.read_csv('/opt/spark/dados/dados_trafego_site.csv')

# Engenharia de Atributos - ATENÇÃO:

# num_visitas_dia_anterior, num_visitas
# 100, 112
# 132, 145
# 118, 127

# num_visitas_dia_anterior, num_visitas, lag_num_visitas
# 100, 112, NA (esse registro será removido com o dropna)
# 132, 145, 112
# 118, 127, 145

# Cria a lag de 'num_visitas' (defasagem)
df['lag_num_visitas'] = df['num_visitas'].shift(1)

# Remove as primeiras linhas que contêm NaN devido à lag
df = df.dropna()

# Converte para DataFrame do PySpark
spark_df = spark.createDataFrame(df)

# Atualiza a lista de features para incluir a lag de 'num_visitas'
features = ['dia_semana', 'eh_feriado', 'campanha_marketing_ativa', 'taxa_media_conversao', 'num_visitas_dia_anterior', 'lag_num_visitas']

# Cria o vector assembler
assembler = VectorAssembler(inputCols = features, outputCol = 'features')

# Aplica o VectorAssembler para transformar as features
dataset = assembler.transform(spark_df)

# Seleciona a coluna de features e a coluna target ('num_visitas')
dataset = dataset.select('features', 'num_visitas')

# Converte para Pandas para uso no XGBoost
pandas_df = dataset.toPandas()

# Separa X e y
X = np.array(pandas_df['features'].tolist())
y = pandas_df['num_visitas']

# Divide os dados em treinamento e teste
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size = 0.2, random_state = 42)

# No caso do XGBoost, a padronização dos dados (normalização ou escalonamento) não é obrigatória para o modelo em si, 
# pois o algoritmo XGBoost lida bem com valores não padronizados. Isso se deve ao fato de que ele é baseado em árvores de decisão e essas, em geral, 
# não são sensíveis à escala dos dados, já que as árvores separam os dados por meio de limiares.

# Cria o modelo XGBoost
xgb_model = XGBRegressor(objective = 'reg:squarederror')

# Treina o modelo
xgb_model.fit(X_treino, y_treino)

# Faz as previsões
previsoes = xgb_model.predict(X_teste)

# Avalia o modelo
mse = mean_squared_error(y_teste, previsoes)
rmse = np.sqrt(mse)

# Exibe o RMSE
print(f'RMSE do Modelo: {rmse}')

# Salva o modelo treinado em disco
joblib.dump(xgb_model, 'modelo_dsa_projeto7.pkl')

# Encerra a sessão Spark
spark.stop()




