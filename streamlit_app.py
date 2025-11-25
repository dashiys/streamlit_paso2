import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("🤖 Chatbot - paso 2 - con LangChain")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit.")

with st.sidebar:
    st.header("⚙️ Configuración del modelo")

    modelo = st.selectbox(
        "Modelo:",
        ["gemini-1.5-flash", "gemini-1.5-pro"]
    )

    temperatura = st.slider("Temperatura", 0.0, 1.0, 0.7)

    if st.button("Limpiar conversación"):
        st.session_state.mensajes = []

# Crear modelo con la configuración elegida
chat_model = ChatGoogleGenerativeAI(
    model=modelo,
    temperature=temperatura
)

# Inicializar historial
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Render historial
for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# Entrada de usuario
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)

    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    # Generar respuesta
    respuesta = chat_model.invoke(st.session_state.mensajes)

    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.mensajes.append(respuesta)


