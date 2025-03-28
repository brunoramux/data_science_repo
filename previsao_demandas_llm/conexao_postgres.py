import psycopg2

# Comando para executar um script SQL
# Parâmetro: filename - nome do arquivo contendo o script SQL
# Retorno: None
# Necessario criar o servidor de banco de dados no Docker
# docker run --name some-postgres -e POSTGRES_PASSWORD=dsapassword -p 5432:5432 -d postgres
# docker exec -it some-postgres bash
def script_execute(filename):
  conn = psycopg2.connect(
    dbname="postgres",
    user="dsa",
    password="dsapassword",
    host="localhost",
    port="5432"
  )
  
  cur = conn.cursor()
  
  with open(filename, 'r') as file:
    sql_script = file.read()
  
  try:
    cur.execute(sql_script)
    conn.commit()
  except Exception as e:
    conn.rollback()
    print(e)
  finally:
    cur.close()
    conn.close
