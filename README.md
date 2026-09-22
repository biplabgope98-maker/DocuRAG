# DocuRAG

### Cognizant NPN Hackathon — Team CODENOVA

An AI-powered document question-answering system using Retrieval-Augmented Generation (RAG).

DocuRAG
DocuRAG is an AI-powered document question-answering system that lets users upload PDFs and images, retrieve relevant information using semantic and keyword search, and ask natural-language questions about their documents.

The system combines document processing, chunking, embeddings, FAISS vector search, hybrid retrieval, image analysis/OCR, Gemini-based answer generation, source references, confidence information, authentication, query history, and response caching.

Important: This README describes the current local implementation. It does not claim cloud services such as GCS, BigQuery, or Vertex AI are part of the working deployment unless they are explicitly configured and integrated in the submitted code.

Features
User Features
User registration and login

JWT-based authentication

Upload PDF, PNG, JPG, and JPEG files

Document processing status

PDF text extraction

Scanned/image-only PDF handling through image analysis/OCR

Image analysis

Text chunking

Semantic vector search

Keyword/hybrid retrieval

Natural-language document questions

Gemini-powered answers

Source/page information with answers

Confidence information

Conversation-based chat

Search/query history

Response caching

User document isolation

Delete uploaded documents

Admin Features
Separate admin access

Admin authentication using the existing JWT system

Dashboard statistics

User management

Activate/deactivate users

Delete normal user accounts

Document monitoring

Document deletion

Processing failure monitoring

Query monitoring

Query deletion

Cache-hit statistics

System Architecture
                    ┌─────────────────────┐
                    │    Vue Frontend     │
                    │  User + Admin UI    │
                    └──────────┬──────────┘
                               │ HTTP/JSON
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    │      Port 8000      │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      Authentication     Document API       Query API
             │                 │                 │
             ▼                 ▼                 ▼
          SQLite       PDF/Image Processing   Cache Check
                               │                 │
                               ▼                 │
                         Chunking + OCR          │
                               │                 │
                               ▼                 │
                         Embeddings              │
                               │                 │
                               ▼                 │
                         FAISS Search            │
                               │                 │
                               ▼                 │
                       Hybrid Retrieval ◄────────┘
                               │
                               ▼
                         Gemini / LLM
                               │
                               ▼
                  Answer + Sources + Confidence
Query Flow
User Question
      │
      ▼
Normalize question
      │
      ▼
Cache lookup
      │
 ┌────┴─────┐
 │          │
HIT        MISS
 │          │
 ▼          ▼
Return    Document security check
cached       │
answer       ▼
         Hybrid retrieval
         ┌────┴────┐
         │         │
      Vector    Keyword
      Search    Search
         │         │
         └────┬────┘
              ▼
       Relevant chunks
              │
              ▼
        Image context
        when relevant
              │
              ▼
       Gemini answer
              │
              ▼
     Save query + sources
              │
              ▼
        Save to cache
              │
              ▼
       Return response
Document Processing Flow
Upload PDF/Image
       │
       ▼
File validation
       │
       ▼
Store file locally
       │
       ├── PDF ───────────────► PyMuPDF extraction
       │                              │
       │                              ├── Text pages
       │                              │      ▼
       │                              │   Chunking
       │                              │
       │                              └── Scanned pages
       │                                     ▼
       │                                  OCR/Image analysis
       │
       └── Image ─────────────► Gemini image analysis
                                      │
                                      ▼
                                Extracted text/context
                                      │
                                      ▼
                                   Chunking
                                      │
                                      ▼
                                  Embeddings
                                      │
                                      ▼
                               FAISS index update
Technology Stack
Frontend
Vue.js

Vite

JavaScript

HTML/CSS

Backend
Python

FastAPI

Uvicorn

REST APIs

AI / RAG
Google Gemini through google-genai

Sentence Transformers

FAISS

Hybrid semantic + keyword retrieval

OCR/image understanding through Gemini image analysis

Document Processing
PyMuPDF

Image processing

Text chunking

Scanned PDF OCR support

Database
SQLite

The database stores users, documents, document chunks, image analysis results, queries, and query-source relationships.

Authentication
JWT

Password hashing with bcrypt

User/admin role separation

Caching
Thread-safe in-memory cache

1-hour TTL

Maximum 500 cached entries

Cache is scoped using user and conversation information

Cached responses are marked with cache_hit

