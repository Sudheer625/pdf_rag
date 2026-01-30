from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama

DB_PATH = "vectorstore"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)

llm = Ollama(model="phi3:mini")

print("PDF Chatbot Ready! Type 'exit' to quit.\n")

while True:
    query = input("You: ")

    if query.lower() == "exit":
        break

    docs = db.similarity_search(query, k=3)

    context = ""
    for doc in docs:
        context += doc.page_content + "\n"

    prompt = f"""
Answer the question only from the context below.

Context:
{context}

Question:
{query}
"""

    response = llm.invoke(prompt)
    print("\nBot:", response, "\n")
