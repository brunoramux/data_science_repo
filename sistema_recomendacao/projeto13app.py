# Projeto 13 - Sistema de Recomendação de Manutenção Preditiva Integrado com IoT Para Redução de Paradas Não Planejadas

# Imports
import joblib
import streamlit as st
import numpy as np
import pandas as pd

# Carregar o modelo e o scaler salvos
model_file = 'modelos/modelo_v1.pkl'
scaler_file = 'padronizadores/scaler_v1.pkl'
modelo_dsa = joblib.load(model_file)
scaler = joblib.load(scaler_file)

# Função para fazer a recomendação de manutenção
def dsa_recomenda_manutencao(novo_dado):

    # Definir os nomes das colunas conforme o scaler foi ajustado
    colunas = ['vibracao', 'temperatura', 'pressao', 'umidade', 'horas_trabalho']
    
    # Converter o novo dado para DataFrame com os nomes de colunas corretos
    novo_dado_df = pd.DataFrame([novo_dado], columns = colunas)
    
    # Aplicar o scaler ao novo dado
    novo_dado_scaled = scaler.transform(novo_dado_df)
    
    # Fazer a previsão
    predicao = modelo_dsa.predict(novo_dado_scaled)
    predicao_proba = modelo_dsa.predict_proba(novo_dado_scaled)[:, 1]

    # Retornar a classe e a probabilidade
    return predicao[0], predicao_proba[0]

# Configura a página da aplicação no Streamlit
st.set_page_config(page_title = "DSA Projeto 13", page_icon = ":100:", layout = "centered")

# Define o título da aplicação
st.title("Sistema de Recomendação de Manutenção Preventiva 🌐")

# Define uma legenda explicativa da aplicação
st.caption("Business Analytics e Machine Learning Para Projetos de Data Science")
st.caption("Data Science Academy - Projeto 13")

st.header("Insira os valores dos sensores:")
vibracao = st.number_input("Vibração", value=0.0)
temperatura = st.number_input("Temperatura (°C)", value=0.0)
pressao = st.number_input("Pressão (PSI)", value=0.0)
umidade = st.number_input("Umidade (%)", value=0.0)
horas_trabalho = st.number_input("Horas de Trabalho", value=0)

# Botão para realizar a previsão
if st.button("Verificar necessidade de manutenção"):
    novo_dado = [vibracao, temperatura, pressao, umidade, horas_trabalho]
    classe, probabilidade = dsa_recomenda_manutencao(novo_dado)
    
    # Mostrar os resultados
    st.write(f"Classe da Previsão: {'Realizar manutenção' if classe == 1 else 'Nenhuma manutenção necessária'}")
    st.write(f"Probabilidade de manutenção: {probabilidade:.2%}")
