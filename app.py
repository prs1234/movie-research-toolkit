
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

from langchain_google_genai import ChatGoogleGenerativeAI

# === Load .env ===
load_dotenv(r"D:\LLM projects\2_news_research_tool_project\movie_reasearch_toolkit_using_gemini\key.env")

INDEX_PATH = "faiss_index_store2.pkl"

# === Helper to rebuild index ===
def refresh_faiss_index():
    st.info("📥 Fetching new movie news and rebuilding FAISS index...")
    documents = load_documents()
    chunks = split_documents(documents)
    vectorindex = create_vector_index(chunks)
    save_vector_index(vectorindex, path=INDEX_PATH)
    st.success("✅ FAISS index updated.")
    return vectorindex

# === Gemini Summarizer for sidebar ===
def extract_key_points(answer_text):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        max_output_tokens=512,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    summarize_prompt = f"""
Please extract 3–5 key bullet points from the following answer:

{answer_text}

Format as:
- Point 1
- Point 2
- ...
"""
    response = llm.invoke(summarize_prompt)
    return response.content.strip()


def main():
    st.set_page_config(page_title="🎬 Movie Research Toolkit", layout="centered")
    st.title("🎬 Movie Research Toolkit with Gemini")

    # === FAISS Index Load or Refresh ===
    if "vectorindex" not in st.session_state:
        try:
            with st.spinner("🔍 Loading FAISS index..."):
                st.session_state.vectorindex = load_vector_index(INDEX_PATH)
                st.success("✅ Loaded existing FAISS index.")
        except FileNotFoundError:
            st.warning("⚠️ No index found, creating new one...")
            st.session_state.vectorindex = refresh_faiss_index()

    # === Manual Refresh Button ===
    if st.button("🔁 Refresh News and Rebuild Index"):
        st.session_state.vectorindex = refresh_faiss_index()

    # === Build RAG chain ===
    rag_chain = build_rag_chain(st.session_state.vectorindex)
    st.success("✅ RAG chain ready.")

    # === User Query ===
    st.markdown("### 🔎 Ask about recent movie news:")
    query = st.text_input("Enter your question")

    if st.button("Get Answer") and query:
        with st.spinner("💡 Generating answer..."):
            response = rag_chain.invoke({"input": query})
            full_answer = response["answer"]
            st.markdown("### 🧠 Answer:")
            st.write(full_answer)

        # Generate sidebar key points
        with st.spinner("📝 Extracting key points..."):
            key_points = extract_key_points(full_answer)
            st.sidebar.markdown("## 📌 Key Points")
            st.sidebar.markdown(key_points)

if __name__ == "__main__":
    main()
