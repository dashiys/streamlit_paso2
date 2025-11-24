import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# -----------------------------
# Configuración inicial
# -----------------------------
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("🤖 Chatbot - paso 2 - con LangChain")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit.")

# -----------------------------
# SIDEBAR (Ejercicio pedido)
# -----------------------------
st.sidebar.title("⚙️ Configuración del modelo")

# Selector de modelo
modelo_seleccionado = st.sidebar.selectbox(
    "Modelo:",
    ["gemini-2.0-flash", "gemini-pro", "gemini-1.5-flash"],
    index=0
)

# Slider para temperatura
temperatura = st.sidebar.slider(
    "Temperatura",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1
)

# Botón para limpiar la conversación
if st.sidebar.button("🧹 Limpiar conversación"):
    st.session_state.mensajes = []
    st.rerun()

# Inicializar modelo con parámetros elegidos
chat_model = ChatGoogleGenerativeAI(
    model=modelo_seleccionado,
    temperature=temperatura
)

# -----------------------------
# Inicializar historial
# -----------------------------
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# -----------------------------
# Mostrar historial existente
# -----------------------------
for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# -----------------------------
# Entrada del usuario
# -----------------------------
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)

    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    respuesta = chat_model.invoke(st.session_state.mensajes)

    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.mensajes.append(respuesta)

