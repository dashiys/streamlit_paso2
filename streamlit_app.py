import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# ------- CONFIG GENERAL -------
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖", layout="wide")

# ------- MENÚ DERECHO --------
with st.sidebar:
    st.header("⚙️ Configuración del modelo")

    modelo = st.selectbox(
        "Modelo:",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"],
        index=0
    )

    temperatura = st.slider(
        "Temperatura",
        min_value=0.0,
        max_value=1.0,
        step=0.01,
        value=0.7
    )

    if st.button("🧹 Limpiar conversación"):
        st.session_state.mensajes = []
        st.rerun()

# ------- TÍTULO DEL CHAT -------
st.title("🤖 Chatbot - paso 2 - con LangChain")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit.")

# ------- MODELO DINÁMICO -------
chat_model = ChatGoogleGenerativeAI(
    model=modelo,
    temperature=temperatura
)

# ------- HISTORIAL DE MENSAJES -------
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Renderizar historial
for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# ------- INPUT DEL USUARIO -------
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)

    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    respuesta = chat_model.invoke(st.session_state.mensajes)

    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.mensajes.append(respuesta)


