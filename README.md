# Anime Recommendation Engine

An AI-powered anime recommendation platform built using FastAPI, PostgreSQL, Qdrant Vector Database, and Large Language Models.

The project combines traditional anime tracking features with semantic search and personalized recommendations using vector embeddings.

---

## Features

### Anime Database
- Large anime catalog stored in PostgreSQL
- Detailed anime information and metadata
- Fast filtering and retrieval

### User Management
- User authentication and profiles
- Watchlist management
- Watched anime tracking
- Personalized recommendation history

### AI Recommendation System
- Semantic anime search using embeddings
- Vector similarity matching with Qdrant
- Content-based recommendations
- LLM-assisted recommendation explanations

### Recommendation Pipeline

1. User provides an anime preference or selects an anime
2. Anime information is converted into vector embeddings
3. Qdrant performs similarity search
4. Relevant anime candidates are retrieved
5. LLM refines and formats recommendations
6. Results are displayed through the frontend

---

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic

### AI & Search
- Qdrant Vector Database
- Embedding Models
- Ollama
- Retrieval-Augmented Recommendation Pipeline

### Frontend
- HTML
- CSS
- JavaScript

### Deployment
- Docker
- Docker Compose
- Linux VPS

---

## Architecture

```text
User
 │
 ▼
Frontend (HTML + JavaScript)
 │
 ▼
FastAPI Backend
 ├── PostgreSQL
 │      └── Anime / Users / Watchlists
 │
 ├── Embedding Pipeline
 │
 └── Qdrant Vector Database
        └── Similar Anime Search
                │
                ▼
            Ollama LLM
                │
                ▼
      Personalized Recommendations
````

---

## Project Structure

```text
MAL-project/
│
├── backend/
│   ├── routes/
│   ├── models/
│   ├── services/
│   ├── database/
│   └── main.py
│
├── frontend/
│   ├── html/
│   ├── css/
│   └── js/
│
├── qdrant/
├── embeddings/
├── docker/
├── requirements.txt
└── docker-compose.yml
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/shayan-wasLazy/MAL-project.git
cd MAL-project
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Services

```bash
docker compose up -d
```

### Run Backend

```bash
uvicorn backend.main:app --reload
```

### API Documentation

```text
http://localhost:8000/docs
```

---

## Future Improvements

* Hybrid recommendation system
* Collaborative filtering
* User review analysis
* Anime-to-anime recommendation graph
* Recommendation feedback loop
* Advanced search filters
* Mobile application

---

## Learning Outcomes

This project explores:

* Backend API development with FastAPI
* Relational database design with PostgreSQL
* Vector databases and semantic search
* Retrieval-Augmented Generation (RAG)
* Recommendation system design
* Containerization with Docker
* Full-stack application deployment

---

## Author

**Shayan Mandrekar**

B.Tech Data Science Student
Backend Development • AI Applications • Recommendation Systems
