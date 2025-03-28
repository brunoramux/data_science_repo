import psycopg2
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/demandas')

def carrega_dados(csv_file, table_name, schema):
  try:
    df = pd.read_csv(csv_file)
    df.to_sql(table_name, engine, schema=schema, if_exists='append', index=False)
    print(f'Tabela {table_name} criada com sucesso!')
  except Exception as e:
    print(f'Erro ao criar a tabela {table_name}: {e}')