import os
import json
from azure.storage.blob import ContainerClient
from dotenv import load_dotenv

load_dotenv()

AZURE_BLOB_CONN_STR = os.getenv("AZURE_BLOB_CONN_STR")
AZURE_BLOB_CONTAINER = os.getenv("AZURE_BLOB_CONTAINER")
AZURE_BLOB_BASE_URL = os.getenv("AZURE_BLOB_BASE_URL")

if not all([AZURE_BLOB_CONN_STR, AZURE_BLOB_CONTAINER, AZURE_BLOB_BASE_URL]):
    print("Error: Azure Blob Storage environment variables not set")
    exit(1)

# Connect to the container
container_client = ContainerClient.from_connection_string(
    conn_str=str(AZURE_BLOB_CONN_STR), container_name=str(AZURE_BLOB_CONTAINER)
)

# Generate mapping of {filename: public_url}
source_links = {}
for blob in container_client.list_blobs():
    if blob.name.endswith(".pdf"):
        source_links[os.path.basename(blob.name)] = f"{AZURE_BLOB_BASE_URL}/{blob.name}"

# Save to JSON
os.makedirs("data", exist_ok=True)
with open("data/source_links.json", "w") as f:
    json.dump(source_links, f, indent=2)

print(f"Saved {len(source_links)} source links to data/source_links.json")
