# MediGuide AI — Healthcare RAG Chatbot

MediGuide AI is a Retrieval-Augmented Generation (RAG) chatbot for general healthcare education. It retrieves relevant passages from a local healthcare knowledge base and uses a Groq-hosted language model to generate grounded responses.

> **Disclaimer:** This educational project does not diagnose conditions, prescribe medicines or replace advice from a qualified healthcare professional.

## Features

- Loads healthcare PDF, TXT and Markdown documents from `data/`.
- Splits source documents into overlapping chunks.
- Creates semantic embeddings with Hugging Face Sentence Transformers.
- Stores and searches vectors using FAISS.
- Retrieves relevant passages for each question.
- Generates context-grounded answers using Groq.
- Provides a Streamlit chat interface and displays retrieved source filenames.
- Instructs the assistant to acknowledge when the knowledge base does not contain an answer.

## RAG Architecture

```text
Healthcare PDF / TXT / Markdown files
              |
        Document Loading
              |
         Text Splitting
       (1000 / 200 overlap)
              |
    Hugging Face Embeddings
              |
       FAISS Vector Store
              |
      Similarity Retriever
              |
       Retrieved Context
              |
          Groq LLM
              |
      Grounded Answer
              |
        Streamlit UI
```

## Tech Stack

- Python and Streamlit
- LangChain
- Hugging Face Sentence Transformers (`sentence-transformers/all-MiniLM-L6-v2`)
- FAISS vector database
- Groq API

## Project Structure

```text
MediGuide-AI/
├── app.py
├── chatbot.py
├── ingest.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── data/
│   └── healthcare_guide.txt
└── vectorstore/       # generated locally; not committed
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/sushmaasree/MediGuide-AI.git
cd MediGuide-AI
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\\Scripts\\activate
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your Groq API key

Copy `.env.example` to `.env` and replace the placeholder with your own key:

```env
GROQ_API_KEY=your_actual_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

Create a key at https://console.groq.com/keys. Never commit `.env` or publish API keys.

### 5. Add documents and build the vector database

The repository includes a starter healthcare text knowledge base. You can add trusted healthcare PDFs or text files inside `data/`.

```bash
python ingest.py
```

The script creates a local `vectorstore/` directory containing the FAISS index.

### 6. Run the chatbot

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit, usually http://localhost:8501.

## Example Questions

- What does WHO recommend for fruit and vegetable intake?
- How much physical activity is recommended for adults?
- Why is second-hand tobacco smoke harmful?
- What is a healthy diet?

## Data Sources

The included knowledge-base notes summarize general educational information from these World Health Organization resources:

- Healthy diet: https://www.who.int/news-room/fact-sheets/detail/healthy-diet
- Physical activity: https://www.who.int/news-room/fact-sheets/detail/physical-activity
- Tobacco: https://www.who.int/news-room/fact-sheets/detail/tobacco

Refer to the original WHO pages for current guidance and full details. The included text is a compact educational summary, not a substitute for the source publications.

## Limitations

- Responses depend on the documents in `data/`.
- Retrieval quality depends on document quality and chunking.
- A working Groq API key and internet connection are required for answer generation.
- The first run may download the embedding model.
- Rebuild the local FAISS index after changing source documents.

## Future Enhancements

- Add more official healthcare PDFs.
- Display page-level citations for PDF sources.
- Add multilingual question answering.
- Deploy the Streamlit application.

## License

For educational and demonstration purposes. Check the terms of each external source before redistributing its content.