Project Structure
DOCURAG/
│
├── backend/
│   ├── api/
│   │   ├── admin_api.py
│   │   ├── auth_api.py
│   │   ├── documents_api.py
│   │   └── rag_api.py
│   │
│   ├── routes/
│   │
│   ├── services/
│   │   ├── cache.py
│   │   ├── document_processor.py
│   │   ├── hybrid_search.py
│   │   ├── image_analyzer.py
│   │   ├── image_file_processor.py
│   │   ├── image_processor.py
│   │   ├── image_search.py
│   │   └── vector_store.py
│   │
│   ├── app.py
│   ├── fastapi_app.py
│   └── ...
│
├── database/
│   ├── database.py
│   └── docurag.db
│
├── frontend/
│   ├── src/
│   │   └── App.vue
│   ├── package.json
│   └── ...
│
├── uploads/
│   ├── pdfs/
│   └── images/
│
├── docurag.index
├── chunks.pkl
├── create_admin.py
├── start_backend.bat
├── requirements.txt
└── README.md
Local Storage
The current local implementation keeps uploaded files separated by type:

uploads/
├── pdfs/
│   └── <uuid>_<filename>.pdf
│
└── images/
    ├── <uuid>_<filename>.png
    └── <uuid>_<filename>.jpg
The actual file path is stored in the database.

FAISS files are currently stored in the project root:

docurag.index
chunks.pkl
Database
The SQLite database contains the main application data.

Important tables include:

users

documents

document_chunks

image_analysis

queries

query_sources

The database is created programmatically by the application.

Requirements
Python 3.10+ recommended

Node.js and npm

A Google Gemini API key

Sufficient disk space for uploaded documents and the local embedding model

Backend Setup
1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd DOCURAG
2. Create a virtual environment
Windows:

python -m venv .venv
.venv\Scripts\activate
macOS/Linux:

python3 -m venv .venv
source .venv/bin/activate
3. Install Python dependencies
pip install -r requirements.txt
4. Configure the Gemini API key
Set the API key as an environment variable.

Windows PowerShell:

$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
Windows CMD:

set GEMINI_API_KEY=YOUR_GEMINI_API_KEY
Do not commit API keys to GitHub.

If the code/environment you are using expects a different Gemini environment-variable name, use the name expected by that implementation.

5. Start the backend
The current development command is:

uvicorn backend.fastapi_app:app --host 127.0.0.1 --port 8000 --reload
Or on Windows:

.\start_backend.bat
The API will be available at:

http://127.0.0.1:8000
Swagger documentation:

http://127.0.0.1:8000/docs
Frontend Setup
Open another terminal:

cd frontend
npm install
npm run dev
The Vite development server normally starts on:

http://localhost:5173
The frontend is configured to communicate with the FastAPI backend at:

http://127.0.0.1:8000
Application Usage
Normal User
Open the frontend.

Register an account.

Log in.

Upload a PDF or image.

Wait until the document status becomes Processed.

Select the document.

Ask a natural-language question.

Review the generated answer.

Review source/page information.

Continue the conversation or start a new chat.

Admin
Admin access is provided through the application's admin flow.

The admin dashboard provides:

user statistics

document statistics

processing failures

recent queries

cache-hit information

user status management

document deletion

query deletion

Admin credentials must never be placed in the README or source code.

API Overview
Authentication
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me
Documents
POST   /api/documents/upload
GET    /api/documents
GET    /api/documents/{document_id}
DELETE /api/documents/{document_id}
Query / RAG
POST /api/ask
GET  /api/history
POST /api/new_chat
POST /api/clear_cache
Admin
GET    /api/admin/health
GET    /api/admin/statistics
GET    /api/admin/users
PUT    /api/admin/users/{user_id}/activate
PUT    /api/admin/users/{user_id}/deactivate
DELETE /api/admin/users/{user_id}
GET    /api/admin/documents
DELETE /api/admin/documents/{document_id}
GET    /api/admin/processing-failures
GET    /api/admin/queries
DELETE /api/admin/queries/{query_id}
GET    /api/admin/documents/{document_id}
The exact API surface should always be verified against the currently submitted backend code.

Embeddings and Vector Search
DocuRAG uses Sentence Transformers to generate dense vector embeddings.

The current vector store uses:

Model: all-mpnet-base-v2
Embedding dimension: 768
Vector index: FAISS IndexFlatIP
Embeddings are normalized before similarity search.

The FAISS index and its chunk metadata are stored locally.

Hybrid Retrieval
The system combines:

Semantic vector retrieval

Keyword retrieval

This allows the system to handle both semantic questions and questions containing important exact terms.

