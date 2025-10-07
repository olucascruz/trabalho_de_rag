from sentence_transformers import SentenceTransformer, util
import chromadb
import os

client_db = chromadb.PersistentClient(path="./meu_banco_vetorial")
collection = client_db.get_or_create_collection("doc_rag")

print("Total de docs:", collection.count())
print("Docs:", collection.get()["documents"])

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

query_texto = "Quais sao as bebidas?"
query_embedding = model.encode([query_texto.lower()])
results = collection.query(
    query_embeddings=query_embedding,
    n_results=3
)

print(results)