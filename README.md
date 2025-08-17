# Document Chatbot

A web-based chatbot that answers questions based on uploaded documents (CSV, DOCX, PDF) and CMS content using vector embeddings stored in Qdrant.

## Features

- Pop-out chatbot on a website with responsive design.
- Upload documents for analysis.
- Ask questions and receive answers based on document and CMS content.
- Vector search powered by Qdrant and `sentence-transformers/all-MiniLM-L6-v2`.

## Tech Stack

**Frontend:** HTML, CSS, JavaScript  
**Backend:** Python, FastAPI  
**NLP/Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)  
**Vector Database:** Qdrant Cloud (free version)  
**File Parsing:** `python-docx`, `pdfminer.six`, `pandas`

## Project Structure

project/
│
├── frontend/
│ ├── index.html
│ ├── styles.css
│ └── chatbot.js
│
├── backend/
│ ├── app.py
│ ├── document_parser.py
│ ├── embeddings.py
│ ├── qdrant_utils.py
│ └── requirements.txt
│
└── README.md

## Setup Instructions

### 1. Qdrant Cloud

- Create a free Qdrant Cloud account.
- Create a new collection.
- Copy your **Cluster URL** and **API Key**.

```bash
$env:QDRANT_URL = "https://8055bedc-d3cd-4ecc-88f1-5e1ab5f26010.eu-west-2-0.aws.cloud.qdrant.io"
$env:QDRANT_API_KEY = "your-api-key"

```

2. Backend

cd backend
pip install -r requirements.txt
uvicorn app:app --reload

3. Frontend

Open frontend/index.html in a browser.

Chat with the bot and upload documents.

API Endpoints

POST /upload → Upload files (CSV, DOCX, PDF)

POST /ask → Ask a question

POST /import_cms → Import CMS content

Styling

Colors

- Chatbot Bubble: Sage Green (#7A9E7E)
- User Bubble: Beige / Eggshell (#F4F1E9)
- Background: Off-White (#FAF8F2)
- Primary Text: Dark Brown / Deep Gray (#413F3D)
- Accent (Buttons/Links): Terracotta (#E07A5F)

Notes

For development, CORS is allowed for all origins.

Ensure Qdrant credentials are set in your environment variables.

For production, secure your API keys and CORS settings.

Author

Gareth Mubaiwa – Intern / Developer / Data Scientist


app not fully working still in making and customization so needs editing

