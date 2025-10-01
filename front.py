import streamlit as st
from api.app.chat_backend import chat_with_rag

st.set_page_config(page_title="Sabores do Amazonas - Chat", page_icon="🍽️")
st.title("🍽️ Sabores do Amazonas - Assistente Virtual")

# Inicializa o histórico na sessão
if "history" not in st.session_state:
    st.session_state.history = [
        {
            "role": "system",
            "content": (
                "Você é um assistente especializado no restaurante Sabores do Amazonas. "
                "Responda perguntas sobre pratos, ingredientes, preços, horários, endereço e recomendações."
            ),
        }
    ]

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
    resposta = chat_with_rag(st.session_state.history.copy())

    # Adiciona resposta do backend
    st.session_state.history.append({"role": "assistant", "content": resposta})

    # Exibe resposta do backend
    with st.chat_message("assistant"):
        st.markdown(resposta)
