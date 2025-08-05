from langchain_core.prompts import PromptTemplate

def build_prompt():
    return PromptTemplate(
        input_variables=["context", "input"],
        template="""Based on the following context, answer the user's question with a detailed and comprehensive final answer of approximately 300 words.

If you don't know the answer, just say that you don't know. Don't try to make up an answer.

{context}

Question: {input}

Detailed Answer:"""
    )
