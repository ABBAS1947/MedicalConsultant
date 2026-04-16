import streamlit as st
from src.components.pipeline import run_ingestion_pipeline
from src.components.retriever import get_retriever
from src.components.rag_chain import RAGChain

# Page Configuration
st.set_page_config(
    page_title="Medical Consultant AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-title {
        color: #1f77b4;
        text-align: center;
        margin-bottom: 30px;
    }
    .answer-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .source-box {
        background-color: #e8f4f8;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-title'>🏥 Medical Consultant AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Ask medical questions and get informed answers based on reliable sources</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("---")
    
    # Initialize session
    if "rag" not in st.session_state:
        with st.spinner("🔄 Initializing system..."):
            try:
                # Step 1: Ingest documents
                run_ingestion_pipeline()
                # Step 2: Load retriever
                retriever = get_retriever()
                # Step 3: Initialize RAG
                st.session_state.rag = RAGChain(retriever)
                st.success("✅ System ready!")
            except Exception as e:
                st.error(f"❌ Error initializing system: {str(e)}")
                st.stop()
    
    st.info("💡 Tips:\n- Ask specific medical questions\n- System uses provided documents\n- Sources are cited automatically")
    st.markdown("---")
    st.markdown("### About")
    st.markdown("**Version:** 1.0.0\n**Type:** RAG Medical Chatbot")

# Main Content
col1, col2 = st.columns([3, 1])

with col1:
    # Input
    st.subheader("📝 Your Question")
    query = st.text_area(
        "Ask a medical question:",
        placeholder="e.g., What are the symptoms of hypertension?",
        height=100,
        label_visibility="collapsed"
    )
    
    # Query button
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        submit_button = st.button("🔍 Search", use_container_width=True)
    with col_btn2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    with col_btn3:
        st.write("")  # Placeholder

with col2:
    st.subheader("📊 Stats")
    st.metric("Query Count", st.session_state.get("query_count", 0))

# Clear chat
if clear_button:
    st.session_state.query_count = 0
    st.rerun()

# Process query
if submit_button and query.strip():
    st.session_state.query_count = st.session_state.get("query_count", 0) + 1
    
    with st.spinner("⏳ Processing your question..."):
        try:
            result = st.session_state.rag.generate_response(query)
            
            # Display Answer
            st.markdown("---")
            st.subheader("💬 Answer")
            st.markdown(f"<div class='answer-box'>{result['answer']}</div>", unsafe_allow_html=True)
            
            # Display Sources
            if result['sources']:
                st.subheader("📚 Sources")
                for idx, source in enumerate(result['sources'], 1):
                    with st.markdown(f"<div class='source-box'>", unsafe_allow_html=True):
                        col_source = st.columns([3, 1])
                        with col_source[0]:
                            st.markdown(f"**{idx}. {source['source']}**")
                            st.caption(f"Page {source['page']}")
                        with col_source[1]:
                            st.write("")
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("⚠️ No sources found for this query.")
                
        except Exception as e:
            st.error(f"❌ Error processing query: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 12px;'>"
    "Medical Consultant AI | Built with LangChain, Ollama & Streamlit"
    "</p>",
    unsafe_allow_html=True
)
