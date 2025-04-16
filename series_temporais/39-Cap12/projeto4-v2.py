# Projeto 4 - Aplicação e Interpretação de Análise Estatística em Dados do Mercado de Ações
# Testes Estatísticos - Script 2

# Imports
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, mean, stddev, min, max
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf, q_stat
from arch.unitroot import PhillipsPerron
import statsmodels.api as sm
import yfinance as yf
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Criar sessão do Spark
spark = SparkSession.builder \
    .appName("Projeto4-V2") \
    .getOrCreate()

print("\nExecutando o Script 2\n")

# Baixar dados de ações da Microsoft para os últimos 10 anos usando yfinance
msft = yf.download('MSFT', start='2013-06-30', end='2023-06-30')
msft.reset_index(inplace=True)

# Converter DataFrame do Pandas para DataFrame do Spark
df = spark.createDataFrame(msft)

# Realizar análise estatística básica
summary = df.describe()

# Mostrar sumário estatístico
summary.show()

# Salvar sumário estatístico em CSV
summary.write.mode('overwrite').csv('dados/script2_sumario', header=True)

# Calcular estatísticas adicionais
stats_df = df.select(
    mean(col('Close')).alias('mean_close'),
    stddev(col('Close')).alias('stddev_close'),
    min(col('Close')).alias('min_close'),
    max(col('Close')).alias('max_close')
)

# Mostrar estatísticas adicionais
stats_df.show()

# Salvar estatísticas adicionais em CSV
stats_df.write.mode('overwrite').csv('dados/script2_stats', header=True)

# Coletar dados para aplicar testes estatísticos
close_prices = df.select('Close').rdd.flatMap(lambda x: x).collect()

# Teste de Dickey-Fuller Aumentado (ADF)
adf_test = adfuller(close_prices)
print(f"\nTeste ADF: Statistic={adf_test[0]}, p-value={adf_test[1]}, Critical Values={adf_test[4]}")

# Teste KPSS
kpss_test = kpss(close_prices)
print(f"\nTeste KPSS: Statistic={kpss_test[0]}, p-value={kpss_test[1]}, Critical Values={kpss_test[3]}")

# Teste de Phillips-Perron
pp_test = PhillipsPerron(close_prices)
pp_test_statistic = pp_test.stat
pp_test_pvalue = pp_test.pvalue
print(f"\nTeste Phillips-Perron: Statistic={pp_test_statistic}, p-value={pp_test_pvalue}")

# Teste de Ljung-Box
ljung_box_test = q_stat(acf(close_prices, fft=False, nlags=40), len(close_prices))
print(f"\nTeste Ljung-Box: Statistics={ljung_box_test[0]}, p-values={ljung_box_test[1]}")

# ACF e PACF
acf_vals = acf(close_prices, fft=False, nlags=40)
pacf_vals = pacf(close_prices, nlags=40)

# Salvar ACF e PACF em CSV
acf_df = pd.DataFrame({'Lag': np.arange(len(acf_vals)), 'ACF': acf_vals})
pacf_df = pd.DataFrame({'Lag': np.arange(len(pacf_vals)), 'PACF': pacf_vals})

acf_df.to_csv('dados/script2_acf.csv', index=False)
pacf_df.to_csv('dados/script2_pacf.csv', index=False)

print("\nScript 2 Concluído\n")

# Encerrar sessão do Spark
spark.stop()
