# Projeto 7 - Machine Learning em Tempo Real Para Previsão de Tráfego de Um Web Site de E-Commerce
# Módulo de Deploy com Novos Dados Gerados em Tempo Real

# Imports
import joblib
import pandas as pd
import time  # Importar o módulo time para usar sleep
from gera_dados_realtime import dsa_gera_dados_tempo_real

# Definir as features (incluindo a lag)
features = ['dia_semana', 'eh_feriado', 'campanha_marketing_ativa', 'taxa_media_conversao', 'num_visitas_dia_anterior', 'lag_num_visitas']

# Carregar o modelo salvo
xgb_model = joblib.load('modelo_dsa_projeto7.pkl')

# Variável para armazenar a lag (tem que ser zero para a primeira previsão)
var_lag_num_visitas = 0  

# Função para gerar dados em tempo real e calcular a lag
def gerar_dados_realtime_com_lag(var_lag_num_visitas):
    
    # Gerar novos dados em tempo real
    real_time_data = dsa_gera_dados_tempo_real()

    # Adicionar a variável de lag (visitas do dia anterior)
    real_time_data['lag_num_visitas'] = var_lag_num_visitas

    return real_time_data

# Inicializar uma lista para armazenar as previsões
todas_previsoes = []

# Loop para gerar 7 previsões consecutivas
for i in range(7):

    # Gerar novos dados com lag
    real_time_data = gerar_dados_realtime_com_lag(var_lag_num_visitas)

    # Verificar se há dados para processar
    if not real_time_data.empty:
        
        # Preparar os dados para a previsão
        real_time_features = real_time_data[features]

        # Fazer a previsão
        predictions = xgb_model.predict(real_time_features)

        # Armazenar a previsão e as features utilizadas
        real_time_data['num_previsto_visitas'] = predictions.astype(int)
        todas_previsoes.append(real_time_data.copy())

        # Exibir os dados e a previsão atual
        print(f'\nPrevisão {i+1}:')
        print(f'Novos Dados de Entrada: {real_time_data[features].iloc[0].tolist()}')
        print(f'Previsão de Visitas: {real_time_data["num_previsto_visitas"].iloc[0]}\n')

        # Atualizar a lag para a próxima previsão
        var_lag_num_visitas = int(real_time_data['num_previsto_visitas'].iloc[0])

        # Pausar por 2 segundos antes da próxima previsão
        time.sleep(2)

# Após o loop, todas as previsões estão armazenadas na lista 'todas_previsoes'.
