import streamlit as st
from agent.legal_agent import get_legal_answer
from ui_helpers import render_answer_block

def render(L):
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
                    result = get_legal_answer(st.session_state.submitted_question)
                st.session_state.last_answer = {
                    "question": st.session_state.submitted_question,
                    "result": result,
                }
            else:
                result = st.session_state.last_answer["result"]

            # Handle the result properly for render_answer_block
            if isinstance(result, str):
                # If result is a string, wrap it in expected format
                formatted_result = {"answer": result}
            elif isinstance(result, dict):
                # If it's already a dict, ensure it has the right key
                if "answer" not in result and "result" in result:
                    formatted_result = {"answer": result["result"]}
                else:
                    formatted_result = result
            else:
                # Fallback for any other type
                formatted_result = {"answer": str(result)}
            
            render_answer_block(formatted_result)

    with col2:
        st.markdown(f"### {L['faq']}")
        for q in L["questions"]:
            if st.button(q):
                st.session_state.submitted_question = q
                st.session_state.question_source = "click"
                st.rerun()

        st.markdown(
            f"""
            <div style='font-size: 0.9rem; color: gray; margin-top: 1em;'>
            ⚠️ {L.get("legal_disclaimer", "This assistant provides general information, not legal advice. Please consult a legal professional for guidance.")}
            </div>
            """,
            unsafe_allow_html=True,
        )
