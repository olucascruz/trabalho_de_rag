# Chat with an intelligent assistant in your terminal
from openai import OpenAI
from api.app.rag import get_relevant_context, load_vault_and_embeddings
# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

history = [
    {
    "role": "system",
    "content": "You are a helpful assistant specialized in providing information about a restaurant called Sabores do Amazonas, located in Manaus. Use the restaurant context provided (menu, ingredients, prices, hours, address, and recommendations) to answer questions accurately. Always provide clear, complete, and contextually relevant answers in Portuguese. When asked for food or drink suggestions, refer to the recommended combinations in the context. If a question is outside the context, politely indicate that you don't have that information."
    },
]

# Carrega modelo, conteúdo e embeddings do vault
model, vault_content, vault_embeddings = load_vault_and_embeddings()


def chat(history, vault_embeddings, vault_content, model):
    # Pega o último input do usuário
    user_input = history[-1]["content"]
    # Recupera contexto relevante
    relevant_context = get_relevant_context(user_input, vault_embeddings, vault_content, model)
    if relevant_context:
        context_str = "\n".join(relevant_context)
        # print("Context Pulled from Documents: \n\n" + context_str)
        # Adiciona contexto como mensagem system
        history.append({"role": "system", "content": f"Contexto relevante: {context_str}"})
    else:
        print("No relevant context found.")

    # Comunica com o modelo usando o histórico completo
    response = client.chat.completions.create(
        model="ollama-3.2",
        messages=history,
        temperature=0.7,
        stream=True,
    )
    return response



while True:
    # Comunicate with the model
    completion = chat(history, vault_embeddings, vault_content, model)


    # Keep response in a variable to add to history
    new_message = {"role": "assistant", "content": ""}
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)
    

    print()    # ...existing code...
    # Suponha que 'rag_context' seja o texto recuperado
    
    # ...existing code...
    history.append({"role": "user", "content": input("> ")})



