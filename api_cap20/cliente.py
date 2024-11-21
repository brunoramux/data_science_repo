# Projeto 10 - Construindo API Para Deploy do Modelo de Deep Learning
# Cliente

# Imports
import requests
import json

# URL da API
url = 'http://127.0.0.1:5000/predict'

# Dados a serem enviados como JSON
dados_dsa = [
    {
        "indice_vegetacao": 354, 
        "capacidade_solo": 684, 
        "concentracao_co2": 3736.3, 
        "nivel_nutrientes": 914.09, 
        "indice_fertilizantes": 849.78, 
        "profundidade_raiz": 412.37, 
        "radiacao_solar": 889, 
        "precipitacao": 49.81, 
        "estagio_crescimento": 154.92254, 
        "historico_rendimento": 245.3
    }
]

# Headers específicos para definir o tipo de conteúdo como JSON
headers = {'Content-Type': 'application/json'}

# Faz a requisição POST
response = requests.post(url, headers = headers, data = json.dumps(dados_dsa))

# Verifica se a requisição foi bem sucedida
if response.status_code == 200:
    print("\nResposta da API:", response.json())
    print("\n")
else:
    print("Erro na requisição:", response.status_code, response.text)
