# 🤖 AI Knowledge Assistant

A production-style **Full Stack AI Knowledge Assistant** built while learning modern Backend Development, Generative AI, Retrieval-Augmented Generation (RAG), and scalable software architecture.

The project was developed step by step, with every concept first learned theoretically, then implemented, tested, and integrated into a single application.

---

# 🚀 Project Overview

The AI Knowledge Assistant allows users to:

- Register and authenticate securely
- Chat with an AI assistant
- Upload PDF documents
- Generate embeddings
- Store vectors inside ChromaDB
- Perform semantic search
- Ask questions about uploaded documents using RAG
- Process documents asynchronously using RabbitMQ
- Cache AI responses using Redis
- Run the entire application with Docker

This project combines modern backend engineering with AI-powered document retrieval into a single production-style application.

---

# 🏗️ System Architecture

```text
                    +----------------------+
                    |   React + TypeScript |
                    |      Frontend        |
                    +----------+-----------+
                               |
                               |
                        REST APIs (JWT)
                               |
                               ▼
                    +----------------------+
                    |   FastAPI Backend    |
                    +----------+-----------+
                               |
        +-----------+----------+-----------+-----------+
        |           |                      |           |
        ▼           ▼                      ▼           ▼
 PostgreSQL      Redis                RabbitMQ     Gemini API
(Database)      (Cache)             (Background)   (LLM)
        |                                   |
        +--------------------+--------------+
                             |
                             ▼
                      ChromaDB Vector Store
                             |
                             ▼
                       LangChain + RAG
```

---

# ✨ Features

## 🔐 Authentication

- JWT Authentication
- Secure Password Hashing
- Protected Routes
- User Registration
- Login
- Logout
- Session Validation

---

## 💬 AI Chat

- AI-powered conversations
- Google Gemini Integration
- Markdown Rendering
- Response Metadata
- Error Handling
- Loading States

---

## 📄 Document Management

- Upload PDF Documents
- Background Processing
- Document Status Tracking

Document lifecycle:

```
UPLOADING
      │
      ▼
PROCESSING
      │
      ▼
READY
```

---

## 🧠 Semantic Search

- Embedding Generation
- Vector Similarity Search
- ChromaDB Integration
- Ranked Search Results

---

## 📚 Retrieval-Augmented Generation (RAG)

- Document Chunking
- Context Retrieval
- AI Grounded Responses
- Source-aware Question Answering

---

## ⚡ Background Processing

- RabbitMQ Integration
- Asynchronous Document Processing
- Worker-based Architecture

---

## 🚀 Caching

- Redis Integration
- AI Response Cache
- Faster Repeated Queries

---

## 🐳 Docker Support

- Docker Compose
- Multi-container Setup
- PostgreSQL
- Redis
- RabbitMQ
- Backend
- Frontend

---

# 🛠 Tech Stack

## Backend

- Python
- FastAPI
- SQLAlchemy ORM
- Pydantic
- Uvicorn

---

## Database

- PostgreSQL

---

## AI

- Google Gemini API
- LangChain
- ChromaDB
- Embeddings
- Retrieval-Augmented Generation (RAG)

---

## Messaging

- RabbitMQ

---

## Cache

- Redis

---

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui
- Axios
- React Router

---

## DevOps

- Docker
- Docker Compose
- Git
- GitHub

---

# 📂 Project Structure

```text
AI-Knowledge-Assistant/
│
├── backend/
│   │
│   ├── app/
│   │   ├── cache/
│   │   ├── database/
│   │   ├── memory/
│   │   ├── messaging/
│   │   ├── parsers/
│   │   ├── prompts/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── vectorstore/
│   │   ├── config.py
│   │   ├── logger.py
│   │   ├── models.py
│   │   ├── dependencies.py
│   │   └── main.py
│   │
│   ├── uploads/
│   ├── chroma_db/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
│
└── README.md
```

---

# 🔌 Main API Modules

## Authentication

- Register
- Login
- Current User

---

## Users

- Create User
- Update User
- Delete User
- List Users

---

## Chat

- AI Chat Endpoint

---

## Documents

- Upload PDF
- List Documents
- Delete Document

---

## Search

- Semantic Search

---

## RAG

- Ask Questions from Uploaded Documents

---

# 🔄 Document Processing Flow

```text
Upload PDF
      │
      ▼
Save File
      │
      ▼
Create Database Record
      │
      ▼
RabbitMQ Queue
      │
      ▼
Worker
      │
      ▼
Extract Text
      │
      ▼
Chunk Document
      │
      ▼
Generate Embeddings
      │
      ▼
Store in ChromaDB
      │
      ▼
READY
```

---

# ✅ Completed Learning Phases

- ✅ Environment Setup
- ✅ Python Fundamentals
- ✅ REST APIs
- ✅ FastAPI
- ✅ PostgreSQL
- ✅ SQLAlchemy ORM
- ✅ JWT Authentication
- ✅ AI Chat Integration
- ✅ Prompt Engineering
- ✅ LangChain
- ✅ ChromaDB
- ✅ Semantic Search
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Redis
- ✅ RabbitMQ
- ✅ Docker
- ✅ React Frontend
- ✅ Frontend–Backend Integration


---

## Start with Docker

```bash
cd backend

docker compose up --build
```

Backend:

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

Frontend:

```
http://localhost:5173
```

---

# 📚 What I Learned

This project helped me gain practical experience with:

- Backend API Development
- Authentication & Authorization
- Database Design
- ORM Relationships
- AI Integration
- Vector Databases
- Semantic Search
- Retrieval-Augmented Generation
- Background Workers
- Caching
- Docker
- Full Stack Development
- Production-style Architecture

---

# 👨‍💻 Author

**Aaditya Aaliwal**

Built as a hands-on learning project to understand modern AI backend development and production-ready application architecture.