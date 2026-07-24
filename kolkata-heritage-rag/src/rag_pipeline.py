"""
RAG Pipeline for Kolkata Heritage Knowledge Bot
"""

import chromadb
from typing import List, Tuple


class KolkataHeritageRAG:
    """RAG pipeline for Kolkata heritage Q&A."""
    
    def __init__(self, vectorstore_path: str = "vectorstore"):
        self.vectorstore_path = vectorstore_path
        self.client = None
        self.collection = None
        self._load_vectorstore()
    
    def _load_vectorstore(self):
        """Load ChromaDB vector store."""
        self.client = chromadb.PersistentClient(path=self.vectorstore_path)
        self.collection = self.client.get_collection("kolkata_heritage")
    
    def retrieve(self, query: str, k: int = 3) -> Tuple[List[str], List[dict]]:
        """
        Retrieve relevant documents for a query.
        
        Returns:
            - List of relevant text chunks
            - List of source metadata
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        
        texts = results["documents"][0] if results["documents"] else []
        sources = results["metadatas"][0] if results["metadatas"] else []
        
        return texts, sources
    
    def get_formatted_sources(self, sources: List[dict]) -> str:
        """Format sources for display."""
        formatted = []
        for i, src in enumerate(sources, 1):
            title = src.get("title", "Unknown")
            section = src.get("section", "")
            formatted.append(f"{i}. **{title}**{f' - {section}' if section else ''}")
        return "\n".join(formatted)


# Simple test
if __name__ == "__main__":
    rag = KolkataHeritageRAG()
    
    test_queries = [
        "Tell me about Victoria Memorial",
        "When was Howrah Bridge built?",
        "What is Durga Puja?",
    ]
    
    for query in test_queries:
        print(f"\nQ: {query}")
        texts, sources = rag.retrieve(query)
        print(f"Sources:\n{rag.get_formatted_sources(sources)}")
