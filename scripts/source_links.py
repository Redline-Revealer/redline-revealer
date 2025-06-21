import os
import json
from azure.storage.blob import ContainerClient
from dotenv import load_dotenv

load_dotenv()

AZURE_BLOB_CONN_STR = os.getenv("AZURE_BLOB_CONN_STR")
AZURE_BLOB_CONTAINER = os.getenv("AZURE_BLOB_CONTAINER")
AZURE_BLOB_BASE_URL = os.getenv("AZURE_BLOB_BASE_URL")

# Connect to the container
container_client = ContainerClient.from_connection_string(
<<<<<<< HEAD
    conn_str=AZURE_BLOB_CONN_STR,
    container_name=AZURE_BLOB_CONTAINER
=======
    conn_str=AZURE_BLOB_CONN_STR, container_name=AZURE_BLOB_CONTAINER
>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62
)

# Generate mapping of {filename: public_url}
source_links = {}
for blob in container_client.list_blobs():
    if blob.name.endswith(".pdf"):
<<<<<<< HEAD
        source_links[os.path.basename(
            blob.name)] = f"{AZURE_BLOB_BASE_URL}/{blob.name}"
=======
        source_links[os.path.basename(blob.name)] = f"{AZURE_BLOB_BASE_URL}/{blob.name}"
>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62

# Save to JSON
os.makedirs("data", exist_ok=True)
with open("data/source_links.json", "w") as f:
    json.dump(source_links, f, indent=2)

print(f"Saved {len(source_links)} source links to data/source_links.json")
