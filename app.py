# import os
# import pickle
# import streamlit as st
# from dotenv import load_dotenv

# from rag_chain_builder import (
#     load_documents,
#     split_documents,
#     create_vector_index,
#     save_vector_index,
#     load_vector_index,
#     build_rag_chain
# )

# # === Load .env ===
# load_dotenv(r"D:\LLM projects\2_news_research_tool_project\movie_reasearch_toolkit_using_gemini\key.env")

# def main():
#     st.set_page_config(page_title="🎬 Movie Research Toolkit", layout="centered")
#     st.title("🎬 Movie Research Toolkit with Gemini")
    
#     index_path = "faiss_index_store2.pkl"

#     with st.spinner("🔍 Loading FAISS index..."):
#         try:
#             vectorindex = load_vector_index(index_path)
#             st.success("✅ Loaded existing FAISS index.")
#         except FileNotFoundError:
#             st.warning("📥 No existing index found. Creating new one...")
#             documents = load_documents()
#             chunks = split_documents(documents)
#             vectorindex = create_vector_index(chunks)
#             save_vector_index(vectorindex, path=index_path)
#             st.success("✅ New FAISS index created and saved.")

#     rag_chain = build_rag_chain(vectorindex)
#     st.success("✅ RAG chain ready.")

#     st.markdown("### 🔎 Ask about recent movie news:")
#     query = st.text_input("Enter your question")

#     if st.button("Get Answer") and query:
#         with st.spinner("💡 Generating answer..."):
#             response = rag_chain.invoke({"input": query})
#             st.markdown("### 🧠 Answer:")
#             st.write(response["answer"])

# if __name__ == "__main__":
#     main()
import os
import pickle
import streamlit as st
from dotenv import load_dotenv

from rag_chain_builder import (
    load_documents,
    split_documents,
    create_vector_index,
    save_vector_index,
    load_vector_index,
    build_rag_chain
)

# === Load .env ===
load_dotenv(r"D:\LLM projects\2_news_research_tool_project\movie_reasearch_toolkit_using_gemini\key.env")

INDEX_PATH = "faiss_index_store2.pkl"

# === Helper to refresh and rebuild index ===
def refresh_faiss_index():
    st.info("📥 Fetching new movie news and rebuilding FAISS index...")
    documents = load_documents()
    chunks = split_documents(documents)
    vectorindex = create_vector_index(chunks)
    save_vector_index(vectorindex, path=INDEX_PATH)
    st.success("✅ FAISS index updated.")
    return vectorindex

def main():
    st.set_page_config(page_title="🎬 Movie Research Toolkit", layout="centered")
    st.title("🎬 Movie Research Toolkit with Gemini")

    # === FAISS Index Loading ===
    if "vectorindex" not in st.session_state:
        try:
            with st.spinner("🔍 Loading FAISS index..."):
                st.session_state.vectorindex = load_vector_index(INDEX_PATH)
                st.success("✅ Loaded existing FAISS index.")
        except FileNotFoundError:
            st.warning("⚠️ No index found, creating new one...")
            st.session_state.vectorindex = refresh_faiss_index()

    # === Manual Refresh ===
    if st.button("🔁 Refresh News and Rebuild Index"):
        st.session_state.vectorindex = refresh_faiss_index()

    # === RAG Chain ===
    rag_chain = build_rag_chain(st.session_state.vectorindex)
    st.success("✅ RAG chain ready.")

    # === User Input ===
    st.markdown("### 🔎 Ask about recent movie news:")
    query = st.text_input("Enter your question")

    if st.button("Get Answer") and query:
        with st.spinner("💡 Generating answer..."):
            response = rag_chain.invoke({"input": query})
            st.markdown("### 🧠 Answer:")
            st.write(response["answer"])

if __name__ == "__main__":
    main()
