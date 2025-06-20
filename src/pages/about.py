"""About Page UI for Redline Revealer.

Displays project mission, Responsible AI (RAI) commitments, and team member bios.
This module is rendered as the 'About Us' tab in the main Streamlit app.
"""

import streamlit as st


def render_about_page():
    st.title("About Redline Revealer")

    # 🌍 Project Overview
    st.subheader("🧭 What Problem Are We Solving?")
    st.markdown(
        "**Redline Revealer** is a civic-tech tool built for the "
        "Microsoft x Women in Cloud AI Hackathon.\n"
        "We use AI and Azure Maps to detect historical redlining and "
        "visualize modern housing instability, helping communities "
        "identify systemic risk and take action through data-driven advocacy."
    )

    # 🔐 Responsible AI Commitments
    st.subheader("🔐 Responsible AI (RAI) Commitments")
    st.markdown(
        "- ✅ **Fairness** – Identifies historic racial bias without reinforcing it\n"
        "- 🛡️ **Reliability** – Includes fallback logic if AI responses fail\n"
        "- 🔒 **Privacy** – No user data is stored; API keys are secured\n"
        "- 🌈 **Inclusiveness** – Accessible layout with contrast-aware visuals\n"
        "- 📋 **Accountability** – All changes tracked in GitHub"
    )

    # 👩🏽‍💻 Meet the Team
    st.subheader("👩🏽‍💻 Meet the Team")

    team = [
        {
            "name": "Portia Jefferson",
            "role": "Project Manager / DevSecOps",
            "img": "assets/jeffersonP.jpg",
            "bio": "Portia coordinated the project, managed GitHub and DevOps, "
                   "and oversaw security, architecture, and submission."
        },
        {
            "name": "Esthefany Humpire Vargas",
            "role": "AI Engineer",
            "img": "assets/esthefany.jpg",
            "bio": "Esthefany built and tested AI prompts using Azure OpenAI and "
                   "created helper scripts for legal insight generation."
        },
        {
            "name": "Henok Tariku",
            "role": "Data Analyst",
            "img": "assets/henok.jpg",
            "bio": "Henok sourced and visualized historical redlining datasets and "
                   "created dashboards for community risk scoring."
        },
        {
            "name": "Megan Nepshinsky",
            "role": "Full-Stack Developer",
            "img": "assets/megan.jpg",
            "bio": "Megan developed the Streamlit frontend, linked the assistant, and "
                   "connected all backend logic to deliver a seamless UI."
        }
    ]

    for person in team:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(person["img"], use_column_width=True)
        with col2:
            st.markdown(f"**{person['name']}** – *{person['role']}*\n\n{person['bio']}")
        st.markdown("---")
