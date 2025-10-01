import torch
from sentence_transformers import SentenceTransformer, util
import os
from openai import OpenAI

# Function to open a file and return its contents as a string
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Function to get relevant context from the vault based on user input
def get_relevant_context(user_input, vault_embeddings, vault_content, model, top_k=3):
    if vault_embeddings.nelement() == 0:  # Check if the tensor has any elements
        return []
    # Encode the user input
    input_embedding = model.encode([user_input])
    # Compute cosine similarity between the input and vault embeddings
    cos_scores = util.cos_sim(input_embedding, vault_embeddings)[0]
    # Adjust top_k if it's greater than the number of available scores
    top_k = min(top_k, len(cos_scores))
    # Sort the scores and get the top-k indices
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    # Get the corresponding context from the vault
    relevant_context = [vault_content[idx].strip() for idx in top_indices]
    return relevant_context


# def load_vault_and_embeddings(vault_path="vault.txt", model_name="paraphrase-multilingual-MiniLM-L6-v2"):
#     model = SentenceTransformer(model_name)
#     vault_content = []
#     if os.path.exists(vault_path):
#         with open(vault_path, "r", encoding="utf-8") as vault_file:
#             vault_content = vault_file.readlines()
#     vault_embeddings = model.encode(vault_content) if vault_content else []
#     vault_embeddings_tensor = torch.tensor(vault_embeddings)
#     return model, vault_content, vault_embeddings_tensor