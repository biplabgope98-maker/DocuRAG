# DocuRAG - Document Question Answering System

### Cognizant NPN Hackathon - Team CODENOVA

DocuRAG is an AI-powered document question-answering application using **Retrieval-Augmented Generation (RAG)**. It allows users to upload PDF documents and images, search their content, and ask questions using AI.

---

## Features

### User

- User Registration and Login
- JWT Authentication
- PDF Upload
- Image Upload
- OCR for Scanned Documents
- Semantic Document Search
- AI-powered Question Answering
- Source and Page References
- Query History
- Query Caching

### Admin

- Separate Admin Login
- Admin Dashboard
- View and Manage Users
- Activate / Deactivate Users
- Delete Users
- View and Manage Documents
- Delete Documents
- View Processing Failures
- View and Manage Queries
- System Statistics

---

## Technologies Used

### Backend

- Python
- FastAPI
- Uvicorn
- SQLite
- PyMuPDF
- Pillow

### AI and RAG

- Google Gemini
- Google GenAI SDK
- Sentence Transformers
- FAISS
- Hybrid Search
- Vector Embeddings
- OCR

### Frontend

- Vue.js
- Vite
- JavaScript
- HTML
- CSS

### Authentication

- JWT
- bcrypt
- Role-based Authorization

---

## Project Structure

```text
DocuRAG-main/
├── backend/
│   ├── api/
│   │   ├── admin_api.py
│   │   ├── auth_api.py
│   │   ├── documents_api.py
│   │   └── rag_api.py
│   ├── routes/
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── documents.py
│   │   └── rag.py
│   ├── services/
│   │   ├── cache.py
│   │   ├── document_processor.py
│   │   ├── hybrid_search.py
│   │   ├── image_analyzer.py
│   │   ├── image_file_processor.py
│   │   ├── image_processor.py
│   │   ├── image_search.py
│   │   └── vector_store.py
│   ├── app.py
│   └── fastapi_app.py
├── database/
│   └── database.py
├── frontend/
│   └── src/
│       ├── App.vue
│       ├── main.js
│       └── style.css
├── vector_store/
│   ├── chunks.pkl
│   └── docurag.index
├── create_admin.py
├── requirements.txt
├── README.md
└── start_backend.bat


## User Roles

| Role | Description |
|------|-------------|
| **Admin** | Manage users, documents, queries, and system information |
| **User** | Upload documents and ask questions using the RAG system |

## Major Functionalities

- User Authentication
- Admin Authentication
- Role-based Authorization
- PDF Processing
- Image Processing
- OCR for Scanned Documents
- Text Chunking
- Text Embeddings
- FAISS Vector Search
- Hybrid Search
- Gemini-based Answer Generation
- Source and Page Retrieval
- Query History
- Query Caching
- Document Management
- User Management
- Query Management
- Processing Status Tracking

---

## RAG Workflow

The system follows a Retrieval-Augmented Generation workflow:

1. User uploads a PDF or image.
2. The document is processed and text is extracted.
3. Scanned documents are processed using OCR.
4. Extracted content is divided into chunks.
5. Chunks are converted into vector embeddings.
6. Embeddings are stored in the FAISS vector index.
7. The user submits a question.
8. Relevant document chunks are retrieved.
9. Retrieved context is provided to Gemini.
10. Gemini generates the answer.
11. Source and page information is returned to the user.

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd DocuRAG-main

### Backend Setup

Install the required Python packages:

```bash
pip install -r requirements.txt

Configure the required environment variables, including the Gemini API key.

Do not commit API keys or .env files to GitHub. 

### Frontend Setup

```bash
cd frontend
npm install

## Run the Project

### Start Backend

From the project root, run:

    uvicorn backend.fastapi_app:app --host 127.0.0.1 --port 8000 --reload

The backend will run at:

    http://127.0.0.1:8000

### API Documentation

FastAPI interactive API documentation is available at:

    http://127.0.0.1:8000/docs

### Start Backend Using Batch File

The backend can also be started using:

    start_backend.bat

### Start Frontend

Open another terminal and run:

    cd frontend
    npm run dev

Open the URL provided by Vite in the browser.

---

## Usage

### User

1. Create an account.
2. Log in to the application.
3. Upload a PDF or image.
4. Wait for the document to be processed.
5. Ask questions about the uploaded document.
6. View the generated answer.
7. Check the source and page references.
8. View previous queries when required.

### Admin

1. Open the admin login page.
2. Log in using an admin account.
3. Open the admin dashboard.
4. View system statistics.
5. Manage users.
6. Manage documents.
7. View processing failures.
8. View and manage queries.

---

## API Documentation

The project uses **FastAPI** for backend API services.

Interactive API documentation is available at:

    http://127.0.0.1:8000/docs

The documentation can be used to view and test the available API endpoints.

---

## Team

**Biplab Gope**



**Project:** DocuRAG