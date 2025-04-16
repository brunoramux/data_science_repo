# Projeto 2 - Análise e Visualização de Dados de Vendas ao Longo do Tempo com PySpark
# Script de Treino do Modelo

# Imports
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator 
from pyspark.ml import Pipeline

# Inicializar a Spark Session
spark = SparkSession.builder \
    .appName("Projeto2-Treino") \
    .getOrCreate()

# Carregar os dados
data_path = '/opt/spark/dados/dataset.csv'
df_dsa = spark.read.csv(data_path, header=True, inferSchema=True)

# Ajustar o tipo de dado
df_dsa = df_dsa.withColumn('Date', col('Date').cast('date'))

# Extrair ano e mês da coluna 'Date'
df_dsa = df_dsa.withColumn('Year', year(col('Date'))).withColumn('Month', month(col('Date')))

# Assembler para transformar as colunas em vetor de features dentro do pipeline
feature_assembler = VectorAssembler(inputCols=['Year', 'Month'], outputCol='Features')

# Modelo de regressão linear
modelo_lr = LinearRegression(featuresCol='Features', labelCol='Sales')

# Configurar o pipeline com assembler e modelo
pipeline_dsa = Pipeline(stages=[feature_assembler, modelo_lr])

# Separar dados para treino e teste
dados_treino, dados_teste = df_dsa.randomSplit([0.7, 0.3])

# Treinar o modelo
modelo_dsa = pipeline_dsa.fit(dados_treino)

# Fazer previsões
previsoes = modelo_dsa.transform(dados_teste)
previsoes.select('Date', 'Sales', 'prediction').show()

# Avaliar o modelo
evaluator = RegressionEvaluator(labelCol="Sales", predictionCol="prediction", metricName="rmse")
rmse = evaluator.evaluate(previsoes)
print("\nRoot Mean Squared Error (RMSE) nos Dados de Teste = %g" % rmse)
print("\n")

evaluator = RegressionEvaluator(labelCol="Sales", predictionCol="prediction", metricName="r2")
r2 = evaluator.evaluate(previsoes)
print("\nCoeficiente de Determinação (R2) nos Dados de Teste = %g" % r2)
print("\n")

# Salvar o modelo treinado
model_path = '/opt/spark/dados/modelo'
modelo_dsa.write().overwrite().save(model_path)

# Salvar as previsões em um arquivo CSV
previsoes.select('Date', 'Sales', 'prediction').write.csv('/opt/spark/dados/previsoesteste', header=True, mode="overwrite")

# Fechar a Spark session
spark.stop()

