# Projeto Final - Deploy de Modelo PySpark e API Para Web App de Sistema de Recomendação em Tempo Real
# Módulo da App Para Consumir a API do Modelo

# Imports
import streamlit as st
import requests

# Configurações da página da aplicação
st.set_page_config(
    page_title="Sistema de Recomendação",
    page_icon="🎯",
    layout="wide"
)

# Barra lateral com título e instruções
st.sidebar.title("Sistema de Recomendação")
st.sidebar.markdown("""
Este sistema permite gerar recomendações personalizadas para usuários com base em dados históricos.
    
### Instruções:
1. Insira o **ID do usuário** no campo fornecido.
2. Selecione o número de recomendações desejado usando o controle deslizante.
3. Clique no botão **Obter Recomendações** para visualizar as sugestões.
""")

# Título principal da página
st.title("🎯 Sistema de Recomendação em Tempo Real")

# Entrada de dados no painel principal
st.subheader("Insira os detalhes para obter recomendações:")
user_id = st.number_input("ID do usuário:", min_value=1, step=1, help="Insira o identificador único do usuário.")
num_recs = st.slider("Número de recomendações:", min_value=1, max_value=20, value=5, help="Escolha quantas recomendações deseja obter.")

# Botão para obter recomendações
if st.button("Obter Recomendações"):

    # Configuração dos parâmetros para a chamada à API
    params = {'user_id': user_id, 'num_recs': num_recs}
    
    try:
        # Chamada à API para obter recomendações
        response = requests.get("http://localhost:8000/predict/", params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Exibe uma mensagem de erro em caso de falha na conexão
        st.error(f"Erro ao conectar com a API: {e}")
    else:
        # Processa a resposta da API
        data = response.json()
        if data['recommendations']:
            st.success(f"Recomendações para o usuário {data['user_id']}:")
            # Exibe as recomendações em formato de tabela
            recommendations = data['recommendations']
            st.table(recommendations)
        else:
            # Mensagem caso não haja recomendações para o usuário
            st.warning(f"Nenhuma recomendação encontrada para o usuário {data['user_id']}.")

# Rodapé da aplicação
st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido como parte do Projeto Final.")
st.sidebar.markdown("© Data Science Academy.")

