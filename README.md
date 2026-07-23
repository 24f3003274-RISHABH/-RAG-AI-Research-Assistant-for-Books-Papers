# AI Research Assistant for Books & Papers

A full-stack **Retrieval-Augmented Generation (RAG)** application that allows users to upload textbooks, notes, and research papers in PDF format, then ask questions and receive AI-generated answers grounded in the uploaded documents.

This project uses **HuggingFace embeddings**, **FAISS vector search**, and **Ollama (Llama 3)** to build a completely **free and local RAG system** without requiring OpenAI API credits.

---

## What is RAG?

**Retrieval-Augmented Generation (RAG)** is an AI architecture that combines **information retrieval** with **large language model (LLM) generation**.

Instead of relying only on the LLM’s pre-trained knowledge, RAG first retrieves the most relevant information from a custom knowledge base (in this case, uploaded PDFs) and then uses that information as context to generate accurate, source-grounded answers.

### RAG workflow

```text
User Query
    │
    ▼
Frontend (React Chat UI)
    │
    ▼
Backend (Node.js + Express)
    │
    ▼
Python RAG Engine
    │
    ├── Retrieve relevant chunks from FAISS
    │
    └── Send context + query to Ollama (Llama 3)
    │
    ▼
AI-generated answer
    │
    ▼
Frontend displays answer + references
```

### Why use RAG?

* **Accurate answers** based on your own books and papers.
* **Reduced hallucination** because the LLM uses retrieved context.
* **No need for internet-based APIs** when using local models.
* **Privacy-friendly** since PDFs and embeddings stay on your computer.

---

## System Architecture

```text
                ┌─────────────────────────┐
                │      React Frontend     │
                │   Upload PDFs & Chat UI │
                └────────────┬────────────┘
                             │ HTTP Requests
                             ▼
                ┌─────────────────────────┐
                │   Node.js + Express     │
                │  /upload and /query API │
                └────────────┬────────────┘
                             │ child_process
                             ▼
                ┌─────────────────────────┐
                │     Python RAG Engine   │
                │  PDF Loading & Chunking │
                └────────────┬────────────┘
                             │
         ┌───────────────────┴───────────────────┐
         ▼                                       ▼
┌──────────────────┐                   ┌──────────────────┐
│ HuggingFace      │                   │      FAISS       │
│ Embeddings       │                   │ Vector Database  │
└──────────────────┘                   └──────────────────┘
         │                                       │
         └───────────────────┬───────────────────┘
                             ▼
                ┌─────────────────────────┐
                │    Ollama (Llama 3)     │
                │   Answer Generation     │
                └─────────────────────────┘
```

---

## Technologies Used

### Frontend

* **React.js** – Interactive user interface.
* **Vite** – Fast development server and build tool.
* **Axios** – HTTP client for API communication.
* **CSS3** – Custom styling for the chat interface.

### Backend

* **Node.js** – JavaScript runtime environment.
* **Express.js** – REST API framework.
* **Multer** – PDF file upload handling.
* **Morgan** – HTTP request logging.
* **CORS** – Cross-origin request handling.

### RAG Engine (Python)

* **LangChain** – RAG pipeline orchestration.
* **PyPDF** – PDF text extraction.
* **Sentence Transformers** – HuggingFace embeddings.
* **FAISS** – Local vector database for semantic search.
* **Ollama** – Local LLM runtime.
* **Llama 3** – Large language model for answer generation.

### Optional Database

* **MongoDB** – Can be used for storing chat history, uploaded file metadata, and user sessions in future enhancements.

---

## Key Components Explained

### PDF Loading

The RAG engine reads all PDF files placed in `rag_engine/data/` using **PyPDFLoader**.

### Text Chunking

Large documents are split into smaller chunks (1000 characters with 200-character overlap) using **RecursiveCharacterTextSplitter**. This improves retrieval accuracy.

### Embedding Generation

Each text chunk is converted into a numerical vector using the **all-MiniLM-L6-v2** HuggingFace embedding model.

### FAISS Vector Store

FAISS stores all embeddings locally and performs **similarity search** to find the most relevant chunks for a user query.

### Retrieval

When a user asks a question, the system retrieves the **top-k most relevant chunks** from FAISS.

### Generation

The retrieved chunks are combined with the user query and sent to **Llama 3 via Ollama** to generate a contextual answer.

---

## Features

* Upload textbooks, notes, and research papers in PDF format.
* Automatic PDF text extraction and chunking.
* Free local embeddings using HuggingFace.
* Fast semantic search with FAISS.
* AI-generated answers using Ollama (Llama 3).
* Modern React-based chat interface.
* Automatic FAISS index rebuilding after PDF upload.
* REST API integration between frontend, backend, and Python RAG engine.
* Completely local and free — no OpenAI credits required.

---

## Project Structure

