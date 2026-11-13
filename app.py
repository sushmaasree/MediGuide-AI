"""Streamlit user interface for MediGuide AI."""
import streamlit as st
from chatbot import HealthcareRAG

st.set_page_config(page_title="MediGuide AI", page_icon="🏥", layout="centered")
st.title("🏥 MediGuide AI")
st.subheader("Healthcare Information Assistant")
st.write("Ask general healthcare questions and get answers grounded in this project's healthcare documents.")
st.info("Educational use only. MediGuide AI does not diagnose conditions, prescribe medicines or replace a qualified healthcare professional.")

@st.cache_resource
def get_chatbot():
    return HealthcareRAG()

try:
    bot = get_chatbot()
except Exception as error:
    st.error(f"Chatbot setup issue: {error}")
    st.markdown("Check README.md, add your Groq API key to .env, and run python ingest.py.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("About")
    st.write("MediGuide AI uses Retrieval-Augmented Generation (RAG).")
    st.markdown("**Pipeline**\n1. Document loading\n2. Text splitting\n3. Hugging Face embeddings\n4. FAISS vector search\n5. Groq LLM response")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            st.caption("Sources: " + ", ".join(message["sources"]))

question = st.chat_input("Ask about healthy eating, activity, tobacco...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Searching the healthcare knowledge base..."):
            try:
                answer, sources = bot.ask(question)
                st.markdown(answer)
                if sources:
                    st.caption("Retrieved from: " + ", ".join(sources))
            except Exception as error:
                answer = f"Sorry, I couldn't complete the request: {error}"
                sources = []
                st.error(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
