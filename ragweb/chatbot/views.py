from django.shortcuts import render

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama

DB_PATH = "../vectorstore"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)

llm = Ollama(model="phi3:mini")


def chat(request):
    answer = ""

    if request.method == "POST":
        question = request.POST.get("question")

        docs = db.similarity_search(question, k=3)

        context = ""
        for doc in docs:
            context += doc.page_content + "\n"

        prompt = f"""
Answer only using the context below.

Context:
{context}

Question:
{question}
"""

        answer = llm.invoke(prompt)

    return render(request, "chat.html", {"answer": answer})
