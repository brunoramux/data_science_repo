# Projeto 7 - Machine Learning em Tempo Real Para Previsão de Tráfego de Um Web Site de E-Commerce
# Módulo de Geração de Dados em Tempo Real

# Imports
import pandas as pd
import numpy as np

# Função
def dsa_gera_dados_tempo_real(num_samples = 1):
    
    # Novos dados
    dsa_novos_dados = pd.DataFrame({
        'dia_semana': np.random.choice(range(7), size = num_samples),
        'eh_feriado': np.random.choice([0, 1], size = num_samples),
        'campanha_marketing_ativa': np.random.choice([0, 1], size = num_samples),
        'taxa_media_conversao': np.random.uniform(0, 50, size = num_samples),
        'num_visitas_dia_anterior': np.random.poisson(100, size = num_samples),
    })
    
    return dsa_novos_dados
