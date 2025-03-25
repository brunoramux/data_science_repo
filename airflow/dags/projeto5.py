# Projeto 5 - Criando Workflow Para Automatizar o Pipeline de Projetos de Data Science com Airflow

# Imports
import os
import requests
import sqlite3
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Definição dos argumentos para a DAG
default_args = {
    "owner": "Data Science Academy",
    "depends_on_past": False,
    "start_date": datetime(2024, 5, 3),
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

# Criação da DAG com o intervalo de agendamento especificado
dsa_dag = DAG(
    "projeto5",
    default_args=default_args,
    schedule_interval="* * * * *",  # Este agendamento deve ser ajustado conforme necessário
    catchup=False
)

# No formato de cron (cron expression), "* * * * *" significa que a DAG será executada a cada minuto. 

# Cada asterisco representa:

# Primeiro *: Minuto (0-59)
# Segundo *: Hora (0-23)
# Terceiro *: Dia do mês (1-31)
# Quarto *: Mês (1-12)
# Quinto *: Dia da semana (0-6, onde 0 é Domingo)

# Função para extrair dados da API
def dsa_extrai_dados():

    URL_BASE = "https://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "7b576667a43852336183990f6f1d6d14"
    CIDADES = ["Indaiatuba", "Blumenau", "Palmas", "Joinville", "Santos", "Curitiba", "Fortaleza", "Manaus", "Betim", "Juazeiro"]
    
    dados_cidades = []

    for cidade in CIDADES:
        url = f"{URL_BASE}q={cidade}&appid={API_KEY}"
        response = requests.get(url).json()
        dados_cidades.append(response)
    
    return dados_cidades

# Função para transformar os dados extraídos
def dsa_transforma_dados(dados_cidades):
    
    dados_transformados = []
    
    for response in dados_cidades:
        dsa_dados_tempo = {
            "city": response['name'],
            "date": datetime.utcfromtimestamp(response['dt']).strftime('%Y-%m-%d'),
            "temperature": round(response['main']['temp'] - 273.15, 2),
            "weather": response['weather'][0]['description']
        }

        dados_transformados.append(dsa_dados_tempo)
    
    return dados_transformados

# Função para carregar os dados transformados
def dsa_carrega_dados(dados_transformados):
    
    conn = sqlite3.connect('/opt/airflow/dags/dsa_projeto5.db')
    
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dsa_previsao_tempo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            date TEXT,
            temperature REAL,
            weather TEXT
        )
    ''')
    
    for dados in dados_transformados:
        
        cursor.execute('''
            INSERT INTO dsa_previsao_tempo (city, date, temperature, weather) 
            VALUES (?, ?, ?, ?)
        ''', (dados['city'], dados['date'], dados['temperature'], dados['weather']))
    
    conn.commit()
    conn.close()

# Define a tarefa para extrair dados
dsa_tarefa_extrai_dados = PythonOperator(
    task_id='dsa_extrai_dados',
    python_callable=dsa_extrai_dados,
    dag=dsa_dag
)

# Define a tarefa para transformar dados
dsa_tarefa_transforma_dados = PythonOperator(
    task_id='dsa_transforma_dados',
    python_callable=dsa_transforma_dados,
    op_args=[dsa_tarefa_extrai_dados.output],
    dag=dsa_dag
)

# Define a tarefa para carregar dados
dsa_tarefa_carrega_dados = PythonOperator(
    task_id='dsa_carrega_dados',
    python_callable=dsa_carrega_dados,
    op_args=[dsa_tarefa_transforma_dados.output],
    dag=dsa_dag
)

# Define a sequência das tarefas
dsa_tarefa_extrai_dados >> dsa_tarefa_transforma_dados >> dsa_tarefa_carrega_dados
