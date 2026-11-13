"""Load healthcare PDF/TXT files, split them, embed them and save a FAISS index."""
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

DATA_DIR = Path("data")
VECTOR_DIR = Path("vectorstore")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")


def load_documents():
    documents = []
    for path in DATA_DIR.rglob("*"):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            documents.extend(PyPDFLoader(str(path)).load())
        elif suffix in {".txt", ".md"}:
            documents.extend(TextLoader(str(path), encoding="utf-8").load())
    return documents


def main():
    if not DATA_DIR.exists():
        raise FileNotFoundError("Create the data/ folder and add healthcare PDF or TXT files.")
    documents = load_documents()
    if not documents:
        raise ValueError("No PDF, TXT or Markdown documents found inside data/.")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local(str(VECTOR_DIR))
    print(f"Loaded {len(documents)} document pages/files.")
    print(f"Created {len(chunks)} text chunks.")
    print(f"FAISS index saved to: {VECTOR_DIR.resolve()}")


if __name__ == "__main__":
    main()
