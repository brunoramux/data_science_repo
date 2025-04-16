# Projeto Final - Deploy de Modelo PySpark e API Para Web App de Sistema de Recomendação em Tempo Real
# Módulo de Geração de Dados

# Importa as bibliotecas necessárias
import os            # Para manipulação do sistema de arquivos
import pandas as pd  # Para manipulação de dados
import numpy as np   # Para operações matemáticas e geração de números aleatórios
from datetime import datetime, timedelta  # Para manipulação de datas

# Define uma função para gerar uma amostra de dados de avaliação
def dsa_gera_amostra_dados(num_users=100, num_items=50):
    
    # Verifica se o diretório 'dados' existe; se não, cria o diretório
    if not os.path.exists('dados'):
        os.makedirs('dados')

    # Cria uma lista de IDs de usuários, de 1 até num_users
    user_ids = np.arange(1, num_users + 1)
    
    # Cria uma lista de IDs de itens, de 1 até num_items
    item_ids = np.arange(1, num_items + 1)

    # Inicializa uma lista para armazenar os dados de avaliações
    dados = []
    
    # Define o intervalo de datas
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range = (end_date - start_date).days

    # Itera sobre cada usuário
    for user_id in user_ids:

        # Seleciona aleatoriamente um conjunto de itens avaliados pelo usuário
        rated_items = np.random.choice(item_ids, size=np.random.randint(1, num_items), replace=False)
        
        # Itera sobre cada item avaliado pelo usuário
        for item_id in rated_items:

            # Gera uma avaliação aleatória entre 1 e 5, com duas casas decimais
            rating = round(np.random.uniform(1, 5), 2)

            # Gera uma data aleatória no intervalo definido
            random_date = start_date + timedelta(days=np.random.randint(0, date_range))

            # Adiciona o registro (date, user_id, item_id, rating) na lista de dados
            dados.append((random_date.strftime('%Y-%m-%d'), user_id, item_id, rating))

    # Cria um dataframe a partir da lista de dados
    df_dsa = pd.DataFrame(dados, columns=['date', 'user_id', 'item_id', 'rating'])
    
    # Salva o dataframe em um arquivo CSV no diretório 'dados'
    df_dsa.to_csv('dados/ratings.csv', index=False)
    
    # Imprime uma mensagem indicando que os dados foram gerados com sucesso
    print("Dados de exemplo gerados em 'dados/ratings.csv'.")

# Executa a função principal se o script for executado diretamente
if __name__ == "__main__":
    dsa_gera_amostra_dados()




