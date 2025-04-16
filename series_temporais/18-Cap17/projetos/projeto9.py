# Projeto 9 - Modelagem do Crescimento de Agriculturas em Diferentes Condições Usando PySpark e LLM

# Imports
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, sum, col
from pyspark.sql import functions as F
from openai import OpenAI

# Inicializando sessão Spark
spark = SparkSession.builder.appName("Projeto9").getOrCreate()

# Caminho do arquivo CSV
csv_file_path = "/opt/spark/dados/dataset.csv"

# Define a chave da OpenAI
client = OpenAI(api_key = 'coloque-aqui-sua-api')

# Função para carregar os dados 
def dsa_carrega_dados(spark, file_path):
    dsa_dados = spark.read.csv(file_path, header = True)
    print(f"\nTotal de registros carregados: {dsa_dados.count()}\n")
    return dsa_dados

# Carrega os dados
df_spark = dsa_carrega_dados(spark, csv_file_path)

# Crescimento total acumulado por cultura
df_spark.groupBy("cultura").agg(sum("crescimento").alias("crescimento_acumulado")).show()

# Média de crescimento por tipo de solo
df_spark.groupBy("solo").agg(avg("crescimento").alias("media_crescimento")).show()

# Função para coletar estatísticas e preparar o prompt para o mês de julho
def dsa_prepara_dados_prompt(df):
    
    # Extrai o mês da coluna de data e filtra para o mês de julho
    df_julho = df.withColumn("mes", F.month("data")).filter(F.col("mes") == 7)
    
    # Calcula a média de temperatura, umidade e crescimento por cultura e tipo de solo para julho
    stats_df = df_julho.groupBy("cultura", "solo").agg(
        F.avg("temperatura").alias("media_temperatura"),
        F.avg("umidade").alias("media_umidade"),
        F.avg("crescimento").alias("media_crescimento")
    ).collect()
    
    # Formatando os dados coletados em uma string para o prompt
    dados_formatados = "Estatísticas de crescimento para o mês de Julho:\n"
    for row in stats_df:
        dados_formatados += (f"Cultura: {row['cultura']}, Solo: {row['solo']}, "
                             f"Média de Temperatura: {row['media_temperatura']:.2f}°C, "
                             f"Média de Umidade: {row['media_umidade']:.2f}%, "
                             f"Média de Crescimento: {row['media_crescimento']:.2f} cm/dia\n")
    
    return dados_formatados

# Extraindo e formatando dados para o prompt
dados_para_prompt = dsa_prepara_dados_prompt(df_spark)

# Função para gerar uma pergunta sobre os dados e obter insights do LLM
def dsa_analisa_dados_com_llm(texto):

    # Construindo o prompt com dados formatados e a pergunta
    prompt = f"""
    Você está analisando um conjunto de dados sobre o crescimento de diferentes culturas agrícolas (milho, soja, trigo).
    Cada registro inclui variáveis como temperatura, umidade, tipo de solo e crescimento diário.
    
    Dados resumidos para análise:
    {dados_para_prompt}
    
    Baseado nesses dados, responda a pergunta abaixo fornecendo sugestões:
    {texto}
    """
    
    # Envio para o modelo de linguagem
    response = client.chat.completions.create(
        model = "gpt-4o",
        messages = [
            {"role": "user", "content": prompt}
        ],
        temperature = 0.2
    )
    
    return response.choices[0].message.content.strip()

# Pergunta sobre os dados
pergunta = "Quais condições de temperatura e umidade são ideais para o crescimento do milho?"

# Obtém a resposta a partir do LLM
resposta = dsa_analisa_dados_com_llm(pergunta)
print("Resposta do LLM:", resposta)

# Fim



