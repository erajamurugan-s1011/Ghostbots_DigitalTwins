from sentence_transformers import SentenceTransformer
import chromadb
import uuid

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Persistent database
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="ghostbot_memory"
)


def store_text(text):

    # Remove extra spaces
    text = text.strip()

    if not text:
        return

    chunk_size = 500

    chunks = [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
    ]

    for chunk in chunks:

        collection.add(
            documents=[chunk],
            ids=[str(uuid.uuid4())]
        )

        print("\nStored:")
        print(chunk[:100])


def search_text(query):

    results = collection.query(
        query_texts=[query],
        n_results=2
    )

    print("\nQuestion:", query)
    print("Results:", results)

    if (
        "documents" in results
        and results["documents"]
        and len(results["documents"][0]) > 0
    ):
        return " ".join(results["documents"][0])

    return ""