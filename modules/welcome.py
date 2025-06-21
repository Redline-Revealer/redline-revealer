# Welcome Page UI logic
import streamlit as st


def render():
    st.title("Welcome to Redline Revealer")
    st.subheader("Unearthing the past. Protecting the future.")
    st.markdown(
        """
    This civic tech app uses AI and historical mapping to reveal patterns of redlining and housing risk. 
    Explore overlays, generate insights, and discover how discriminatory housing policies still impact communities today.
    """
    )
