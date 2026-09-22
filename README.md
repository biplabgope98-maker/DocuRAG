DocuRAG



Cognizant NPN Hackathon --- Team CODENOVA



DocuRAG is an AI-powered document question-answering and search system

using Retrieval-Augmented Generation (RAG).



Features



User registration and JWT-based login



Separate administrator dashboard



PDF and image upload



OCR support for scanned/image-only PDF pages



Semantic and hybrid document retrieval



FAISS vector search



Gemini-powered question answering



Source and page references



Query history



Query caching



Admin user, document, and query management



Local storage separated by file type



Project Structure



DOCURAG/

├── backend/

│   ├── api/

│   │   ├── admin\_api.py

│   │   ├── auth\_api.py

│   │   ├── documents\_api.py

│   │   └── rag\_api.py

│   ├── routes/

│   ├── services/

│   │   ├── cache.py

│   │   ├── document\_processor.py

│   │   ├── hybrid\_search.py

│   │   ├── image\_analyzer.py

│   │   ├── image\_file\_processor.py

│   │   ├── image\_processor.py

│   │   ├── image\_search.py

│   │   └── vector\_store.py

│   ├── app.py

│   └── fastapi\_app.py

├── database/

│   ├── database.py

│   └── docurag.db

├── frontend/

│   ├── src/

│   │   └── App.vue

│   └── package.json

├── uploads/

│   ├── pdfs/

│   └── images/

├── docurag.index

├── chunks.pkl

├── create\_admin.py

├── start\_backend.bat

├── requirements.txt

└── README.md



Architecture



Frontend (Vue + Vite)

&#x20;       │

&#x20;       ▼

FastAPI Backend

&#x20;       │

&#x20;  ┌────┼─────────────┐

&#x20;  ▼    ▼             ▼

Upload Auth          RAG API

&#x20;  │                  │

&#x20;  ▼                  ▼

PDF/Image        Hybrid Retrieval

Processing            │

&#x20;  │             ┌────┴────┐

&#x20;  ▼             ▼         ▼

Chunks          FAISS     Cache

&#x20;  │               │        │

&#x20;  └───────────────┼────────┘

&#x20;                  ▼

&#x20;               Gemini

&#x20;                  │

&#x20;                  ▼

&#x20;            Answer + Sources



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



SQLite



AI / RAG



Google Gemini



Google GenAI SDK



Sentence Transformers



FAISS



PyMuPDF



Pillow



Authentication



JWT



bcrypt



Local Storage



Uploaded files are separated by type:



uploads/

├── pdfs/

│   └── <uploaded PDF files>

└── images/

&#x20;   ├── <uploaded PNG files>

&#x20;   ├── <uploaded JPG files>

&#x20;   └── <other supported images>



The actual file path is stored in the database.



FAISS files are stored in the project root:



docurag.index

chunks.pkl



SQLite database:



database/

└── docurag.db



Document Processing



Normal PDF



PDF

&#x20;│

&#x20;▼

Text Extraction

&#x20;│

&#x20;▼

Chunking

&#x20;│

&#x20;▼

Embeddings

&#x20;│

&#x20;▼

FAISS



Scanned PDF



Scanned PDF Page

&#x20;│

&#x20;▼

Page Rendering

&#x20;│

&#x20;▼

OCR / Gemini Vision

&#x20;│

&#x20;▼

Extracted Text

&#x20;│

&#x20;▼

Chunking

&#x20;│

&#x20;▼

Embeddings

&#x20;│

&#x20;▼

FAISS



Image



Uploaded images are analyzed and their extracted information can be

included in the retrieval pipeline.



RAG Query Flow



User Question

&#x20;     │

&#x20;     ▼

Cache Check

&#x20;     │

&#x20;     ├── Cache Hit ──► Cached Answer

&#x20;     │

&#x20;     ▼

Hybrid Retrieval

&#x20;     │

&#x20;     ▼

Relevant Chunks

&#x20;     │

&#x20;     ▼

Gemini

&#x20;     │

&#x20;     ▼

Answer + Sources

&#x20;     │

&#x20;     ▼

