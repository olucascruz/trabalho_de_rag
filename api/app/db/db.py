from sentence_transformers import SentenceTransformer, util
import chromadb
import os
# Dados de exemplo

def save_to_chromadb():
    document_path = "document.txt"
    document_content = []
    if os.path.exists(document_path):
        with open(document_path, "r", encoding="utf-8") as vault_file:
            document_content = vault_file.readlines()
    else:
        print("Arquivo document.txt não encontrado.")
        return

    if not document_content:
        print("Nenhum conteúdo encontrado em document.txt.")
        return

    ids_documentos = [f"doc_{i}" for i in range(len(document_content))]
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    embeddings_documentos = model.encode(document_content).tolist()
    client_db = chromadb.PersistentClient(path="./meu_banco_vetorial")
    collection = client_db.get_or_create_collection(name="doc_rag")
    collection.add(
        embeddings=embeddings_documentos,
        documents=document_content,
        ids=ids_documentos
    )

    print(collection.count())
    docs = collection.get()
    if 'documents' in docs:
        for doc in docs['documents']:
            print(doc)
    else:
        print("Nenhum documento encontrado na coleção.")

def load_from_chromadb(query_texto):
    client_db = chromadb.PersistentClient(path="./meu_banco_vetorial")
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    query_embedding = model.encode([query_texto]).tolist()
    collection = client_db.get_or_create_collection(name="doc_rag")

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )
    return results
