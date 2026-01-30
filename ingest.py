from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

PDF_PATH = "data"
DB_PATH = "vectorstore"

docs = []

for file in os.listdir(PDF_PATH):
    if file.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(PDF_PATH, file))
        docs.extend(loader.load())

print(f"Loaded {len(docs)} pages")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = FAISS.from_documents(docs, embeddings)
db.save_local(DB_PATH)

print("Vector DB created successfully!")
