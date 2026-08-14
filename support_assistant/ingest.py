"""
Module 3 - Task 1: Document Ingestion and Embedding
Loads the 8 Zepto policy documents, treats each whole document as a single
chunk (acceptable per the spec since documents are short), generates local
embeddings with sentence-transformers (all-MiniLM-L6-v2), and stores them
in a persistent, queryable ChromaDB collection.

No API key, no external LLM, no network call to any LLM service.
"""

import os
from sentence_transformers import SentenceTransformer
import chromadb

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(SCRIPT_DIR, "docs")
CHROMA_DB_PATH = os.path.join(SCRIPT_DIR, "chroma_db")
COLLECTION_NAME = "zepto_policies"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


def load_documents():
    """
    Read every doc_XX.txt file in the docs folder.
    Returns a list of dicts, each with an id, the source filename, and the text.
    One chunk per document - acceptable since these documents are short.
    """
    documents = []
    filenames = sorted(f for f in os.listdir(DOCS_DIR) if f.endswith(".txt"))

    for filename in filenames:
        doc_id = filename.replace(".txt", "")  # e.g. "doc_01"
        filepath = os.path.join(DOCS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read().strip()
        documents.append({
            "id": doc_id,
            "source": filename,
            "text": text,
        })

    return documents


def main():
    print("Loading documents...")
    documents = load_documents()
    print(f"Loaded {len(documents)} documents: {[d['id'] for d in documents]}\n")

    print(f"Loading embedding model: {EMBEDDING_MODEL_NAME} (runs locally, no API)...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    print("Model loaded.\n")

    print("Generating embeddings for each document/chunk...")
    texts = [doc["text"] for doc in documents]
    embeddings = model.encode(texts).tolist()
    embedding_dimension = len(embeddings[0])
    print(f"Generated {len(embeddings)} embeddings, each of dimension {embedding_dimension}.\n")

    print(f"Connecting to persistent ChromaDB at ./{CHROMA_DB_PATH} ...")
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    # Fresh collection each run, so re-running this script doesn't duplicate entries
    existing_collections = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing_collections:
        client.delete_collection(COLLECTION_NAME)
        print(f"Removed existing '{COLLECTION_NAME}' collection to rebuild cleanly.")

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},  # required: doc specifies cosine similarity for retrieval
    )

    collection.add(
        ids=[doc["id"] for doc in documents],
        embeddings=embeddings,
        documents=[doc["text"] for doc in documents],
        metadatas=[{"source": doc["source"]} for doc in documents],
    )
    print(f"Stored {collection.count()} chunks in ChromaDB collection '{COLLECTION_NAME}'.\n")

    # --- Verification: run a test query to confirm the collection is queryable ---
    print("=" * 50)
    print("VERIFICATION")
    print("=" * 50)

    test_query = "How long do I have to return a damaged item?"
    query_embedding = model.encode([test_query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=1,
    )

    print(f"Test query: '{test_query}'")
    print(f"Top matching document ID: {results['ids'][0][0]}")
    print(f"Source: {results['metadatas'][0][0]['source']}")
    print(f"Matched text: {results['documents'][0][0][:100]}...")

    print(f"\nNumber of documents loaded: {len(documents)}")
    print(f"Number of chunks stored: {collection.count()}")
    print(f"Embedding dimension: {embedding_dimension}")
    print(f"Embedding model: {EMBEDDING_MODEL_NAME}")
    print(f"ChromaDB collection name: {COLLECTION_NAME}")


if __name__ == "__main__":
    main()