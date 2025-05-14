
import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# Set paths
VECTOR_STORE_DIR = "data/vector_store"
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "index.faiss")
META_PATH = os.path.join(VECTOR_STORE_DIR, "docs.pkl")

# Use a lightweight, fast model
EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts):
    return EMBED_MODEL.encode(texts)

def save_vector_store(texts):
    vectors = embed_texts(texts)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(texts, f)

def load_vector_store():
    if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
        return None, None

    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        texts = pickle.load(f)
    return index, texts

def search(query, top_k=5):
    index, texts = load_vector_store()
    if index is None:
        return []

    query_vec = embed_texts([query])
    distances, indices = index.search(query_vec, top_k)
    return [texts[i] for i in indices[0]]

def store_embeddings(new_text):
    # Load existing store (or initialize)
    index, texts = load_vector_store()
    new_vec = embed_texts([new_text])

    if index is None:
        index = faiss.IndexFlatL2(new_vec.shape[1])
        texts = [new_text]
    else:
        index.add(new_vec)
        texts.append(new_text)

    # Save updated index and texts
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(texts, f)