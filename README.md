# DocuRAG

Cognizant NPN Hackathon - Team CODENOVA

DocuRAG is an AI-powered document question-answering system using Retrieval-Augmented Generation (RAG).

## Features

- User registration and login
- Admin login and dashboard
- PDF and image upload
- OCR for scanned documents
- Semantic document search
- AI-powered question answering
- Source and page references
- Query history
- Query caching
- User and document management

## Technology Stack

Frontend: Vue.js, Vite, JavaScript, HTML, CSS

Backend: Python, FastAPI, Uvicorn, SQLite

AI and RAG: Google Gemini, Sentence Transformers, FAISS, PyMuPDF, Pillow

Authentication: JWT, bcrypt

## Requirements

Python 3.x

Node.js

npm

Gemini API key

## Installation

Clone the repository:

git clone <repository-url>

cd DOCURAG

Install backend dependencies:

pip install -r requirements.txt

Install frontend dependencies:

cd frontend

npm install

Configure the required environment variables, including the Gemini API key.

Do not upload API keys or .env files to GitHub.

## Running the Project

Start the backend from the project root:

uvicorn backend.fastapi_app:app --host 127.0.0.1 --port 8000 --reload

The backend will run at:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

Start the frontend:

cd frontend

npm run dev

Open the URL provided by Vite in your browser.

## Usage

User:

Register an account.

Log in to the application.

Upload a PDF or image.

Wait for the document to be processed.

Ask questions about the uploaded document.

View the generated answer.

Check the source and page references.

Admin:

Open the admin login page.

Log in using the admin account.

Open the admin dashboard.

View users, documents, queries, and processing information.

Manage users and documents.

## Project Structure

DOCURAG/
backend/
database/
frontend/
uploads/
create_admin.py
start_backend.bat
requirements.txt
README.md

## Team

Team: CODENOVA

Event: Cognizant NPN Hackathon

Project: DocuRAG

## License

Copyright (c) 2026 Team CODENOVA