```text
AI-Research-Assistant/
│
├── backend/
│   ├── middleware/
│   │   ├── errorHandler.js
│   │   └── logger.js
│   ├── routes/
│   │   ├── query.js
│   │   └── upload.js
│   ├── uploads/
│   ├── package.json
│   └── server.js
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chatbot.jsx
│   │   │   ├── Results.jsx
│   │   │   └── UploadBooks.jsx
│   │   ├── App.css
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── rag_engine/
│   ├── data/
│   ├── vector_store/
│   ├── main.py
│   ├── requirements.txt
│   └── utils.py
│
├── .gitignore
└── README.md
```

---

## Local Setup Guide

### Prerequisites

Before running the project, install the following:

* **Python 3.10+**
* **Node.js 18+**
* **Git**
* **Ollama**

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Research-Assistant.git
cd AI-Research-Assistant
```

---

## Setup the RAG Engine

### Install Python Dependencies

```bash
cd rag_engine
pip install -r requirements.txt
```

### Install Ollama

Download Ollama from:

```text
https://ollama.com
```

### Download Llama 3 Model

```bash
ollama pull llama3
```

### Add PDF Files

Place your textbooks, notes, and research papers inside:

```text
rag_engine/data/
```

### Build the FAISS Vector Database

```bash
python main.py --build
```

Expected output:

```text
Loading PDFs...
Loaded 1550 pages
Created 3167 chunks
FAISS vector store created successfully!
```

---

## Setup the Backend

### Install Backend Dependencies

```bash
cd ../backend
npm install
```

### Start the Backend Server

```bash
npm start
```

The backend will run on:

```text
http://localhost:5000
```

---

## Setup the Frontend

### Install Frontend Dependencies

```bash
cd ../frontend
npm install
```

### Start the React Development Server

```bash
npm run dev
```

The frontend will run on:

```text
http://localhost:5173
```

---

## Running the Complete Application

1. Start **Ollama** and ensure Llama 3 is installed.
2. Start the **backend** using `npm start`.
3. Start the **frontend** using `npm run dev`.
4. Open `http://localhost:5173` in your browser.
5. Upload a PDF.
6. Ask questions related to the uploaded documents.
7. Receive AI-generated answers grounded in the PDF content.

---

## API Endpoints

### Upload PDF

**POST** `/upload`

Uploads a PDF file and rebuilds the FAISS vector index.

**Request:** `multipart/form-data`

| Field | Type | Description            |
| ----- | ---- | ---------------------- |
| pdf   | File | PDF document to upload |

**Response:**

```json
{
  "success": true,
  "message": "PDF uploaded and FAISS index rebuilt successfully!"
}
```

### Query the RAG System

**POST** `/query`

Sends a question to the RAG engine and returns an AI-generated answer.

**Request:**

```json
{
  "query": "What is normalization in DBMS?"
}
```

**Response:**

```json
{
  "success": true,
  "answer": "Normalization in DBMS is the process of organizing data..."
}
```

---

## Example Usage

### Query Example

**User Question:**

```text
What is the Indian Councils Act of 1861?
```

**RAG Process:**

1. FAISS retrieves the most relevant chunks from the uploaded Indian Polity PDF.
2. The chunks are sent as context to Llama 3.
3. Llama 3 generates a contextual answer based on the retrieved information.

---

## GitHub Ignore Rules

The project includes `.gitignore` files to exclude:

* `node_modules/`
* `dist/`
* Python virtual environments
* `__pycache__/`
* `.env` files
* `rag_engine/vector_store/`
* `rag_engine/data/`
* `backend/uploads/`

This keeps the repository lightweight and prevents sensitive files from being uploaded.

---

## Future Enhancements

* Store chat history in MongoDB.
* Add user authentication.
* Support multiple file formats (DOCX, TXT, PPTX).
* Add highlighted source references in answers.
* Implement streaming AI responses.
* Add document summarization.
* Deploy frontend on Vercel and backend on Render.
* Add Docker support for containerized deployment.

---

## Learning Outcomes

By building this project, you gain hands-on experience with:

* Retrieval-Augmented Generation (RAG)
* Vector databases and semantic search
* HuggingFace embeddings
* FAISS indexing and retrieval
* Ollama and local LLMs
* Full-stack development with React and Express
* Python backend integration
* REST API development

---

## Author

**Rishabh Keshari**

B.Tech Computer Science & Engineering | AI & Full Stack Developer

GitHub: https://github.com/24f3003274-RISHABH

---

## License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute this project for educational and personal purposes.

---

## Acknowledgements

* **Meta** for the Llama 3 model.
* **Ollama** for providing local LLM runtime support.
* **HuggingFace** for free embedding models.
* **FAISS** by Facebook AI Research for vector similarity search.
* **LangChain** for simplifying RAG pipeline development.

---

⭐ If you found this project useful, consider giving it a **star** on GitHub!