Save Query / Cache



Embeddings and Vector Search



The current embedding model is:



all-mpnet-base-v2



Current embedding dimension:



768



Embeddings are normalized and stored using a FAISS IndexFlatIP index.



Rebuild the index with:



python -c "from backend.services.vector\_store import rebuild\_index; print(rebuild\_index())"



Caching



The application includes an in-memory query cache.



Current configuration:



Cache TTL: 1 hour

Maximum cache size: 500 entries



The cache key uses the user, conversation context, and normalized

question.



Authentication



The application has separate logical access areas:



/login

&#x20;   └── Normal User



/admin/login

&#x20;   └── Administrator



Administrative APIs require administrator authentication.



Admin Dashboard



The administrator dashboard provides:



User statistics



User activation/deactivation



User deletion



Document listing



Document deletion



Processing-failure monitoring



Query history



Query deletion



Cache-hit statistics



Document details



Database



Important SQLite tables include:



users

documents

document\_chunks

image\_analysis

queries

query\_sources



Requirements



Install Python dependencies:



pip install -r requirements.txt



Install frontend dependencies:



cd frontend

npm install



Environment Variables



Secrets such as API keys and production JWT secrets should be supplied

through environment variables.



Do not commit:



.env

API keys

service-account credentials

passwords

private credentials



Running the Backend



From the project root:



uvicorn backend.fastapi\_app:app --host 127.0.0.1 --port 8000 --reload



Or:



.\\start\_backend.bat



Backend:



http://127.0.0.1:8000



Running the Frontend



Open another terminal:



cd frontend

npm install

npm run dev



Open the URL displayed by Vite.



API Documentation



With the backend running:



http://127.0.0.1:8000/docs



OpenAPI:



http://127.0.0.1:8000/openapi.json



Basic Usage



Start the FastAPI backend.



Start the Vue frontend.



Register or log in.



Upload a PDF or image.



Wait for processing to complete.



Ask questions about the uploaded content.



Review the answer and source information.



Administrators can use the admin dashboard for management.



Development Workflow



After making changes:



git status

git add .

git commit -m "Describe your changes"

git pull --rebase origin main

git push origin main



Team members can get the latest changes with:



git pull origin main



Testing Checklist



Backend starts successfully



Frontend starts successfully



User registration works



User login works



Administrator login works



PDF upload works



Image upload works



Scanned PDF/OCR works



Document reaches processed status



Questions return answers



Sources/page references are shown



Repeated questions can use cache



Admin statistics load



Admin user management works



Admin document deletion works



Admin query deletion works



FAISS index is available



Troubleshooting



Backend does not start



Run from the project root:



uvicorn backend.fastapi\_app:app --host 127.0.0.1 --port 8000 --reload



Frontend cannot connect



Confirm the backend is running on:



http://127.0.0.1:8000



Document remains uploaded



Check the FastAPI terminal for processing errors and verify the required

AI/API configuration.



Scanned PDF has no extracted text



Check the OCR/image-processing logs and confirm the AI configuration is

available.



FAISS index problem



Rebuild it using the command shown in the Embeddings section.



Security Notes



Never commit API keys.



Never commit passwords.



Never commit cloud credentials.



Use environment variables for secrets.



Administrative APIs require administrator authentication.



Use a strong production JWT secret.



Current Limitations



The development version uses local SQLite, local uploads, and a local

FAISS index.



Production deployment may require persistent cloud storage, managed

databases, persistent vector storage, production secret management, and

deployment-specific configuration.



Future Improvements



Cloud object storage



Managed vector database



Advanced OCR



Improved document ranking



Streaming AI responses



More analytics



Background processing for large documents



Additional document formats



More granular access control



Production deployment improvements



Hackathon



Project: DocuRAG

Event: Cognizant NPN Hackathon

Team: CODENOVA



DocuRAG was developed as a team project for hackathon evaluation and

demonstration.



License



This project, DocuRAG, was developed by Team CODENOVA for the

Cognizant NPN Hackathon.



The source code and project materials are intended for hackathon

evaluation and demonstration purposes.

