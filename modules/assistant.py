"""LLM Assistant Page for Redline Revealer.

Provides an interactive interface for users to ask legal questions about
heirs’ property, title issues, and housing instability. Integrates Azure OpenAI
with retrieval-augmented generation (RAG) and fallback logic.
"""

import streamlit as st
from agent.legal_agent import get_legal_answer


def render():
    st.title("AI Legal Assistant")
    st.info(
        "Ask questions about heirs’ property, title issues, or stability strategies."
    )

    user_input = st.text_input("Ask me anything:")

    if user_input:
        st.write(f"🔍 You asked: {user_input}")
        with st.spinner("Thinking..."):
            response = get_legal_answer(user_input)
        st.markdown(response)
