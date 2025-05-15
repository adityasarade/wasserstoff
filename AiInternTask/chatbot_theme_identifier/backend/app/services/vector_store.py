import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from typing import List, Dict

# Paths for vector store and metadata
VECTOR_STORE_DIR = "data/vector_store"
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "index.faiss")
META_PATH = os.path.join(VECTOR_STORE_DIR, "metadata.pkl")

# Embedding model
EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts: List[str]):
    """
    Encode a list of texts into embeddings.
    """
    return EMBED_MODEL.encode(texts, convert_to_numpy=True)

def save_vector_store(chunks: List[Dict]):
    """
    Create or overwrite the FAISS index with provided sentence chunks and metadata.
    """
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embed_texts(texts)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(chunks, f)

def load_vector_store():
    """
    Load the FAISS index and associated metadata.
    """
    if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
        return None, None

    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def store_embeddings(new_chunks: List[Dict]):
    """
    Incrementally add new sentence chunks to the existing FAISS index.
    """
    new_texts = [chunk["text"] for chunk in new_chunks]
    new_vectors = embed_texts(new_texts)

    index, existing_chunks = load_vector_store()

    if index is None:
        index = faiss.IndexFlatL2(new_vectors.shape[1])
        existing_chunks = []

    index.add(new_vectors)
    all_chunks = existing_chunks + new_chunks

    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(all_chunks, f)

def search(query: str, top_k: int = 5) -> List[Dict]:
    """
    Searches the FAISS index and returns top_k most relevant and informative chunks.
    Preference is given to longer chunks with higher semantic relevance.
    """
    index, chunks = load_vector_store()
    if index is None or not chunks:
        return []

    query_vector = embed_texts([query])
    distances, indices = index.search(query_vector, top_k * 3)  # Fetch more to rerank

    # Gather candidate chunks with distance info
    results = []
    for i, dist in zip(indices[0], distances[0]):
        if i < len(chunks):
            chunk = chunks[i]
            chunk["similarity_score"] = float(dist)
            chunk["text_length"] = len(chunk["text"])
            results.append(chunk)

    # Rerank: prioritize longer, more meaningful chunks
    results = sorted(results, key=lambda x: (x["text_length"], -x["similarity_score"]), reverse=True)

    return results[:top_k]