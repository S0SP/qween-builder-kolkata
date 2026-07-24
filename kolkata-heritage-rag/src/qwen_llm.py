"""
Qwen LLM Integration via Ollama
"""

import ollama
from typing import Generator, Optional


class QwenLLM:
    """Qwen 2.5 LLM wrapper using Ollama."""
    
    def __init__(self, model: str = "qwen2.5:7b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.client = ollama.Client(host=base_url)
        
        # Test connection
        try:
            self.client.list()
            print(f"✅ Connected to Ollama at {base_url}")
        except Exception as e:
            print(f"⚠️  Could not connect to Ollama: {e}")
            print("   Make sure Ollama is running: ollama serve")
    
    def generate(self, prompt: str, context: str = "") -> str:
        """Generate a response from Qwen."""
        full_prompt = self._build_prompt(prompt, context)
        
        response = self.client.generate(
            model=self.model,
            prompt=full_prompt,
            options={
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 1024
            }
        )
        
        return response["response"]
    
    def generate_stream(self, prompt: str, context: str = "") -> Generator[str, None, None]:
        """Stream a response from Qwen."""
        full_prompt = self._build_prompt(prompt, context)
        
        for chunk in self.client.generate(
            model=self.model,
            prompt=full_prompt,
            stream=True,
            options={
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 1024
            }
        ):
            yield chunk["response"]
    
    def _build_prompt(self, question: str, context: str) -> str:
        """Build the full prompt with context."""
        return f"""You are a knowledgeable guide about Kolkata's heritage, history, and culture. 
Use the following context to answer the question. If you don't know the answer, say so honestly.
Always provide helpful, accurate information based on the context.

=== CONTEXT ===
{context}

=== QUESTION ===
{question}

=== ANSWER ===
"""


# Simple test
if __name__ == "__main__":
    llm = QwenLLM()
    
    print("Testing Qwen LLM...")
    response = llm.generate("What is Kolkata known for?")
    print(response)
