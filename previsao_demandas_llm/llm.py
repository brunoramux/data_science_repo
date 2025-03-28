# https://ollama.com/
# Baixar o llama e instalar
# rodar o comando no terminal para iniciar o modelo
import csv
import psycopg2
from langchain_core.prompts import ChatPrompTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms.ollama import Ollama


llm = Ollama(model = "llama3")

output_parser = StrOutputParser()

def gera_insights():
  
  conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5342"
  )
  
  cursor = conn.cursor()
  
  query = """
    SELECT
      *
    FROM
      demandas  
  """
  
  cursor.execute(query)
  
  rows = cursor.fetchall()
  
  insights = []
  
  prompt = ChatPrompTemplate.from_message(
    [
      ("system", "Você pode me ajudar a prever a demanda de produtos?"),
      ("user", "question: {question}")
    ]
  )
  
  chain = prompt | llm | output_parser
  
  for row in rows:
    consulta = f""
    response = chain.invoke({'question': consulta})
    insights.append(response)
  
  conn.close()
  
  with open('projeto7-analise.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.write(file)
    writer.writerow(['Insight'])
    for insight in insights:
      writer.writerow([insight])
  
  return insights

insights = gera_insights()