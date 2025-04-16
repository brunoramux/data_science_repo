# Projeto 12 - Blockchain Analytics Para Criptoativos com Machine Learning

# Imports necessários para o projeto
import torch
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from transformers import BertTokenizer, BertForSequenceClassification

# Carrega o modelo treinado para classificação de sentimento
modelo_dsa_final = BertForSequenceClassification.from_pretrained('./dsa_modelo_final')

# Carrega o tokenizador correspondente ao modelo treinado
tokenizador = BertTokenizer.from_pretrained('./dsa_modelo_final')

# Definição das classes de sentimento
sentiment_labels = ['Negativo', 'Neutro', 'Positivo']

# Função para analisar o sentimento de um texto usando o modelo carregado
def dsa_analisa_sentimento(text):

    # Tokeniza o texto de entrada
    inputs = tokenizador(text, return_tensors = 'pt', padding = True, truncation = True, max_length = 512)
    
    # Realiza a inferência com o modelo desativando o cálculo do gradiente
    with torch.no_grad():
        outputs = modelo_dsa_final(**inputs)
    
    # Obtém os logits da saída do modelo
    logits = outputs.logits
    
    # Calcula as probabilidades para cada classe de sentimento
    probabilities = torch.nn.functional.softmax(logits, dim = 1)
    
    # Identifica a classe prevista com maior probabilidade
    predicted_class = np.argmax(probabilities.numpy(), axis=1)[0]
    
    # Confiança associada à predição da classe
    confidence = probabilities[0][predicted_class].item()
    
    # Retorna o sentimento previsto, a confiança e as probabilidades
    return sentiment_labels[predicted_class], confidence, probabilities.numpy()

# Inicializa o histórico de análises de sentimento na sessão do Streamlit
if "history" not in st.session_state:
    st.session_state["history"] = []

# Configuração da página do Streamlit
st.set_page_config(page_title="DSA Projeto 12", page_icon=":100:", layout="centered")
st.header("Projeto 12 - Blockchain Analytics Para Criptoativos com Machine Learning")
st.subheader("₿ Análise de Sentimento de Blockchain e Criptoativos ₿")
st.write("Tomando decisões de investimento com base no sentimento do mercado.")

# Área de texto para o usuário digitar a entrada para análise de sentimento
user_input = st.text_area("Digite o texto para analisar o sentimento:")

# Executa a análise de sentimento ao clicar no botão
if st.button("Analisar Sentimento"):
    
    # Verifica se o texto não está vazio
    if user_input.strip():

        # Realiza a análise de sentimento e armazena o resultado
        sentiment, confidence, probabilities = dsa_analisa_sentimento(user_input)
        st.session_state["history"].append((user_input, sentiment, confidence))

        # Exibe o resultado do sentimento e a confiança
        st.write(f"Sentimento: {sentiment}")
        st.write(f"Confiança: {confidence:.2f}")

        # Cria e exibe um gráfico de gauge para a confiança
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = confidence,
            title = {'text': f"Sentimento: {sentiment}", 'font': {'size': 22}},
            gauge = {
                'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "black"},
                'steps': [
                    {'range': [0, 0.1], 'color': "rgba(255,1,1,1)"},
                    {'range': [0.1, 0.2], 'color': "rgba(255,84,0,1)"},
                    {'range': [0.2, 0.3], 'color': "rgba(255,167,0,1)"},
                    {'range': [0.3, 0.4], 'color': "rgba(255,214,0,1)"},
                    {'range': [0.4, 0.5], 'color': "rgba(255,214,0,1)"},
                    {'range': [0.5, 0.6], 'color': "rgba(241,255,1,1)"},
                    {'range': [0.6, 0.7], 'color': "rgba(198,255,0,1)"},
                    {'range': [0.7, 0.8], 'color': "rgba(155,255,0,1)"},
                    {'range': [0.8, 0.9], 'color': "rgba(9,255,0,1)"},
                    {'range': [0.9, 1], 'color': "rgba(9,255,0,1)"}],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': confidence}}))

        st.plotly_chart(fig)

        # Cria e exibe um gráfico de barras com a distribuição de probabilidades de sentimento
        fig_bar = go.Figure([go.Bar(x = sentiment_labels, y = probabilities[0])])
        fig_bar.update_layout(title = "Distribuição de Probabilidades de Sentimento", 
                              xaxis_title = "Sentimento", 
                              yaxis_title = "Probabilidade")
        
        st.plotly_chart(fig_bar)

        # Gera e exibe uma nuvem de palavras a partir do texto de entrada
        wordcloud = WordCloud(background_color = "white").generate(user_input)
        plt.figure(figsize = (8, 8))
        plt.imshow(wordcloud, interpolation = "bilinear")
        plt.axis("off")
        st.pyplot(plt)

        # Exibe o histórico de análises de sentimento
        st.subheader("Histórico de Análises")
        history_df = pd.DataFrame(st.session_state["history"], columns = ["Texto", "Sentimento", "Confiança"])
        st.write(history_df)

    else:
        st.write("Por favor, digite o texto para analisar.")


# Exemplos de texto para testar a app:

# A tecnologia blockchain está sendo adotada em diferentes indústrias
# A mineração de criptomoedas consome muita energia elétrica
# Investidores de longo prazo estão otimistas com o futuro do Bitcoin

