# Projeto Final - Deploy de Modelo PySpark e API Para Web App de Sistema de Recomendação em Tempo Real
# Módulo de Treinamento do Modelo com PySpark

# Importa os módulos necessários para manipulação de arquivos e treinamento do modelo
import os  # Para verificar e manipular o sistema de arquivos
import shutil  # Para remover diretórios e arquivos
from pyspark.sql import SparkSession  # Para inicializar uma sessão do Spark
from pyspark.ml.recommendation import ALS  # Algoritmo ALS para recomendação
from pyspark.ml.evaluation import RegressionEvaluator  # Avaliação do modelo

# Define a função principal para treinar o modelo
def dsa_treina_modelo():
    
    # Inicializa uma sessão Spark com configurações para localhost
    spark = SparkSession.builder \
        .appName("DSAProjetoFinal") \
        .config("spark.driver.bindAddress", "127.0.0.1") \
        .config("spark.driver.host", "127.0.0.1") \
        .getOrCreate()

    # Define o nível de log do Spark para suprimir mensagens de aviso
    spark.sparkContext.setLogLevel("ERROR")

    # Carrega os dados de avaliações a partir de um arquivo CSV
    ratings = spark.read.csv('dados/ratings.csv', header=True, inferSchema=True)

    # Remove a coluna 'date' para garantir que ela não seja usada no modelo
    # Ou seja, vamos trabalhar sem considerar o tempo como parte da informação
    ratings = ratings.drop('date')

    # Divide os dados em conjuntos de treinamento (80%) e teste (20%)
    (training, test) = ratings.randomSplit([0.8, 0.2])

    # Configura o modelo ALS (Alternating Least Squares) com parâmetros específicos
    als = ALS(maxIter=10,  # Número máximo de iterações
              regParam=0.1,  # Parâmetro de regularização
              userCol="user_id",  # Coluna que representa os IDs de usuários
              itemCol="item_id",  # Coluna que representa os IDs de itens
              ratingCol="rating",  # Coluna que representa as avaliações
              coldStartStrategy="drop")  # Lida com valores ausentes

    # Treina o modelo ALS usando o conjunto de treinamento
    modelo_dsa = als.fit(training)

    # Faz previsões no conjunto de teste
    predictions = modelo_dsa.transform(test)

    # Inicializa um avaliador para calcular o erro médio quadrático (RMSE)
    evaluator = RegressionEvaluator(metricName="rmse",  # Métrica de avaliação
                                    labelCol="rating",  # Coluna real
                                    predictionCol="prediction")  # Coluna prevista
    
    # Avalia o modelo e calcula o RMSE
    rmse = evaluator.evaluate(predictions)
    
    # Exibe o RMSE do modelo treinado
    print(f"RMSE = {rmse}")

    # Verifica se o diretório para salvar modelos existe; se não, cria o diretório
    if not os.path.exists('modelos'):
        os.makedirs('modelos')

    # Define o caminho onde o modelo será salvo
    model_path = "modelos/als_model"

    # Remove o diretório existente do modelo, se já existir, para evitar conflitos
    if os.path.exists(model_path):
        shutil.rmtree(model_path)

    # Salva o modelo treinado no diretório especificado
    modelo_dsa.save(model_path)
    print(f"Modelo salvo em '{model_path}'.")

    # Encerra a sessão Spark
    spark.stop()

# Executa a função principal se o script for executado diretamente
if __name__ == "__main__":
    dsa_treina_modelo()




