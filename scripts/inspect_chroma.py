import os
import chromadb
from dotenv import load_dotenv, find_dotenv

# 1. Load environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# 2. Resolve ChromaDB path
PROJECT_ROOT = os.path.dirname(dotenv_path)
raw_chroma_path = os.getenv("CHROMA_PATH", "./chroma_data")
full_path = os.path.join(PROJECT_ROOT, raw_chroma_path)
LOCKED_CHROMA_PATH = os.path.abspath(full_path)


def inspect_database():
    print(f"🔗 Connecting to ChromaDB at: {LOCKED_CHROMA_PATH}")
    client = chromadb.PersistentClient(path=LOCKED_CHROMA_PATH)

    try:
        collection = client.get_collection(name="tarantula_docs")
    except Exception as e:
        print(f"❌ Could not find collection 'tarantula_docs': {e}")
        return

    # Fetch all stored data
    data = collection.get(include=["documents", "metadatas"])
    ids = data["ids"]
    documents = data["documents"]
    metadatas = data["metadatas"]

    print(f"\n📊 Total Chunks in Database: {len(ids)}\n")
    print("-" * 50)

    # Print out each chunk's details
    chunk_data = enumerate(zip(ids, documents, metadatas))
    for idx, (chunk_id, doc, meta) in chunk_data:
        print(f"[{idx + 1}] ID: {chunk_id}")
        print(f"Metadata: {meta}")
        # Print a short snippet of the text preview
        preview = doc[:150].replace("\n", " ")
        print(f"Snippet: {preview}...")
        print("-" * 50)


if __name__ == "__main__":
    inspect_database()
