# Projeto 8 - IA Para Detecção de Anomalias em Dados de Sensores IoT em Tempo Real
# Módulo de Deploy do Modelo

# Ajusta o nível de log do TensorFlow
import logging, os
logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Imports
import json
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, FloatType, StringType, TimestampType
from pyspark.ml.feature import VectorAssembler
from tensorflow.keras.models import load_model

# Inicializando sessão Spark
spark = SparkSession.builder.appName("Projeto8-StreamDeploy").getOrCreate()

# Schema para dados de sensores
schema = StructType([
    StructField("sensor_id", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("temperatura", FloatType(), True),
    StructField("umidade", FloatType(), True),
    StructField("pressao", FloatType(), True)
])

# Carregando o modelo LSTM salvo para detecção de anomalias
model = load_model("/opt/spark/modelos/modelo_dsa.keras")
print("\nModelo LSTM para detecção de anomalias carregado com sucesso.")

# Carregando os parâmetros de padronização
try:
    with open("/opt/spark/modelos/scaler_params.json", "r") as f:
        scaler_params = json.load(f)
        mean = np.array(scaler_params["mean"])
        std = np.array(scaler_params["std"])
    print("Parâmetros de padronização carregados com sucesso.\n")
except Exception as e:
    print(f"Erro ao carregar os parâmetros de padronização: {e}")
    exit(1)

# Função de detecção de anomalias 
def dsa_detecta_anomalias(batch_df, batch_id):

    # Converter para vetor numpy
    batch_np = np.array([row['features'].toArray() for row in batch_df.collect()])

    # Verificar se o lote está vazio
    if batch_np.size == 0:
        print(f"Batch {batch_id} está vazio. Nada para processar.")
        return

     # Caso tenha uma única amostra, transformar para 2D
    if batch_np.ndim == 1:
        batch_np = batch_np.reshape(1, -1)  

    # Aplica a padronização
    batch_np = (batch_np - mean) / std

    # Ajustar para o formato esperado pelo LSTM
    batch_np = batch_np.reshape(-1, 1, 3)  

    # Realizar a previsão com o modelo carregado
    predictions = model.predict(batch_np)

    # Calcular o erro de reconstrução
    threshold = 0.8  # Ajuste conforme necessário
    anomalies = []
    for i, pred in enumerate(predictions):
        error = np.mean(np.abs(pred - batch_np[i]))
        if error > threshold:
            anomalies.append((batch_df.collect()[i]['sensor_id'], error))
    
    # Exibir anomalias detectadas ou mensagem de ausência
    if anomalies:
        print(f"Anomalia detectada no batch {batch_id}: {anomalies}")
    else:
        print(f"Nenhuma anomalia detectada no batch {batch_id}.")

# Configuração do stream de dados usando socket
streaming_data = spark.readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# Transformando os dados de streaming e convertendo colunas para DoubleType
sensor_data = streaming_data \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("temperatura", col("temperatura").cast("double")) \
    .withColumn("umidade", col("umidade").cast("double")) \
    .withColumn("pressao", col("pressao").cast("double"))

# Preparação dos dados para o modelo
assembler = VectorAssembler(inputCols = ["temperatura", "umidade", "pressao"], outputCol = "features")
assembled_data = assembler.transform(sensor_data)

# Aplicação do modelo no stream
print("\nPronto Para Realizar Detecção de Anomalias em Tempo Real...\n")
query = assembled_data.writeStream \
    .foreachBatch(dsa_detecta_anomalias) \
    .start()

query.awaitTermination()

spark.stop()
