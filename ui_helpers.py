import streamlit as st


def render_answer_block(result: dict):
    # Main answer
    st.markdown("### 🧠 AI Legal Assistant Answer")
    st.markdown(result["answer"], unsafe_allow_html=True)

    # Curated link
    if result.get("curated_link"):
        curated_block = (
            "<div style='margin-top:25px;padding:16px;"
            "background-color:#eef6fc;"
            "border-left:5px solid #2a5bd7;border-radius:8px;'>"
            "<p style='margin:0;font-size:15px;color:#1a1a1a;'>"
            "📘 For more information, consult the full legal guide below:</p>"
            f"<a href='{result['curated_link']}' target='_blank' style='"
            "display:inline-block;margin-top:8px;padding:10px 16px;"
            "background-color:#2a5bd7;color:#fff;text-decoration:none;"
            "font-weight:600;border-radius:6px;'>"
            "🔍 View Legal Resource</a></div>"
        )
        st.markdown(curated_block, unsafe_allow_html=True)

    # Source files
    if result.get("source_info"):
        st.markdown("### 📄 Source Documents Used:")
        for src in result["source_info"]:
            st.markdown(f"🔹 {src}", unsafe_allow_html=True)
