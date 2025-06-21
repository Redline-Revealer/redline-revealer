import streamlit as st
import sys
import os

# Add parent directory to path to access modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import welcome, map_page, assistant, about
from ui_helpers import render_answer_block
from prompt_handler import handle_prompt

# Configure page
st.set_page_config(page_title="Redline Revealer", layout="wide")

# Translation dictionary
text = {
    "English": {
        "title": "🏙️ Redline Revealer",
        "tagline": "Unearthing the past. Protecting the future.",
        "tab1": "📍 Redlining Map",
        "tab2": "🧠 LLM Assistant",
        "tab3": "👋 Welcome",
        "tab4": "💡 About Us",
        "map_header": "Historical Redlining Visualization",
        "map_info": "Map overlay and risk scoring will appear here.",
        "assistant_header": "AI Legal Assistant",
        "assistant_info": "Ask questions about heirs’ property, title issues, and stability strategies.",
        "input_label": "Ask me anything:",
        "submit": "Submit",
        "you_asked": "🔍 You asked:",
        "faq": "💡 Frequently Asked",
        "questions": [
            "What is heirs' property?",
            "Can I inherit property in Florida without a will?",
            "What is a partition action?",
            "How do I resolve unclear property titles?",
            "Can heirs sell inherited land without consent?",
            "Where do I start if I think I inherited land?",
            "What legal documents should I look for after someone passes away?",
        ],
    },
    "Español": {
        "title": "🏙️ Redline Revealer",
        "tagline": "Descubriendo el pasado. Protegiendo el futuro.",
        "tab1": "📍 Mapa de Redlining",
        "tab2": "🧠 Asistente Legal IA",
        "tab3": "👋 Bienvenida",
        "tab4": "💡 Sobre Nosotros",
        "map_header": "Visualización Histórica del Redlining",
        "map_info": "Aquí aparecerá la superposición del mapa y la puntuación de riesgo.",
        "assistant_header": "Asistente Legal con IA",
        "assistant_info": "Haz preguntas sobre propiedades heredadas, títulos y estrategias de estabilidad.",
        "input_label": "Haz tu pregunta aquí:",
        "submit": "Enviar",
        "you_asked": "🔍 Preguntaste:",
        "faq": "💡 Preguntas Frecuentes",
        "questions": [
            "¿Qué es una propiedad heredada?",
            "¿Puedo heredar una propiedad en Florida sin testamento?",
            "¿Qué es una acción de partición?",
            "¿Cómo resolver títulos de propiedad poco claros?",
            "¿Pueden los herederos vender la tierra sin consentimiento?",
            "¿Por dónde empiezo si creo que heredé un terreno?",
            "¿Qué documentos legales debo buscar tras el fallecimiento de alguien?",
        ],
    },
}

# Initialize session state
if "language" not in st.session_state:
    st.session_state.language = "English"
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "tab1"
if "submitted_question" not in st.session_state:
    st.session_state.submitted_question = ""
if "question_source" not in st.session_state:
    st.session_state.question_source = ""
if "last_answer" not in st.session_state:
    st.session_state.last_answer = None

# Language Selector
st.markdown(
    """
    <style>
    .compact-selectbox .stSelectbox > div {
        padding-top: 1px !important;
        padding-bottom: 1px !important;
        font-size: 0.65rem !important;
        min-height: 25px !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

language_row = st.columns([10, 1])
with language_row[1]:
    with st.container():
        st.markdown('<div class="compact-selectbox">', unsafe_allow_html=True)
        selected_language = st.selectbox(
            "Select Language:",
            ["English", "Español"],
            label_visibility="collapsed",
            key="language_toggle_box",
        )
        st.markdown("</div>", unsafe_allow_html=True)

        if selected_language != st.session_state.language:
            st.session_state.language = selected_language
            st.rerun()

# Use translation
L = text[st.session_state.language]

# Header
st.title(L["title"])
st.markdown(L["tagline"])

# Tab Switcher (radio styled like tabs)
tab_map = {
    "tab1": L["tab1"],
    "tab2": L["tab2"],
    "tab3": L["tab3"],
    "tab4": L["tab4"]
}

active_tab = st.radio(
    label="",
    options=list(tab_map.keys()),
    format_func=lambda x: tab_map[x],
    horizontal=True,
)
st.session_state.active_tab = active_tab

# Content for Tab 1
if st.session_state.active_tab == "tab1":
    map_page.render(L)

# Content for Tab 2
elif st.session_state.active_tab == "tab2":
    assistant.render(L)

# Content for Tab 3 (Welcome)
elif st.session_state.active_tab == "tab3":
    welcome.render(L)

# Content for Tab 4 (About)
elif st.session_state.active_tab == "tab4":
    about.render(L)
