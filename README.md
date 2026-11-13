# MediGuide AI

## Healthcare Information Assistant

MediGuide AI is a simple chatbot that answers general healthcare and nutrition questions using information stored in its healthcare knowledge base.

The project uses Retrieval-Augmented Generation (RAG). It searches the documents for information related to a user's question and sends the retrieved text to a language model to prepare an answer.

## Features

- Answers general healthcare, nutrition and fitness questions from the available documents.
- Uses a local FAISS vector database to search the knowledge base.
- Shows the source document used for an answer.
- Says when the requested information is not available in the documents.
- Includes a Streamlit chat interface.

## Technologies

- Python
- Streamlit
- LangChain
- Hugging Face Sentence Transformers
- FAISS
- Groq API

## How it works

1. Healthcare documents are placed in the `data/` folder.
2. `ingest.py` loads the documents and splits them into smaller text chunks.
3. Hugging Face creates embeddings for the chunks.
4. FAISS stores the embeddings for similarity search.
5. When a user asks a question, the app retrieves relevant text.
6. The Groq language model uses the retrieved text to generate an answer.
7. Streamlit displays the answer and source filename.

## Project files

- `app.py` – Streamlit interface.
- `chatbot.py` – retrieval and answer-generation logic.
- `ingest.py` – loads documents and builds the FAISS index.
- `data/healthcare_guide.txt` – healthcare information used by the chatbot.
- `requirements.txt` – Python dependencies.
- `.env.example` – example environment configuration.

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/sushmaasree/MediGuide-AI.git
cd MediGuide-AI
```

### 2. Create and activate a virtual environment

Windows:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install the packages

```bash
pip install -r requirements.txt
```

### 4. Set up the Groq API key

Create a file named `.env` in the project folder. Add your own Groq API key and a Groq model available to your account:

```env
GROQ_API_KEY=your_actual_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Get an API key from https://console.groq.com/keys. Do not upload your `.env` file or share your API key.

### 5. Build the knowledge base

```bash
python ingest.py
```

Run this again whenever you change the documents in `data/`.

### 6. Start the app

```bash
python -m streamlit run app.py
```

Open the local address shown in the terminal, usually http://localhost:8501.

## Example questions

- What does a balanced diet include?
- What are some vegetarian sources of protein?
- What are the benefits of eating bananas?
- How much physical activity is recommended for adults?
- Why is vitamin B12 important for vegetarians?

## Data sources

The healthcare guide contains short educational summaries and links to public health guidance, including:

- WHO healthy diet: https://www.who.int/news-room/fact-sheets/detail/healthy-diet
- WHO physical activity: https://www.who.int/news-room/fact-sheets/detail/physical-activity
- WHO tobacco: https://www.who.int/news-room/fact-sheets/detail/tobacco
- NHS vegetarian diet: https://www.nhs.uk/live-well/eat-well/how-to-eat-a-balanced-diet/the-vegetarian-diet/
- NIH vitamin C: https://ods.od.nih.gov/factsheets/VitaminC-Consumer/
- ICMR-NIN dietary guidelines: https://www.nin.res.in/downloads/DietaryGuidelinesforNINwebsite.pdf

## Limitations

This project provides general educational information only. It does not diagnose health conditions or prescribe medicines. Answers depend on the documents available in the knowledge base and should not replace advice from a qualified healthcare professional.
