from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def create_vector_index(docs):
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": False}  # ✅ Fix
    )
    return FAISS.from_documents(docs, embedding_model)

def save_vector_index(index, path="faiss_index_store2.pkl"):
    import pickle
    with open(path, "wb") as f:
        pickle.dump(index, f)

def load_vector_index(path="faiss_index_store2.pkl"):
    import pickle
    with open(path, "rb") as f:
        return pickle.load(f)
