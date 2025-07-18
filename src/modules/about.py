"""About Page UI for Redline Revealer.

Displays project mission, Responsible AI (RAI) commitments, and team member bios.
This module is rendered as the 'About Us' tab in the main Streamlit app.
"""

import streamlit as st


def render(L):
    st.title(L.get("about_title", "About Redline Revealer"))

    # 🚨 Project Overview
    st.subheader(L.get("problem_header", "🧭 What Problem Are We Solving?"))
    st.markdown(
        L.get("project_description",
        """
    **Redline Revealer** is a civic-tech tool built for the Microsoft x Women in Cloud AI Hackathon.  
    We use AI and Azure Maps to detect historical redlining and visualize modern housing instability,  
    helping communities identify systemic risk and take action through data-driven advocacy.
    """)
    )

    # 🔐 RAI Commitments
    st.subheader(L.get("rai_header", "🔐 Responsible AI (RAI) Commitments"))
    st.markdown(
        L.get("rai_commitments",
        """
    - ✅ **Fairness** – Identifies historic racial bias without reinforcing it  
    - 🛡️ **Reliability** – Includes fallback logic if AI responses fail  
    - 🔒 **Privacy** – No user data is stored; API keys are secured  
    - 🌍 **Inclusiveness** – Accessible layout with contrast-aware visuals  
    - 📋 **Accountability** – All changes tracked in GitHub  
    """)
    )

    # 👩🏽‍💻 Meet the Team
    st.subheader(L.get("team_header", "👩🏽‍💻 Meet the Team"))
    team = [
        {
            "name": "Portia Jefferson",
            "role": "Project Manager / DevSecOps",
            "img": "assets/JeffersonP.jpg",
            "bio": "Portia is a Certified Cybersecurity Professional, Certified AI Consultant, and current cybersecurity student with a background in IT, finance, and compliance. While serving as the Project Manager, she also led DevSecOps efforts—including managing GitHub branches and CI/CD workflows, handling environment secrets across platforms, and troubleshooting deployment issues in Streamlit. Portia played a key role in maintaining project momentum, unblocking teammates, and ensuring technical systems stayed organized and secure. She joined Redline Revealer to apply her skills in a real-world AI context, driven by her passion for ethical tech and empowering underserved communities through data transparency and accountability."
        },
        {
            "name": "Esthefany Humpire Vargas",
            "role": "AI Engineer",
            "img": "assets/esthef2025.jpg",
            "bio": "Esthefany developed the AI Legal Assistant for Redline Revealer, implementing LangChain, Azure OpenAI, and document retrieval to provide accessible legal guidance. She focused on prompt engineering, state-specific filtering, and simplifying complex legal topics using AI."
        },
        {
            "name": "Henok Tariku",
            "role": "Data Analyst",
            "img": "assets/henok-pic.jpg",
            "bio": "Henok sourced and visualized historical redlining datasets and created dashboards for community risk scoring. Henok is a junior Data Analyst and Computer Science student at the University of the People, holding a CGPA of 3.94. He brings a strong foundation in Python, Power BI, Excel, and Azure data tools, combined with a deep passion for mathematics, critical thinking, and data-driven storytelling. As a member of the Redline Revealer team, Henok contributes technical insights to spatial data visualization, supporting the integration of historical redlining datasets with modern geospatial tools. With an eye for detail and a learner's mindset, he plays a vital role in dataset validation, statistical interpretation, and UI clarity. Henok is driven by a desire to apply data science in meaningful social contexts amplifying underserved voices and uncovering patterns that support transparency and equity."
        },
        {
            "name": "Megan Nepshinsky",
            "role": "Full-Stack Developer",
            "img": "assets/megan-pic.jpg",
            "bio": "Megan developed the Streamlit frontend, linked the assistant, and connected all backend logic to deliver a seamless UI. Megan is a Junior Full Stack Developer with experience in Python, JavaScript, Django, and React, focused on building clean, efficient back-end systems and responsive front-end interfaces. Her technical projects highlight a talent for full-stack development and a deep commitment to purpose-driven tech."
        }
    ]

    for person in team:
        col1, col2 = st.columns([1, 3])
        with col1:
            try:
                st.image(person["img"], use_container_width=True)
            except Exception:
                st.warning(L.get("image_not_found", f"Image not found: {person['img']}"))
        with col2:
            st.markdown(f"**{person['name']}** – *{person['role']}*\n\n{person['bio']}")
        st.markdown("---")
