import streamlit as st

def authenticated_page():
    st.title("Bem-vindo à página autenticada!")
    st.write("Você foi autenticado com sucesso.")

if __name__ == "__main__":
    authenticated_page()
