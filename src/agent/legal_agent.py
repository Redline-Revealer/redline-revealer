"""
Legal Assistant Agent for Redline Revealer

Uses Azure OpenAI + LangChain RAG pipeline to generate legal insights
about heirs' property laws.
"""
import os
import json
import re
from typing import Optional
from dotenv import load_dotenv
from openai import AzureOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from pydantic.types import SecretStr
from utils.state_list import US_STATES

load_dotenv()

# Set up OpenAI client
try:
    azure_key = os.getenv("AZURE_OPENAI_KEY")
    if azure_key:
        client = AzureOpenAI(
            api_key=azure_key,
            api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2023-12-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT") or "",
        )
    else:
        print("Warning: AZURE_OPENAI_KEY not found in environment variables")
        client = None
except Exception as e:
    print(f"Warning: Could not initialize Azure OpenAI client: {e}")
    client = None

# Load public blob links for source documents
with open(os.path.join("data", "source_links.json"), "r") as f:
    source_links = json.load(f)
# Load curated law links
with open(os.path.join("data", "state_links.json"), "r") as f:
    reference_links = json.load(f)

# Helper to check if a document is generic (not state-specific)
def is_generic_doc(filename):
    return not re.search(r"-[a-z]{2}-\d{4}", filename.lower())


# Helper to check if a document is state-specific
def is_state_specific(doc):
    source = doc.metadata.get("source", "").lower()
    for state in US_STATES:
        if state.lower() in source:
            return True
    return False


def get_reference_link(question):
    question_lower = question.lower()
    for state, topics in reference_links.items():
        if state.lower() in question_lower:
            for topic, link in topics.items():
                topic_words = topic.lower().split()
                if any(word in question_lower for word in topic_words):
                    return link
    return None


def extract_state(question):
    for state in US_STATES:
        if re.search(rf"\b{state}\b", question, re.IGNORECASE):
            return state
    return None


# Setup RAG (FAISS + LangChain)
try:
    azure_key = os.getenv("AZURE_OPENAI_KEY")
    if azure_key:
        embedding_model = AzureOpenAIEmbeddings(
            azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT") or "",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT") or "",
            api_key=SecretStr(azure_key),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2023-12-01-preview",
        )
    else:
        print("Warning: AZURE_OPENAI_KEY not found for embeddings")
        embedding_model = None
    
    # Check if the index directory exists
    index_path = "data/indexes/legal_docs_index"
    if embedding_model and os.path.exists(index_path):
        vectorstore = FAISS.load_local(
            index_path,
            embeddings=embedding_model,
            allow_dangerous_deserialization=True,
        )
        print(f"✅ Loaded FAISS index with {vectorstore.index.ntotal} documents")
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    else:
        if not embedding_model:
            print("⚠️ Warning: Could not initialize embedding model")
        else:
            print(f"⚠️ Warning: FAISS index not found at {index_path}")
        vectorstore = None
        retriever = None
except Exception as e:
    print(f"⚠️ Warning: Could not load FAISS index: {e}")
    vectorstore = None
    retriever = None

try:
    azure_key = os.getenv("AZURE_OPENAI_KEY")
    if azure_key:
        llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            api_key=SecretStr(azure_key),
            azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        )
    else:
        print("Warning: AZURE_OPENAI_KEY not found for LLM")
        llm = None
except Exception as e:
    print(f"Warning: Could not initialize LLM: {e}")
    llm = None

custom_prompt_text = (
    "You are a legal assistant helping someone with a legal question.\n\n"
    "Use the following context documents to answer the question. Only use them "
    "if they are clearly relevant to the user's question.\n\n"
    "If the documents are not about the topic the user is asking (e.g., if the "
    "user is asking about vehicle registration but the documents are about "
    "heirs’ property), say:\n"
    '"I don’t have information on that specific topic."\n\n'
    "Include in your answer:\n"
    "- Steps the person should take\n"
    "- Any laws, legal terms, or definitions if available\n"
    "- Names of relevant agencies, organizations, or websites if found\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}"
)

custom_prompt = PromptTemplate.from_template(custom_prompt_text)

generic_prompt_text = (
    "You are a helpful legal assistant.\n\n"
    "A user has asked the following question:\n\n"
    '"{question}"\n\n'
    "Try to answer in a way that is useful and easy to understand. "
    "If you don’t know the answer or it requires specific legal information "
    "from a state that’s not available, say so clearly.\n\n"
    "If applicable, include:\n"
    "- General steps the person should take\n"
    "- Legal terms (e.g., probate, partition, title search)\n"
    "- Practical advice (e.g., who to contact, where to go)\n\n"
    "Avoid making assumptions about heirs’ property unless the question is "
    "clearly related to it."
)

generic_prompt = PromptTemplate.from_template(generic_prompt_text)


def get_legal_answer(question):
    try:
        if not llm:
            return "Azure OpenAI is not available. Please check your configuration."
            
        state = extract_state(question)

        is_us_state = state is not None and any(
            state.lower() == s.lower() for s in US_STATES
        )

        filtered_docs = []

        if is_us_state and retriever:
            # Only retrieve documents if it's a US state and retriever is available
            docs = retriever.get_relevant_documents(question)
            for doc in docs:
                print("[DEBUG] Retrieved doc source:", doc.metadata.get("source", ""))
                print(
                    "[DEBUG] Document content sample:", doc.page_content[:300]
                )  # limit to avoid flooding
            for doc in docs:
                content = doc.page_content.lower()
                source = doc.metadata.get("source", "").lower()
                if state and (state.lower() in content or state.lower() in source):
                    filtered_docs.append(doc)
        else:
            # Non-US questions or no retriever should skip RAG
            filtered_docs = []

        # RAG path
        if filtered_docs:
            chain = load_qa_chain(llm, chain_type="stuff", prompt=custom_prompt)
            answer = chain.run(input_documents=filtered_docs, question=question)
            # Ensure answer is a string
            if not isinstance(answer, str):
                answer = str(answer)
            result = {"result": answer, "source_documents": filtered_docs}
        else:
            # Direct LLM answer (no documents used)
            result = {"source_documents": []}
            formatted_question = generic_prompt.format(question=question)
            answer = llm.invoke(formatted_question).content

        # Retry if response is unhelpful
        if isinstance(answer, str) and ("i don't know" in answer.lower() or len(answer.strip()) < 40):
            answer = llm.invoke(question).content

        # Append sources only if documents were used
        if result["source_documents"]:
            sources = set()
            for doc in result["source_documents"]:
                filename = os.path.basename(doc.metadata.get("source", ""))
                link = source_links.get(filename)
                if link:
                    sources.add(f"[{filename}]({link})")
                else:
                    sources.add(filename)

            if sources:
                source_list = "\n".join(f"🔹 {src}" for src in sorted(sources))
                answer += "\n\n📄 Source Documents Used:\n" + source_list

        # Add curated law link if available
        curated_link = get_reference_link(question)
        if curated_link:
            answer += f"\n\n🔗 For more info, see: {curated_link}"

        return answer

    except Exception as e:
        print(f"Error in get_legal_answer: {e}")
        return (
            "We weren’t able to generate a response right now. Please try again later."
        )
