import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# ------- CONFIG GENERAL -------
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖", layout="wide")

# ------- PERSISTENCIA DE CONFIG -------
if "modelo" not in st.session_state:
    st.session_state.modelo = "gemini-2.5-flash"

if "temp" not in st.session_state:
    st.session_state.temp = 0.7

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# ---------- DISEÑO: CHAT CENTRADO + MENÚ A LA DERECHA ----------
left, center, right = st.columns([0.1, 0.7, 0.2])  # proporciones perfectas

# ---------- MENÚ A LA DERECHA ----------
with right:

    st.markdown("### ⚙️ **Menú**")

    # Select modelo (solo estético)
    modelo = st.selectbox(
        "Modelo:",
        ["gemini-2.5-flash", "gemini-pro", "gemini-1.5-flash"],
        index=["gemini-2.5-flash", "gemini-pro", "gemini-1.5-flash"].index(st.session_state.modelo)
    )
    st.session_state.modelo = modelo

    # Temperatura
    temperatura = st.slider(
        "Temperatura",
        min_value=0.0,
        max_value=1.0,
        step=0.01,
        value=st.session_state.temp
    )
    st.session_state.temp = temperatura

    # Estilo
    modo = st.radio(
        "Estilo de respuesta:",
        ["Corta", "Normal", "Detallada"],
        index=1
    )

    # Limpiar conversación
    if st.button("🧹 Limpiar conversación"):
        st.session_state.mensajes = []
        st.rerun()

    # Descargar
    if st.button("📄 Descargar conversación"):
        texto = "\n".join(
            ["USER: " + m.content if isinstance(m, HumanMessage)
             else "BOT: " + m.content for m in st.session_state.mensajes]
        )
        st.download_button(
            "Guardar archivo",
            texto,
            file_name="conversacion.txt"
        )

# ---------- ZONA DEL CHAT (CENTRADA) ----------
with center:
    st.title("🤖 Chatbot - paso 2 - con LangChain")
    st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit.*")

    # Mensaje de bienvenida solo si está vacío
    if len(st.session_state.mensajes) == 0:
        bienvenida = AIMessage(content="¡Hola! 👋 ¿En qué puedo ayudarte hoy?")
        st.session_state.mensajes.append(bienvenida)

    # MODELO DINÁMICO (funcional, no se toca lógica)
    chat_model = ChatGoogleGenerativeAI(
        model=st.session_state.modelo,
        temperature=st.session_state.temp
    )

    # Limitar historial
    MAX_HISTORY = 15
    st.session_state.mensajes = st.session_state.mensajes[-MAX_HISTORY:]

    # Render historial
    for msg in st.session_state.mensajes:
        role = "assistant" if isinstance(msg, AIMessage) else "user"
        with st.chat_message(role):
            st.markdown(msg.content, unsafe_allow_html=True)

    # Input usuario
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

