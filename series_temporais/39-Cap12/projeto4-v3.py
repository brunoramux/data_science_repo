# Projeto 4 - Aplicação e Interpretação de Análise Estatística em Dados do Mercado de Ações
# Testes Estatísticos - Script 3

# Imports
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from statsmodels.tsa.stattools import grangercausalitytests
import yfinance as yf
import pandas as pd

# Criar sessão do Spark
spark = SparkSession.builder \
    .appName("Projeto4-V3") \
    .getOrCreate()

print("\nExecutando o Script 3\n")

# Baixar dados de ações da Microsoft e Apple para os últimos 10 anos usando yfinance
msft = yf.download('MSFT', start='2013-06-30', end='2023-06-30')
aapl = yf.download('AAPL', start='2013-06-30', end='2023-06-30')

# Manter apenas a coluna de fechamento ajustado
msft_close = msft[['Close']]
aapl_close = aapl[['Close']]

# Combinar os dois dataframes em um único dataframe
combined_df = pd.concat([msft_close, aapl_close], axis=1)
combined_df.columns = ['MSFT_Close', 'AAPL_Close']

# Remover NaNs
combined_df.dropna(inplace=True)

# Converter DataFrame do Pandas para DataFrame do Spark
df = spark.createDataFrame(combined_df)

# Coletar dados para aplicar o Teste de Causalidade de Granger
data = df.select('MSFT_Close', 'AAPL_Close').toPandas()

# Aplicar o Teste de Causalidade de Granger
# O parâmetro 'maxlag' define o número máximo de lags a serem testados
maxlag = 5
test_result = grangercausalitytests(data[['AAPL_Close', 'MSFT_Close']], maxlag = maxlag)

print("\nScript 3 Concluído\n")

# Encerrar sessão do Spark
spark.stop()
