# Kolkata Heritage Knowledge Bot

A RAG-based chatbot powered by Qwen that answers questions about Kolkata's heritage, landmarks, history, and culture.

## Quick Start

```bash
# 1. Install Ollama and pull Qwen model
ollama pull qwen2.5:7b

# 2. Setup virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Collect data (see DATA_SOURCES.md)
python scripts/collect_data.py

# 5. Build vector store
python scripts/build_vectorstore.py

# 6. Run the app
streamlit run app.py
```

## Project Structure

```
kolkata-heritage-rag/
├── app.py                 # Streamlit UI
├── src/
│   ├── rag_pipeline.py    # RAG logic
│   └── qwen_llm.py        # Qwen integration
├── scripts/
│   ├── collect_data.py    # Data scraper
│   └── build_vectorstore.py
├── data/
│   ├── raw/               # Raw scraped content
│   └── processed/         # Chunked documents
├── vectorstore/           # ChromaDB storage
└── DATA_SOURCES.md        # Heritage data sources
```

## Features

- ✅ Q&A about Kolkata landmarks (Victoria Memorial, Howrah Bridge, etc.)
- ✅ Source citations for every answer
- ✅ Powered by Qwen 2.5
- ✅ Multi-language support (English + Bengali)

## Demo Questions

- "Tell me about Victoria Memorial history"
- "When was Howrah Bridge built?"
- "What is the significance of Durga Puja in Kolkata?"
- "Who designed the Indian Museum?"
- "Best time to visit Marble Palace?"
