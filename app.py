<<<<<<< HEAD:app.py
import streamlit as st
from modules import welcome, map_page, assistant, about
=======
"""Main Streamlit App Launcher for Redline Revealer.

Initializes session state and routes to modular pages: Welcome, Map, Assistant, About.
Serves as the entry point for Streamlit execution.
"""

from ui_helpers import render_answer_block
from prompt_handler import handle_prompt
from pages import welcome, map, assistant, about
import streamlit as st
import sys
import os

# Add /src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62:src/app.py

# Configure page
st.set_page_config(page_title="Redline Revealer", layout="wide")

# Translation dictionary
text = {
    "English": {
        "title": "🏙️ Redline Revealer",
        "tagline": "Unearthing the past. Protecting the future.",
        "tab1": "📍 Redlining Map",
        "tab2": "🧠 LLM Assistant",
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
tab_map = {"tab1": L["tab1"], "tab2": L["tab2"]}
active_tab = st.radio(
    label="",
    options=["tab1", "tab2"],
    format_func=lambda x: tab_map[x],
    horizontal=True,
)
st.session_state.active_tab = active_tab

# Content for Tab 1
if st.session_state.active_tab == "tab1":
    st.subheader(L["map_header"])
    st.info(L["map_info"])

# Content for Tab 2
elif st.session_state.active_tab == "tab2":
    st.subheader(L["assistant_header"])
    st.info(L["assistant_info"])

    col1, col2 = st.columns([2.5, 1.5])

    with col1:
        with st.form("question_form", clear_on_submit=True):
            user_input = st.text_input(L["input_label"], key="user_input")
            submitted = st.form_submit_button(L["submit"])

            if submitted and user_input.strip():
                st.session_state.submitted_question = user_input.strip()
                st.session_state.question_source = "typed"
                st.rerun()

        if st.session_state.submitted_question:
            st.write(f"{L['you_asked']} {st.session_state.submitted_question}")

            if (
                st.session_state.last_answer is None
                or st.session_state.last_answer["question"]
                != st.session_state.submitted_question
            ):
                with st.spinner(
                    "Thinking..."
                    if st.session_state.language == "English"
                    else "Pensando..."
                ):
                    result = handle_prompt(st.session_state.submitted_question)
                st.session_state.last_answer = {
                    "question": st.session_state.submitted_question,
                    "result": result,
                }
            else:
                result = st.session_state.last_answer["result"]

            render_answer_block(result)

    with col2:
        st.markdown(f"### {L['faq']}")
        for q in L["questions"]:
            if st.button(q):
                st.session_state.submitted_question = q
                st.session_state.question_source = "click"
                st.rerun()

        # Legal Disclaimer
        st.markdown(
            """
        <div style='font-size: 0.9rem; color: gray; margin-top: 1em;'>
        ⚠️ This assistant provides general information, not legal advice. Please consult a legal professional for guidance.
        </div>
        """,
            unsafe_allow_html=True,
        )
