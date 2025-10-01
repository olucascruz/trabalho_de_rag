import streamlit as st
import requests

st.set_page_config(page_title="Sabores do Amazonas - Chat", page_icon="🍽️")
st.title("🍽️ Sabores do Amazonas - Assistente Virtual")


if "history" not in st.session_state:
    st.session_state.history = []

# Exibir mensagens do histórico
for msg in st.session_state.history:
    with st.chat_message(msg["role"] if msg["role"] != "system" else "assistant"):
        st.markdown(msg["content"])

# Entrada do usuário
user_input = st.chat_input("Digite sua pergunta sobre o restaurante...")
if user_input:
    # Adiciona mensagem do usuário
    st.session_state.history.append({"role": "user", "content": user_input})

    # Exibe mensagem do usuário
    with st.chat_message("user"):
        st.markdown(user_input)

    # Chama o backend para obter resposta real
    response = requests.post(url="http://127.0.0.1:8000/prompt/", json={"prompt": user_input})
    resposta = response.json()["message"]

    # Adiciona resposta do backend
    st.session_state.history.append({"role": "assistant", "content": resposta})

    # Exibe resposta do backend
    with st.chat_message("assistant"):
        st.markdown(resposta)
