# Projeto Final - Deploy de Modelo PySpark e API Para Web App de Sistema de Recomendação em Tempo Real

## Descrição

Projeto que implementa um sistema de recomendação utilizando PySpark para treinamento do modelo, FastAPI para servir a API e Streamlit para a interface web.

## Estrutura

- **dados/**: Dados históricos.
- **modelos/**: Modelo treinado.
- **scripts/**: Scripts Python.
  - **01_dsa_gera_dados.py**: Gera dados de exemplo.
  - **02_dsa_treina_modelo_pyspark.py**: Treina o modelo de recomendação.
  - **03_dsa_api.py**: API para servir o modelo.
  - **04_dsa_app.py**: Aplicação web com Streamlit.
- **requirements.txt**: Dependências do projeto.

## Pré-requisitos

- Python 3.11 ou superior
- PySpark instalado

## Instalação

# Crie um ambiente virtual:

python -m venv dsavenv

# Ative o ambiente virtual:

# Windows:
dsavenv\Scripts\activate

# MacOS/Linux:
source dsavenv/bin/activate

# Execute as instruções abaixo conforme demonstrado nas aulas:

pip install --upgrade pip

pip install --upgrade cmake 

pip install -r requirements.txt

python scripts/01_dsa_gera_dados.py

python scripts/02_dsa_treina_modelo_pyspark.py

# Abra outro terminal ou prompt de comando, navegue até a pasta com os arquivos, ative o dsaenv e execute:

python scripts/03_dsa_api.py

# Abra outro terminal ou prompt de comando, navegue até a pasta com os arquivos, ative o dsaenv e execute:

streamlit run scripts/04_dsa_app.py

# Acesse a app via navegador e faça previsões em tempo real!







