"""
Kolkata Heritage Knowledge Bot - Streamlit App
"""

import streamlit as st
from src.rag_pipeline import KolkataHeritageRAG
from src.qwen_llm import QwenLLM


# Page config
st.set_page_config(
    page_title="Kolkata Heritage Bot",
    page_icon="🏛️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_rag():
    """Load RAG pipeline (cached)."""
    return KolkataHeritageRAG("vectorstore")


@st.cache_resource
def load_llm():
    """Load Qwen LLM (cached)."""
    return QwenLLM()


def main():
    # Header
    st.markdown("<h1 class='main-header'>🏛️ Kolkata Heritage Knowledge Bot</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Powered by Qwen 2.5 • RAG-based Q&A about Kolkata's heritage</p>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.markdown("""
        Ask questions about:
        - 🏛️ Landmarks (Victoria Memorial, Howrah Bridge)
        - 🎭 Culture (Durga Puja, Kalighat)
        - 📚 History (British Raj, Bengali Renaissance)
        - 🍛 Food & More!
        """)
        
        st.divider()
        
        # Demo questions
        st.subheader("Try asking:")
        demo_questions = [
            "Tell me about Victoria Memorial history",
            "When was Howrah Bridge built and who designed it?",
            "What is the significance of Durga Puja?",
            "Best time to visit Marble Palace?",
            "Who was Rabindranath Tagore?",
        ]
        
        for dq in demo_questions:
            if st.button(dq, key=f"demo_{dq[:20]}"):
                st.session_state["demo_query"] = dq
    
    # Check if vectorstore exists
    try:
        rag = load_rag()
        llm = load_llm()
    except Exception as e:
        st.error(f"""
        ❌ Could not load the RAG system: {e}
        
        **Setup steps:**
        1. Run `python scripts/collect_data.py` to collect data
        2. Run `python scripts/build_vectorstore.py` to build embeddings
        3. Make sure Ollama is running: `ollama serve`
        4. Pull Qwen model: `ollama pull qwen2.5:7b`
        """)
        return
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    
    # Display chat history
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "sources" in msg:
                with st.expander("📚 Sources"):
                    st.write(msg["sources"])
    
    # Handle demo query
    if "demo_query" in st.session_state:
        st.session_state["user_query"] = st.session_state["demo_query"]
        del st.session_state["demo_query"]
    
    # Chat input
    if query := st.chat_input("Ask about Kolkata heritage...") or st.session_state.get("user_query"):
        user_query = query
        if "user_query" in st.session_state:
            del st.session_state["user_query"]
        
        # Add user message
        st.session_state["messages"].append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Retrieve relevant documents
                    texts, sources = rag.retrieve(user_query, k=3)
                    context = "\n\n".join(texts)
                    
                    # Generate response with Qwen
                    response = llm.generate(user_query, context)
                    
                    st.write(response)
                    
                    # Show sources
                    sources_text = rag.get_formatted_sources(sources)
                    with st.expander("📚 Sources"):
                        st.write(sources_text)
                        for i, src in enumerate(sources, 1):
                            st.caption(f"{i}. {src.get('title', 'Unknown')} - {src.get('section', 'Overview')}")
                    
                    # Save to history
                    st.session_state["messages"].append({
                        "role": "assistant",
                        "content": response,
                        "sources": sources_text
                    })
                    
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.info("Make sure Ollama is running and Qwen model is pulled.")


if __name__ == "__main__":
    main()
