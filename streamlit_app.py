import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage


st.set_page_config(page_title="Chatbot Básico", page_icon="🤖", layout="wide")

st.title("🤖 Chatbot - paso 2 - con LangChain")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit.")

st.markdown("""
    <style>
        .menu-derecha {
            position: fixed;
            top: 100px;
            right: 20px;
            width: 260px;
            padding: 15px;
            background: #ffffff;
            border: 1px solid #ccc;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            transition: transform 0.3s ease, opacity 0.3s ease;
            z-index: 9999;
        }
        .menu-hidden {
            transform: translateX(350px);
            opacity: 0;
        }
        .menu-btn {
            position: fixed;
            top: 40px;
            right: 30px;
            z-index: 10000;
            padding: 10px 14px;
            font-size: 22px;
            border-radius: 8px;
            border: 1px solid #ccc;
            background: white;
            cursor: pointer;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }
    </style>
""", unsafe_allow_html=True)

# Estado del menú
if "menu_visible" not in st.session_state:
    st.session_state.menu_visible = True

# Botón para abrir/cerrar menú
if st.button("☰", key="menu", help="Mostrar / Ocultar menú"):
    st.session_state.menu_visible = not st.session_state.menu_visible
    
menu_clase = "menu-derecha" + ("" if st.session_state.menu_visible else " menu-hidden")
st.markdown(f'<div class="{menu_clase}">', unsafe_allow_html=True)

st.markdown("### ⚙️ Configuración del modelo")

modelo_seleccionado = st.selectbox(
    "Modelo:",
    ["gemini-2.0-flash", "gemini-pro", "gemini-1.5-flash"]
)

temperatura = st.slider(
    "Temperatura",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1
)

if st.button("🧹 Limpiar conversación"):
    st.session_state.mensajes = []
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Inicializar historial
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Inicializar modelo
chat_model = ChatGoogleGenerativeAI(
    model=modelo_seleccionado,
    temperature=temperatura
)

# Mostrar historial
for msg in st.session_state.mensajes:
    rol = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(rol):
        st.markdown(msg.content)

# Entrada usuario
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)

    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    respuesta = chat_model.invoke(st.session_state.mensajes)

    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.mensajes.append(respuesta)

