from langchain_ollama import ChatOllama

def chat_Ollama(prompt: str, modelo: str = "llama3.2") -> str:
    """Sends a prompt to the Ollama model and returns the response."""
    llm = ChatOllama(model=modelo)
    respuesta = llm.invoke(prompt)
    return respuesta.content

