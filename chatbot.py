"""RAG question-answering logic for MediGuide AI."""
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
VECTOR_DIR = Path("vectorstore")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

SYSTEM_PROMPT = """You are MediGuide AI, a healthcare information assistant.
Answer the user's question using ONLY the supplied context.
If the context does not contain the answer, say:
'I couldn't find this information in the available healthcare documents.'
Do not diagnose illnesses, prescribe medicines, recommend doses, or tell users
 to start/stop treatment. For personal medical concerns, advise consulting a
qualified healthcare professional. For severe or life-threatening symptoms,
advise contacting local emergency services. Keep answers clear and easy to understand.

Context:
{context}
"""


class HealthcareRAG:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here":
            raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")
        if not VECTOR_DIR.exists():
            raise FileNotFoundError("FAISS index not found. Run python ingest.py before starting the app.")
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
        self.vector_db = FAISS.load_local(
            str(VECTOR_DIR), embeddings, allow_dangerous_deserialization=True
        )
        self.retriever = self.vector_db.as_retriever(
            search_type="similarity", search_kwargs={"k": 4}
        )
        self.llm = ChatGroq(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            temperature=0.2,
            api_key=api_key,
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [("system", SYSTEM_PROMPT), ("human", "{question}")]
        )

    def ask(self, question: str):
        docs = self.retriever.invoke(question)
        if not docs:
            return "I couldn't find this information in the available healthcare documents.", []
        context = "\n\n".join(doc.page_content for doc in docs)
        response = self.llm.invoke(
            self.prompt.format_messages(context=context, question=question)
        )
        answer = response.content
        if isinstance(answer, list):
            answer = "\n".join(
                item.get("text", str(item)) if isinstance(item, dict) else str(item)
                for item in answer
            )
        sources = []
        for doc in docs:
            source = Path(doc.metadata.get("source", "Healthcare document")).name
            if source not in sources:
                sources.append(source)
        return str(answer), sources
