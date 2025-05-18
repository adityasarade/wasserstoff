import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from app.config import params

# Paths for vector store and metadata
VECTOR_STORE_DIR = params["paths"]["vector_store_dir"]
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, params["paths"]["index_file"])
META_PATH = os.path.join(VECTOR_STORE_DIR, params["paths"]["metadata_file"])

# Embedding model
EMBED_MODEL = SentenceTransformer(params["embedding"]["model_name"])

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

def search(query: str, top_k: int = 5, doc_ids: List[str] = None) -> List[Dict]:
    """
    Searches the FAISS index and returns top_k most relevant and informative chunks.
    If doc_ids is provided, only considers chunks from those documents.
    Preference is given to longer chunks with higher semantic relevance.
    """
    index, chunks = load_vector_store()
    if index is None or not chunks:
        return []

    # fetch extra candidates so we can rerank/filter later
    multiplier = params["search"]["initial_top_k_multiplier"]
    query_vector = embed_texts([query])
    distances, indices = index.search(query_vector, top_k * multiplier)

    # Gather candidate chunks with distance info
    results = []
    for i, dist in zip(indices[0], distances[0]):
        if i < len(chunks):
            chunk = chunks[i].copy()
            chunk["similarity_score"] = float(dist)
            chunk["text_length"] = len(chunk["text"])
            results.append(chunk)

    # If user passed a list of doc_ids, filter out others
    if doc_ids:
        results = [c for c in results if c["doc_id"] in doc_ids]

     # Filter out chunks below the minimum word threshold
    min_words = params["search"]["chunk_min_words"]
    results = [c for c in results if len(c["text"].split()) >= min_words]
     
    # Rerank: prioritize longer, more meaningful chunks
    results = sorted(
        results,
        key=lambda x: (x["text_length"], -x["similarity_score"]),
        reverse=True
    )

    return results[:top_k]