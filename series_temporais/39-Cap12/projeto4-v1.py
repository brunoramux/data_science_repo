# Projeto 4 - Aplicação e Interpretação de Análise Estatística em Dados do Mercado de Ações
# Testes Estatísticos - Script 1

# Imports
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, mean, stddev, min, max
from scipy import stats
import yfinance as yf
import pandas as pd

# Criar sessão do Spark
spark = SparkSession.builder \
    .appName("Projeto4-V1") \
    .getOrCreate()

print("\nExecutando o Script 1\n")

# Baixar dados de ações da Microsoft para os últimos 10 anos usando yfinance
msft = yf.download('MSFT', start='2013-06-30', end='2023-06-30')
msft.reset_index(inplace=True)

# Converter DataFrame do Pandas para DataFrame do Spark
df_dsa = spark.createDataFrame(msft)

# Realizar análise estatística básica
summary = df_dsa.describe()

# Mostrar sumário estatístico
summary.show()

# Salvar sumário estatístico em CSV
summary.write.mode('overwrite').csv('dados/script1_sumario', header=True)

# Calcular estatísticas adicionais
stats_df = df_dsa.select(
    mean(col('Close')).alias('mean_close'),
    stddev(col('Close')).alias('stddev_close'),
    min(col('Close')).alias('min_close'),
    max(col('Close')).alias('max_close')
)

# Mostrar estatísticas adicionais
stats_df.show()

# Salvar estatísticas adicionais em CSV
stats_df.write.mode('overwrite').csv('dados/script1_stats', header=True)

# Coletar dados para aplicar testes estatísticos
# Vamos considerar a coluna de fechamento da cotação do preço de ação (Close)
close_prices = df_dsa.select('Close').rdd.flatMap(lambda x: x).collect()

# Teste de Normalidade (Shapiro-Wilk)
shapiro_test = stats.shapiro(close_prices)
print(f"\nTeste Shapiro-Wilk: W={shapiro_test[0]}, p-value={shapiro_test[1]}")

# Teste de Normalidade (Anderson-Darling)
ad_test = stats.anderson(close_prices)
print(f"\nTeste Anderson-Darling: Statistic={ad_test.statistic}, Critical Values={ad_test.critical_values}, Significance Level={ad_test.significance_level}")

# Teste de Homogeneidade de Variância (Levene)
# Assumindo que estamos comparando entre duas partes dos dados
split_index = len(close_prices) // 2
levene_test = stats.levene(close_prices[:split_index], close_prices[split_index:])
print(f"\nTeste de Levene: Statistic={levene_test.statistic}, p-value={levene_test.pvalue}")

print("\nScript 1 Concluído\n")

# Encerrar sessão do Spark
spark.stop()
