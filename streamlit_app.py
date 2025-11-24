import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")

st.title("🤖 Chatbot - paso 2 - con LangChain")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit.")


with st.sidebar:
    st.header("⚙️ Configuración del modelo")

    modelo = st.selectbox(
        "Modelo:",
        ["gemini-pro", "gemini-1.5-flash", "gemini-1.5-pro"],
        index=0
    )

    temperatura = st.slider(
        "Temperatura",
        0.0, 1.0, 0.7
    )

    limpiar = st.button("🧹 Limpiar conversación")

# Crear el modelo dinámicamente según selectbox
chat_model = ChatGoogleGenerativeAI(model=modelo, temperature=temperatura)


# Si el usuario pulsa “limpiar conversación”
if limpiar:
    st.session_state.mensajes = []

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []


# Mostrar historial
for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)

    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    # Obtener respuesta del modelo
    respuesta = chat_model.invoke(st.session_state.mensajes)

    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.mensajes.append(respuesta)

