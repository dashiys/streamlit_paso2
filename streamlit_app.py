import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# ------- CONFIG GENERAL -------
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖", layout="wide")

# ------- ESTILO GLOBAL 
st.markdown(
    """
    <style>
        /* --- Menú derecho gris suave --- */
        [data-testid="stExpander"] {
            background-color: #f2f2f2 !important;
            border-radius: 10px;
            padding: 10px;
        }

        /* --- Chat con scroll, input siempre abajo --- */
        .block-container {
            padding-top: 2rem !important;
        }
        .stChatMessage {
            max-height: 65vh;
            overflow-y: auto;
        }

        /* --- Input abajo estilo ChatGPT --- */
        #chat-input-box {
            position: fixed;
            bottom: 20px;
            left: 20%;
            width: 60%;
            z-index: 999;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ------- PERSISTENCIA DE CONFIG -------
if "modelo" not in st.session_state:
    st.session_state.modelo = "gemini-2.5-flash"

if "temp" not in st.session_state:
    st.session_state.temp = 0.7

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []


# ---------- MENÚ A LA DERECHA 
with st.expander("⚙️ Menú", expanded=True):

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

    modo = st.radio("Estilo de respuesta:", ["Corta", "Normal", "Detallada"], index=1)

    if st.button("🧹 Limpiar conversación"):
        st.session_state.mensajes = []
        st.rerun()

    texto_export = "\n".join(
        ["USER: " + m.content if isinstance(m, HumanMessage)
         else "BOT: " + m.content for m in st.session_state.mensajes]
    )
    st.download_button("📄 Descargar conversación", texto_export, file_name="conversacion.txt")


# -------- CHAT CENTRADO --------
st.title("🤖 Chatbot - paso 2 - con LangChain")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit.*")

# Mensaje bienvenida
if len(st.session_state.mensajes) == 0:
    bienvenida = AIMessage(content="¡Hola! 👋 ¿En qué puedo ayudarte hoy?")
    st.session_state.mensajes.append(bienvenida)

# Modelo real (no se toca)
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

# -------- INPUT FIJO ABAJO --------
with st.container():
    st.markdown('<div id="chat-input-box">', unsafe_allow_html=True)
    pregunta = st.chat_input("Escribe tu mensaje:")
    st.markdown('</div>', unsafe_allow_html=True)


# -------- PROCESAR MENSAJE --------
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


