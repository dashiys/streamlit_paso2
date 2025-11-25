import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# ------- CONFIG GENERAL -------
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖", layout="wide")

# ------- ESTADO PARA MOSTRAR/OCULTAR MENU -------
if "mostrar_menu" not in st.session_state:
    st.session_state.mostrar_menu = True

if "modelo" not in st.session_state:
    st.session_state.modelo = "gemini-2.5-flash"

if "temp" not in st.session_state:
    st.session_state.temp = 0.7

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# ------- DISEÑO GLOBAL EN DOS COLUMNAS -------
col_chat, col_menu = st.columns([4, 1])   # Chat grande / menú estrecho a la DERECHA

# ------- BOTÓN FLOTANTE PARA MOSTRAR/OCULTAR MENU -------
with col_chat:
    if st.button("⚙️", key="toggle_menu"):
        st.session_state.mostrar_menu = not st.session_state.mostrar_menu

# ------- MENÚ EN LA DERECHA  -------
with col_menu:
    if st.session_state.mostrar_menu:
        st.header("⚙️ Configuración del modelo")

        # Select solo estético (no afecta lógica)
        modelo = st.selectbox(
            "Modelo:",
            ["gemini-2.5-flash", "gemini-pro", "gemini-1.5-flash"],
            index=["gemini-2.5-flash", "gemini-pro", "gemini-1.5-flash"].index(st.session_state.modelo)
        )
        st.session_state.modelo = modelo

        temperatura = st.slider(
            "Temperatura",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            value=st.session_state.temp
        )
        st.session_state.temp = temperatura

        modo = st.radio(
            "Estilo de respuesta:",
            ["Corta", "Normal", "Detallada"],
            index=1
        )

        if st.button("🧹 Limpiar conversación"):
            st.session_state.mensajes = []
            st.rerun()

        if st.button("📄 Descargar conversación"):
            texto = "\n".join(
                ["USER: " + m.content if isinstance(m, HumanMessage)
                 else "BOT: " + m.content for m in st.session_state.mensajes]
            )
            st.download_button("Guardar archivo", texto, file_name="conversacion.txt")

# ------- CHAT 
with col_chat:
    st.title("🤖 Chatbot - paso 2 - con LangChain")
    st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit.")

    if len(st.session_state.mensajes) == 0:
        bienvenida = AIMessage(content="¡Hola! 👋 ¿En qué puedo ayudarte hoy?")
        st.session_state.mensajes.append(bienvenida)

    chat_model = ChatGoogleGenerativeAI(
        model=st.session_state.modelo,
        temperature=st.session_state.temp
    )

    MAX_HISTORY = 15
    st.session_state.mensajes = st.session_state.mensajes[-MAX_HISTORY:]

    # Render historial
    for msg in st.session_state.mensajes:
        role = "assistant" if isinstance(msg, AIMessage) else "user"
        with st.chat_message(role):
            st.markdown(msg.content, unsafe_allow_html=True)

    pregunta = st.chat_input("Escribe tu mensaje:")

    if pregunta:
        with st.chat_message("user"):
            st.markdown(pregunta)

        if modo == "Corta":
            mensaje_final = pregunta + "\nResponde en una frase breve."
        elif modo == "Detallada":
            mensaje_final = pregunta + "\nResponde con detalle y paso a paso."
        else:
            mensaje_final = pregunta

        st.session_state.mensajes.append(HumanMessage(content=mensaje_final))

        with st.chat_message("assistant"):
            with st.spinner("Escribiendo..."):
                respuesta = chat_model.invoke(st.session_state.mensajes)
            st.markdown(respuesta.content, unsafe_allow_html=True)

        st.session_state.mensajes.append(respuesta)

