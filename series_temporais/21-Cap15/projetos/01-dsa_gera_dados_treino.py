# Projeto 7 - Machine Learning em Tempo Real Para Previsão de Tráfego de Um Web Site de E-Commerce
# Módulo de Geração de Dados Históricos

# Imports
import pandas as pd
import numpy as np

# Parâmetros para gerar dados de exemplo
np.random.seed(42)
data_size = 1000

# Cria um DataFrame de exemplo com dados de tráfego de web site de e-commerce
df_dsa = pd.DataFrame({
    'dia_semana': np.random.choice(range(7), size = data_size),              # Dia da semana (0=domingo, 6=sábado)
    'eh_feriado': np.random.choice([0, 1], size = data_size),                # Feriado ou não
    'campanha_marketing_ativa': np.random.choice([0, 1], size = data_size),  # Campanha de marketing ativa ou não
    'taxa_media_conversao': np.random.uniform(0, 50, size = data_size),      # Taxa média de conversão em %
    'num_visitas_dia_anterior': np.random.poisson(100, size = data_size),    # Visitas no dia anterior
    'num_visitas': np.random.poisson(120, size = data_size)                  # Número de visitas (variável dependente)
})

# Salvar o dataset para análise
df_dsa.to_csv('/opt/spark/dados/dados_trafego_site.csv', index = False)