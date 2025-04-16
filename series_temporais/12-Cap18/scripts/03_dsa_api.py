# Projeto Final - Deploy de Modelo PySpark e API Para Web App de Sistema de Recomendação em Tempo Real
# Módulo da API Para Servir o Modelo

# Importa as bibliotecas necessárias
from fastapi import FastAPI  # Para criar a API
from pyspark.sql import SparkSession  # Para manipulação de dados no Spark
from pyspark.ml.recommendation import ALSModel  # Para carregar o modelo ALS
import uvicorn  # Para executar a aplicação FastAPI

# Cria uma instância da aplicação FastAPI
app = FastAPI()

# Inicializa a SparkSession com configurações específicas para localhost
spark = SparkSession.builder \
    .appName("ServeRecommendationModel") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .config("spark.driver.host", "127.0.0.1") \
    .getOrCreate()

# Define o nível de log do Spark para suprimir mensagens de aviso
spark.sparkContext.setLogLevel("ERROR")

# Carrega o modelo ALS previamente treinado do diretório especificado
model = ALSModel.load("modelos/als_model")

# Define o endpoint da API para gerar recomendações
@app.get("/predict/")
def predict(user_id: int, num_recs: int = 5):
    """
    Endpoint para obter recomendações para um usuário específico.

    Args:
        user_id (int): ID do usuário para o qual as recomendações serão geradas.
        num_recs (int): Número de recomendações desejado (padrão: 5).

    Returns:
        dict: Contém o ID do usuário e uma lista de recomendações com 'item_id' e 'rating'.
    """
    
    # Cria um DataFrame Spark contendo apenas o ID do usuário fornecido
    users_df = spark.createDataFrame([(user_id,)], ["user_id"])

    # Utiliza o modelo ALS para obter as principais recomendações para o usuário
    user_recs = model.recommendForUserSubset(users_df, num_recs)

    # Extrai as recomendações do resultado do modelo
    recs = user_recs.collect()  # Converte os resultados para uma lista Python
    
    # Verifica se há recomendações disponíveis
    if recs:  

        # Obtém a lista de recomendações
        recommendations = recs[0]['recommendations']  
        
        # Formata as recomendações como uma lista de dicionários com 'item_id' e 'rating'
        recommendations = [{'item_id': row['item_id'], 'rating': row['rating']} for row in recommendations]
    
    else:

        # Retorna uma lista vazia se não houver recomendações
        recommendations = []  

    # Retorna o resultado como um dicionário JSON
    return {"user_id": user_id, "recommendations": recommendations}

# Executa a aplicação FastAPI se o script for executado diretamente
if __name__ == "__main__":

    # Define o host e a porta para a API
    uvicorn.run(app, host="0.0.0.0", port=8000)  



