from agent.legal_agent import get_legal_answer
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def handle_prompt(user_input: str) -> dict:
    """
    Handles user prompt input by calling the legal agent and parsing response.

    Returns a structured dictionary with:
    - 'answer': the main text
    - 'curated_link': URL (if any)
    - 'source_info': list of sources (if any)
    """
    if not user_input or not user_input.strip():
        return {
            "answer": "⚠️ Please enter a valid legal question.",
            "curated_link": None,
            "source_info": []
        }

    raw_response = get_legal_answer(user_input)

    # Initialize fields
    curated_link = None
    source_info = []
    answer = raw_response.strip()

    # Extract curated link
    if "🔗 For more info, see:" in answer:
        parts = answer.split("🔗 For more info, see:")
        answer = parts[0].strip()
        curated_link = parts[1].strip()

    # Extract sources
    if "📄 Sources:" in answer:
        parts = answer.split("📄 Sources:")
        answer = parts[0].strip()
        source_info = [src.strip()
                       for src in parts[1].split(",") if src.strip()]

    return {
        "answer": answer,
        "curated_link": curated_link,
        "source_info": source_info
    }
