import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# ------- CONFIG GENERAL -------
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖", layout="wide")

# ------- CSS PANEL DERECHA -------
st.markdown("""
<style>
/* Contenedor del panel */
#panel-derecha {
    position: fixed;
    top: 70px;
    right: 0;
    width: 280px;
    height: 100%;
    background-color: #f5f5f7;
    padding: 20px;
    border-left: 1px solid #ddd;
    box-shadow: -2px 0 6px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
    z-index: 999;
}
.panel-hidden {
    transform: translateX(100%);
}

#boton-menu {
    position: fixed;
    top: 80px;
    right: 15px;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 8px 10px;
    cursor: pointer;
    z-index: 1000;
}
</style>
""", unsafe_allow_html=True)

# ------- ESTADO DEL PANEL -------
if "panel_visible" not in st.session_state:
    st.session_state.panel_visible = True

# ------- BOTÓN MOSTRAR/OCULTAR -------
if st.button("⚙️", key="boton-menu"):
    st.session_state.panel_visible = not st.session_state.panel_visible

panel_class = "" if st.session_state.panel_visible else "panel-hidden"

# ------- HTML PANEL DERECHA -------
st.markdown(f"""
<div id="panel-derecha" class="{panel_class}">
    <h3>⚙️ Configuración del modelo</h3>

    <p><b>Modelo:</b></p>
    <div id="modelo"></div>

    <p><b>Temperatura:</b></p>
    <div id="temperatura"></div>

    <p><b>Estilo de respuesta:</b></p>
    <div id="modo"></div>

    <br>
    <div id="limpiar"></div>
    <br>
    <div id="descargar"></div>
</div>
""", unsafe_allow_html=True)

with st.container():
    modelo = st.selectbox(
        "Modelo:",
        ["gemini-2.5-flash", "gemini-pro", "gemini-1.5-flash"],
        key="modelo_real"
    )

    temperatura = st.slider(
        "Temperatura",
        0.0, 1.0, 0.7,
        key="temp_real"
    )

    modo = st.radio(
        "Estilo de respuesta:",
        ["Corta", "Normal", "Detallada"],
        index=1,
        key="modo_real"
    )

    limpiar_btn = st.button("🧹 Limpiar conversación", key="limpiar_real")
    descargar_btn = st.button("📄 Descargar conversación", key="descargar_real")

# Push los controles al HTML del panel
st.session_state._html = {
    "modelo": st.session_state.modelo_real,
    "temperatura": st.session_state.temp_real,
    "modo": st.session_state.modo_real,
}

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

if limpiar_btn:
    st.session_state.mensajes = []
    st.rerun()

if descargar_btn:
    texto = "\n".join(
        ["USER: " + m.content if isinstance(m, HumanMessage)
         else "BOT: " + m.content for m in st.session_state.mensajes]
    )
    st.download_button("Guardar archivo", texto, file_name="conversacion.txt")

st.title("🤖 Chatbot - paso 2 - con LangChain")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit.")

if len(st.session_state.mensajes) == 0:
    bienvenida = AIMessage(content="¡Hola! 👋 ¿En qué puedo ayudarte hoy?")
    st.session_state.mensajes.append(bienvenida)

chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=st.session_state.temp_real
)

MAX_HISTORY = 15
st.session_state.mensajes = st.session_state.mensajes[-MAX_HISTORY:]

for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)

    mensaje_final = pregunta
    if st.session_state.modo_real == "Corta":
        mensaje_final += "\nResponde en una frase."
    elif st.session_state.modo_real == "Detallada":
        mensaje_final += "\nExplica paso a paso y con detalle."

    st.session_state.mensajes.append(HumanMessage(content=mensaje_final))

    with st.chat_message("assistant"):
        with st.spinner("Escribiendo..."):
            respuesta = chat_model.invoke(st.session_state.mensajes)
        st.markdown(respuesta.content)

    st.session_state.mensajes.append(respuesta)

