import streamlit as st
import pandas as pd

try:
    df = pd.read_excel("resposta.xlsx")
    st.success("Arquivo Excel lido com sucesso!")
    st.dataframe(df.head())  # Exibe as primeiras linhas
except FileNotFoundError:
    st.error("Arquivo resposta.xlsx não encontrado!")
except Exception as e:
    st.error(f"Ocorreu um erro: {e}")
