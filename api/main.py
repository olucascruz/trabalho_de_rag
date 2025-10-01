from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from .app.chat_backend import chat
from .app.db.db import load_from_chromadb
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Domínios permitidos
    allow_credentials=True,  # Permitir envio de cookies
    allow_methods=["*"],  # Métodos HTTP permitidos
    allow_headers=["*"],  # Cabeçalhos permitidos
)
class PromptRequest(BaseModel):
    prompt: str

@app.post("/prompt/")
async def protected_route(request: PromptRequest):
    # Rag
    rag_results = load_from_chromadb(request.prompt)

    # response = chat(request.prompt, rag_results)
    
    return {"message": rag_results}