The retrieved context is then passed to Gemini for answer generation.

Image and OCR Support
DocuRAG supports image documents and scanned PDF pages.

For image/scanned content, the system can use Gemini image analysis to obtain information such as:

description

detected objects

extracted text

orientation

colors

other image-related context

The extracted information can then participate in the document question-answering workflow.

Caching
DocuRAG uses an in-memory cache.

Current configuration:

TTL: 1 hour
Maximum entries: 500
The cache key includes:

user_id + conversation_id + normalized question
On a cache hit, the previously generated response can be returned without repeating the complete retrieval and Gemini generation flow.

The response contains a cache indicator so the frontend can display the cached state.

Important
The in-memory cache is cleared when the backend process restarts. A persistent cache such as Redis can be considered for a future production deployment.

Security
The project includes:

JWT authentication

Password hashing

User/admin role separation

User document ownership checks

Authorization checks on protected APIs

File type validation

File size validation

Processing failure handling

No API keys in the repository

Never commit:

.env
API keys
JWT secrets
Admin passwords
Service-account credentials
Private cloud credentials
Use environment variables or a secure secret-management system instead.

Error Handling
The application handles several failure cases, including:

invalid file types

oversized uploads

missing documents

failed document processing

scanned/image-only PDFs

AI/image-analysis errors

unauthorized access

inactive accounts

invalid authentication tokens

empty search results

cache expiration

Processing failures are recorded in the database and can be viewed from the admin dashboard.

Testing Checklist
Before submission, verify:

User registration works

User login works

Invalid credentials are rejected

Document upload works

PDF processing reaches Processed

Image upload works

Scanned PDF/OCR works

Questions return answers

Sources are displayed

Confidence is displayed

Same question can return from cache

Cache hit appears in admin statistics

Users cannot access another user's documents

User document deletion works

Admin login works

Admin user management works

Admin document deletion works

Admin query deletion works

Processing failures are visible

Swagger API documentation loads

Frontend and backend communicate correctly

Running the Project for a Demo
Recommended order:

Terminal 1 — Backend
cd C:\Users\bipla\DOCURAG
.\start_backend.bat
Terminal 2 — Frontend
cd C:\Users\bipla\DOCURAG\frontend
npm run dev
Then open the Vite URL shown by the terminal.

Troubleshooting
Backend does not start
Check:

python --version
pip install -r requirements.txt
Then run:

uvicorn backend.fastapi_app:app --host 127.0.0.1 --port 8000 --reload
Frontend cannot reach backend
Make sure FastAPI is running on:

http://127.0.0.1:8000
Document stays in processing/failed state
Check the backend terminal for the processing error and inspect the document's processing status/error message from the API/admin panel.

FAISS index problem
Rebuild the index using the project's vector-store rebuild function:

python -c "from backend.services.vector_store import rebuild_index; print(rebuild_index())"
Cache test
Ask the exact same question twice in the same conversation and for the same selected document.

Expected behavior:

First request  → normal RAG/Gemini processing
Second request → from cache
Limitations
The current implementation has some local-development limitations:

SQLite is used as the primary database.

FAISS index files are stored locally.

Uploaded files are stored locally.

Cache is in memory and is lost after backend restart.

Large-scale multi-user production deployment would require persistent/shared storage and a persistent cache.

Cloud storage and managed vector infrastructure are not assumed unless separately configured in the submitted implementation.

Future Improvements
Possible future improvements include:

Redis or another persistent distributed cache

Cloud object storage for uploaded documents

Managed/vector database deployment

Background document-processing workers

Multi-document question answering

Page-level text highlighting

Document comparison

Exporting answers and citations

Better monitoring and observability

Automated test coverage

Production-grade deployment and scaling

AI Assistance Declaration
AI-assisted development should be declared accurately according to the competition/institution requirements.

Examples of assistance may include:

debugging

code generation

documentation drafting

architecture discussion

error analysis

development guidance

Do not claim that AI wrote parts of the project that were not actually AI-assisted, and do not omit required declarations.

Submission Safety
Before pushing the final repository, check:

git status
Make sure sensitive files are not included.

At minimum, review:

.env
credentials
service-account JSON files
API keys
private keys
password files
local secrets
A .gitignore should be used to keep local secrets and generated files out of the repository. 

## License

This project, **DocuRAG**, was developed by **Team CODENOVA** for the **Cognizant NPN Hackathon**.

The source code and project materials are intended for hackathon evaluation and demonstration purposes.