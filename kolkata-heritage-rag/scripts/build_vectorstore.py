#!/usr/bin/env python3
"""
Build vector store for Kolkata Heritage RAG
Creates ChromaDB embeddings from collected data
"""

import json
import os
from pathlib import Path
import chromadb


def load_documents(data_dir: str) -> list[dict]:
    """Load documents from JSON files."""
    documents = []
    data_path = Path(data_dir)
    
    # Load combined file if exists
    combined_file = data_path.parent / "combined_data.json"
    if combined_file.exists():
        with open(combined_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for item in data:
            # Main content
            documents.append({
                "content": item["content"],
                "metadata": {
                    "source": item["source"],
                    "title": item["title"],
                    "url": item["url"],
                    "section": "overview"
                }
            })
            
            # Sections
            for section in item.get("sections", []):
                documents.append({
                    "content": section["content"],
                    "metadata": {
                        "source": item["source"],
                        "title": item["title"],
                        "url": item["url"],
                        "section": section["title"]
                    }
                })
    
    return documents


def split_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    """Simple text splitter without external dependencies."""
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        
        # Try to break at sentence boundary
        if end < text_length:
            last_period = chunk.rfind('. ')
            last_newline = chunk.rfind('\n')
            break_point = max(last_period, last_newline)
            if break_point > chunk_size // 2:
                chunk = chunk[:break_point + 1].strip()
                start = start + break_point + 1
            else:
                start = end
        else:
            chunks.append(chunk.strip())
            break
        
        if chunk.strip():
            chunks.append(chunk.strip())
    
    return chunks


def build_vectorstore(documents: list[dict], output_dir: str):
    """Build ChromaDB vector store with built-in embeddings."""
    print(f"Building vector store with {len(documents)} documents...")
    
    # Split documents into chunks
    all_chunks = []
    all_metadatas = []
    
    for doc in documents:
        chunks = split_text(doc["content"], chunk_size=500, chunk_overlap=50)
        for chunk in chunks:
            all_chunks.append(chunk)
            all_metadatas.append(doc["metadata"])
    
    print(f"Created {len(all_chunks)} chunks")
    
    # Create ChromaDB with persistent storage
    print("Creating ChromaDB vector store...")
    client = chromadb.PersistentClient(path=output_dir)
    
    # Get or create collection
    collection = client.get_or_create_collection(
        name="kolkata_heritage",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Clear existing data
    existing = collection.count()
    if existing > 0:
        print(f"Clearing {existing} existing chunks...")
        collection.delete(where={})
    
    # Add documents in batches
    batch_size = 100
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i + batch_size]
        batch_meta = all_metadatas[i:i + batch_size]
        
        collection.add(
            ids=[f"chunk_{i+j}" for j in range(len(batch))],
            documents=batch,
            metadatas=batch_meta
        )
        print(f"  Added {min(i + batch_size, len(all_chunks))}/{len(all_chunks)} chunks")
    
    print(f"\n✅ Vector store saved to: {output_dir}")
    print(f"📊 Total chunks: {len(all_chunks)}")
    print(f"📁 Collection: kolkata_heritage")
    
    return collection


if __name__ == "__main__":
    # Load documents
    docs = load_documents("data/raw")
    
    if not docs:
        print("❌ No documents found. Run 'python scripts/collect_data.py' first.")
        exit(1)
    
    # Build vector store
    build_vectorstore(docs, "vectorstore")
