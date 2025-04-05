import streamlit as st
import pandas as pd
import requests
import os.path
import base64
import streamlit.components.v1 as components

# Configuração da página Streamlit - DEVE VIR PRIMEIRO
st.set_page_config(page_title="Assistente de Apostas Betnaldo", page_icon=":soccer:", layout="wide")

st.markdown(
    """
    <style>
    body {
        color: #FFFFFF;
        background-color: #0E1117;
        font-family: 'Poppins', sans-serif;
    }
    .stApp {
        background-color: #000000;
        font-family: 'Poppins', sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ADD8E6;
    }
    p, div {
        color: #FFFFFF;
    }
    .stTextInput > div > div > input {
        color: #000000;
        background-color: #FFFFFF;
    }
    .stButton > button {
        color: #FFFFFF;
        background-color: #1E293B;
        border-color: #1E293B;
    }
    .stButton > button:hover {
        background-color: #384A61;
        border-color: #384A61;
    }
    .stSidebar {
        background-color: #1E293B;
        color: #FFFFFF;
    }
    .stSidebar h3, .stSidebar p {
        color: #FFFFFF;
    }
    #betnaldo-image {
        transition: transform 0.5s ease-in-out !important;
    }
    #betnaldo-image:hover {
        transform: scale(1.05) !important;
    }
    .typing-animation {
        overflow: hidden;
        white-space: nowrap;
        border-right: .15em solid #98FB98; /* Cor do cursor */
        animation: typing 2s steps(40, end), blink-caret .75s step-end infinite;
    }

    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }

    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #98FB98; } /* Cor do cursor */
    }

    .response-container { /* Nova classe para a div que contém a resposta */
        word-wrap: break-word;
        overflow-x: auto; /* Rolagem horizontal se necessário */
        display: inline-block; /* Importante para o tamanho do contêiner */
        max-width: 100%; /* Garante que não ultrapasse o contêiner pai */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <link href='https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap' rel='stylesheet'>
    """, unsafe_allow_html=True)

# Barra lateral
with st.sidebar:
    caminho_imagem = r"C:\Users\Salsa\PycharmProjects\PythonProject2\betnaldo.gif"

    if os.path.exists(caminho_imagem):
        # Ler a imagem como bytes e codificar para base64
        with open(caminho_imagem, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()

        # Injetar a imagem como uma string base64
        components.html(
            f"""
            <img id="betnaldo-image" src="data:image/gif;base64,{encoded_string}" width="300">
            """,
            height=300,
        )
    else:
        st.error(f"Erro: Imagem não encontrada em: {caminho_arquivo}")

    st.markdown("### Sobre o Betnaldo")
    st.markdown("Seu guia virtual para o mundo das apostas esportivas.")
    st.markdown("Aqui você pode me perguntar dúvidas sobre as regras de um torneio ou partida\nDúvidas sobre a promoção do dia\nTermos usados em apostas e muito mais")
    st.markdown("---")
    st.markdown("Desenvolvido com Streamlit")

# Título principal no centro
st.title("⚽ Bem-vindo ao Assistente de Apostas Betnaldo! 🏆")

# Mensagem inicial do agente com um toque de estilo
st.markdown(f"<div style='background-color: #0E1117; padding: 10px; border-radius: 5px;'> <p style='color: #ADD8E6;' class='typing-animation'> Sou Betnaldo, seu assistente de apostas esportivas. <br> Posso te ajudar com informações e orientações sobre suas apostas. <br> Qual é a sua dúvida?</p> </div>", unsafe_allow_html=True)

# Caminho para a planilha
caminho_arquivo = r"C:\Users\Salsa\Desktop\resposta.xlsx"

try:
    df = pd.read_excel(caminho_arquivo)
    coluna_perguntas = df.columns[0]
    coluna_respostas = df.columns[1]
except FileNotFoundError:
    st.error(f"Erro: Arquivo não encontrado em: {caminho_arquivo}")
    df = None
except Exception as e:
    st.error(f"Ocorreu um erro ao ler a planilha: {e}")
    df = None

# Função para obter respostas do Ollama
def get_ollama_response(prompt, model="llama2", max_tokens=150):
    url = "http://localhost:11434/api/generate"
    data = {
        "prompt": prompt,
        "model": model,
        "stream": False,
        "options": {"max_tokens": max_tokens}
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        return f"Erro ao comunicar com o Ollama: {e}"

# Campo para o usuário digitar a pergunta
pergunta_usuario = st.text_input("Digite sua pergunta aqui:")

# Lógica para pesquisar e responder
if pergunta_usuario and df is not None:
    encontrou_resposta = False
    for index, row in df.iterrows():
        pergunta_planilha = str(row[coluna_perguntas]).lower()
        if pergunta_planilha in pergunta_usuario.lower():
            resposta = row[coluna_respostas]
            st.markdown(f"<div style='background-color: #1E293B; padding: 10px; border-radius: 5px;' class='response-container'> <p style='color: #98FB98;' class='typing-animation'><b>Betnaldo:</b> {resposta}</p> </div>", unsafe_allow_html=True)
            encontrou_resposta = True
            break

    if not encontrou_resposta:
        # Prompt para Ollama com instruções detalhadas em português (e limite de comprimento)
        prompt_ollama = f"""
        Você é um assistente virtual chamado Betnaldo, especializado em apostas esportivas.
        Responda a todas as perguntas de forma clara, concisa e em português do Brasil.
        Não use gírias, expressões informais ou emojis.
        Seja profissional e informativo.
        Limite suas respostas a aproximadamente 100 palavras.
        Responda à seguinte pergunta: {pergunta_usuario}
        """
        ollama_response = get_ollama_response(prompt_ollama, max_tokens=200)
        st.markdown(f"<div style='background-color: #1E293B; padding: 10px; border-radius: 5px;' class='response-container'> <p style='color: #FFD700;' class='typing-animation'><b>Betnaldo:</b> {ollama_response}</p> </div>", unsafe_allow_html=True)

# Podemos adicionar mais informações ou links úteis aqui no corpo principal
st.markdown("---")
st.markdown("#### Links Úteis")
st.markdown("- [Regulamentos de Apostas](https://www.example.com/regulamentos)") # Substitua pelo link real
st.markdown("- [Suporte ao Cliente](https://www.example.com/suporte)") # Substitua pelo link real