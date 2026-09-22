DocuRAG - Document Question Answering System

Cognizant NPN Hackathon - Team CODENOVA

DocuRAG is an AI-powered document question-answering application using Retrieval-Augmented Generation (RAG). It allows users to upload PDF documents and images, search their content, and ask questions using AI.

Features

User

User Registration and Login

JWT Authentication

PDF Upload

Image Upload

OCR for Scanned Documents

Semantic Document Search

AI-powered Question Answering

Source and Page References

Query History

Query Caching

Admin

Separate Admin Login

Admin Dashboard

View and Manage Users

Activate / Deactivate Users

Delete Users

View and Manage Documents

Delete Documents

View Processing Failures

View and Manage Queries

System Statistics

Technologies Used

Backend

Python

FastAPI

Uvicorn

SQLite

PyMuPDF

Pillow

AI and RAG

Google Gemini

Google GenAI SDK

Sentence Transformers

FAISS

Hybrid Search

Vector Embeddings

OCR

Frontend

Vue.js

Vite

JavaScript

HTML

CSS

Authentication

JWT

bcrypt

Role-based Authorization

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


User Roles

Role

Description

Admin

Manage users, documents, queries, and system information

User

Upload documents and ask questions using the RAG system

Major Functionalities

User Authentication

Admin Authentication

Role-based Authorization

PDF Processing

Image Processing

OCR for Scanned Documents

Text Chunking

Text Embeddings

FAISS Vector Search

Hybrid Search

Gemini-based Answer Generation

Source and Page Retrieval

Query History

Query Caching

Document Management

User Management

Query Management

Processing Status Tracking

RAG Workflow

User uploads a PDF or image.

The document is processed and text is extracted.

Scanned documents are processed using OCR.

Extracted content is divided into chunks.

Chunks are converted into vector embeddings.

Embeddings are stored in the FAISS vector index.

The user submits a question.

Relevant document chunks are retrieved.

Retrieved context is provided to Gemini.

Gemini generates the answer.

Source and page information is returned to the user.

Installation

Clone Repository

git clone <repository-url>
cd DocuRAG-main

Backend Setup

pip install -r requirements.txt

Configure the required environment variables, including the Gemini API key.

Do not commit API keys or .env files to GitHub.

Frontend Setup

cd frontend
npm install

Run the Project

Start Backend

From the project root:

uvicorn backend.fastapi_app:app --host 127.0.0.1 --port 8000 --reload

The backend runs at:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

The backend can also be started using:

start_backend.bat

Start Frontend

Open another terminal:

cd frontend
npm run dev

Open the URL provided by Vite in the browser.

Usage

User

Create an account.

Log in to the application.

Upload a PDF or image.

Wait for document processing.

Ask questions about the uploaded document.

View the generated answer.

Check the source and page references.

View previous queries when required.

Admin

Open the admin login page.

Log in using an admin account.

Open the admin dashboard.

View system statistics.

Manage users.

Manage documents.

View processing failures.

View and manage queries.

API Documentation

FastAPI provides interactive API documentation at:

http://127.0.0.1:8000/docs

The documentation can be used to view and test the available API endpoints.

Team

Team: CODENOVA

Event: Cognizant NPN Hackathon

Project: DocuRAG
