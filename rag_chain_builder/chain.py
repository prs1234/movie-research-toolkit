import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from .prompt import build_prompt as get_prompt_template


load_dotenv()

def build_rag_chain(vectorindex):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        max_output_tokens=2048,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    prompt = get_prompt_template()
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vectorindex.as_retriever(search_kwargs={"k": 2})

    return create_retrieval_chain(retriever, document_chain)
