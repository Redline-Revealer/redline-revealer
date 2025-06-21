# Welcome Page UI logic
import streamlit as st


def render(L):
    st.title(L["title"])
    st.subheader(L["tagline"])
    st.markdown(
        L.get("welcome_description", 
        """
    This civic tech app uses AI and historical mapping to reveal patterns of redlining and housing risk. 
    Explore overlays, generate insights, and discover how discriminatory housing policies still impact communities today.
    """)
    )
