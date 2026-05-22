import os

from crewai import LLM
from crewai.project import llm

def get_llm(api_key: str, provider: str):
    """
    Instantiates Cloud providers if keys exist, otherwise defaults cleanly to Ollama.
    """
    if provider == "openai" and api_key:
        return LLM(
            model="openai/gpt-4o-mini",
            api_key= api_key
        )
        
    elif provider == "anthropic" and api_key:
        return LLM(
            model="anthropic/claude-3-5-haiku-latest",
            api_key=api_key
        )
        
    elif provider == "groq" and api_key:
        return LLM(
            model="groq/llama-3.1-8b-instant",
            api_key=api_key
        )
        
    else:
        # Captures your custom 'MODEL' env var
        local_model_name = os.getenv("MODEL")
        
        print(f"[LOCAL RUN] Defaulting to local Ollama framework with model: {local_model_name}")
        
        # CrewAI routes local models using the 'ollama/model_name' string syntax
        return LLM(
            model=f"{os.getenv('PROVIDER')}/{local_model_name}",
            base_url=os.getenv("API_BASE") # Points directly to your local machine port
        )
        