"""
Legal Assistant Agent for Redline Revealer

Uses Azure OpenAI + LangChain RAG pipeline to generate legal insights
about heirs' property laws.
"""
<<<<<<< HEAD


=======
>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62
import os
import json
import re
from dotenv import load_dotenv
from openai import AzureOpenAI
<<<<<<< HEAD
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_community.vectorstores import (
    FAISS
)
=======
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from utils.state_list import US_STATES

<<<<<<< HEAD

=======
>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62
load_dotenv()

# Set up OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
<<<<<<< HEAD
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
=======
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62
)

# Load public blob links for source documents
with open(os.path.join("data", "source_links.json"), "r") as f:
    source_links = json.load(f)
<<<<<<< HEAD

=======
>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62
# Load curated law links
with open(os.path.join("data", "state_links.json"), "r") as f:
    reference_links = json.load(f)

<<<<<<< HEAD

=======
>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62
# Helper to check if a document is generic (not state-specific)
def is_generic_doc(filename):
    return not re.search(r"-[a-z]{2}-\d{4}", filename.lower())


<<<<<<< HEAD
=======
# Helper to check if a document is state-specific
def is_state_specific(doc):
    source = doc.metadata.get("source", "").lower()
    for state in US_STATES:
        if state.lower() in source:
            return True
    return False


>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62
def get_reference_link(question):
    question_lower = question.lower()
    for state, topics in reference_links.items():
        if state.lower() in question_lower:
            for topic, link in topics.items():
                topic_words = topic.lower().split()
<<<<<<< HEAD
                if all(word in question_lower for word in topic_words):
=======
                if any(word in question_lower for word in topic_words):
>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62
                    return link
    return None


<<<<<<< HEAD
# Helper to extract state name from question
def extract_state(question):
    for state in US_STATES:
        if re.search(rf"\b{state}\b", question, re.IGNORECASE):
            return state.lower()
=======
def extract_state(question):
    for state in US_STATES:
        if re.search(rf"\b{state}\b", question, re.IGNORECASE):
            return state
>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62
    return None


# Setup RAG (FAISS + LangChain)
embedding_model = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)
<<<<<<< HEAD

vectorstore = FAISS.load_local(
    "data/indexes/legal_docs_index",
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
)
=======
vectorstore = FAISS.load_local(
    "data/indexes/legal_docs_index",
    embeddings=embedding_model,
    allow_dangerous_deserialization=True,
)
print(f"✅ Loaded FAISS index with {len(vectorstore.docstore._dict)} documents")

>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
)

<<<<<<< HEAD
# Custom prompt for QA
custom_prompt_text = (
    "You are a legal assistant helping someone understand how to resolve "
    "heirs' property issues.\n\n"
    "Use the following documents to give a detailed and actionable response, "
    "including:\n"
    "- Steps the person should take\n"
    "- Names of organizations, contact info, and websites if available\n"
    "- Legal terms or state laws if mentioned in the documents\n\n"
    "If you don't find information in the documents, say \"I don't know\".\n\n"
    "Context:\n{context}\n\nQuestion: {question}"
)
custom_prompt = PromptTemplate.from_template(custom_prompt_text)

=======
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

>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62

def get_legal_answer(question):
    try:
        state = extract_state(question)
<<<<<<< HEAD
        docs = retriever.get_relevant_documents(question)

        # Filter documents
        filtered_docs = []
        if state:
            for doc in docs:
                content = doc.page_content.lower()
                source = doc.metadata.get("source", "").lower()
                if state in content or state in source:
                    filtered_docs.append(doc)
        else:
            # Only allow generic docs if state not found
            for doc in docs:
                filename = os.path.basename(
                    doc.metadata.get("source", "")
                ).lower()
                if is_generic_doc(filename):
                    filtered_docs.append(doc)

        # Use RAG if there are any documents
        if filtered_docs:
            chain = load_qa_chain(
                llm,
                chain_type="stuff",
                prompt=custom_prompt
            )
            answer = chain.run(
                input_documents=filtered_docs,
                question=question
            )
            result = {"result": answer, "source_documents": filtered_docs}
        else:
            # Fallback to raw LLM
            result = {"source_documents": []}
            answer = llm.invoke(question).content

        # Fallback again if LLM reply is too short or unhelpful
        if "i don't know" in answer.lower() or len(answer.strip()) < 40:
            answer = llm.invoke(question).content

        # Add clickable source links
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
            answer += (
                "\n\n📄 Source Documents Used:\n"
                f"{source_list}"
            )
=======

        is_us_state = state is not None and any(
            state.lower() == s.lower() for s in US_STATES
        )

        filtered_docs = []

        if is_us_state:
            # Only retrieve documents if it's a US state
            docs = retriever.get_relevant_documents(question)
            for doc in docs:
                print("[DEBUG] Retrieved doc source:", doc.metadata.get("source", ""))
                print(
                    "[DEBUG] Document content sample:", doc.page_content[:300]
                )  # limit to avoid flooding
            for doc in docs:
                content = doc.page_content.lower()
                source = doc.metadata.get("source", "").lower()
                if state.lower() in content or state.lower() in source:
                    filtered_docs.append(doc)
        else:
            # Non-US questions should skip RAG
            filtered_docs = []

        # RAG path
        if filtered_docs:
            chain = load_qa_chain(llm, chain_type="stuff", prompt=custom_prompt)
            answer = chain.run(input_documents=filtered_docs, question=question)
            result = {"result": answer, "source_documents": filtered_docs}
        else:
            # Direct LLM answer (no documents used)
            result = {"source_documents": []}
            formatted_question = generic_prompt.format(question=question)
            answer = llm.invoke(formatted_question).content

        # Retry if response is unhelpful
        if "i don't know" in answer.lower() or len(answer.strip()) < 40:
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
>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62

        # Add curated law link if available
        curated_link = get_reference_link(question)
        if curated_link:
<<<<<<< HEAD
            answer += (
                f"\n\n🔗 For more info, see: {curated_link}"
            )
=======
            answer += f"\n\n🔗 For more info, see: {curated_link}"
>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62

        return answer

    except Exception as e:
<<<<<<< HEAD
        return f"❌ Error: {e}"
=======
        print(f"Error in get_legal_answer: {e}")
        return (
            "We weren’t able to generate a response right now. Please try again later."
        )
>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62
