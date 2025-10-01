from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def chat(prompt, relevant_context):
    default_history = history = [
    {
        "role": "system",
        "content": "You are a helpful assistant specialized in providing information about a restaurant called Sabores do Amazonas, located in Manaus. Use the restaurant context provided (menu, ingredients, prices, hours, address, and recommendations) to answer questions accurately. Always provide clear, complete, and contextually relevant answers in Portuguese. When asked for food or drink suggestions, refer to the recommended combinations in the context. If a question is outside the context, politely indicate that you don't have that information."
        },
    ]

    history = default_history
    if relevant_context:
        context_str = "\n".join(relevant_context)
        history.append({"role": "system", "content": f"Contexto relevante: {context_str}"})

    history.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model="ollama-3.2",
        messages=history,
        temperature=0.7,
        stream=False,
    )
    return response.choices[0].message.content