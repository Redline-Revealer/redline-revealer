import os
from dotenv import load_dotenv
from azure.storage.blob import ContainerClient
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

AZURE_CONN_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv(
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT"
)
AZURE_OPENAI_EMBEDDING_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

# Update your container name here
container_name = "legal-docs"

# Where to store downloaded PDFs locally
local_path = os.path.join("data", "blob_pdfs")
os.makedirs(local_path, exist_ok=True)

print("⬇️ Downloading PDFs from Azure Blob Storage...")
container_client = ContainerClient.from_connection_string(
    AZURE_CONN_STR, container_name
)

for blob in container_client.list_blobs():
    if blob.name.endswith(".pdf"):
        local_file = os.path.join(
            local_path,
            os.path.basename(blob.name)
        )
        blob_client = container_client.get_blob_client(blob.name)
        blob_data = blob_client.download_blob().readall()
        with open(local_file, "wb") as f:
            f.write(blob_data)
        print(f"✅ Downloaded: {blob.name}")

# Load and process PDFs
print("📄 Loading and splitting documents...")
docs = []
for filename in os.listdir(local_path):
    if filename.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(local_path, filename))
        docs.extend(loader.load())

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs = splitter.split_documents(docs)

# Build vector store using Azure OpenAI embeddings
print("🔎 Creating FAISS vector index with Azure OpenAI embeddings...")
embeddings = AzureOpenAIEmbeddings(
    azure_deployment=AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    openai_api_version=AZURE_OPENAI_API_VERSION,
)

vectorstore = FAISS.from_documents(split_docs, embeddings)

# Save index
index_path = os.path.join("data", "indexes", "legal_docs_index")
vectorstore.save_local(index_path)
print(f"✅ FAISS index saved at: {index_path}")
