# Architecture Overview

## System Components

### 1. API Layer (`src/api/`)
- Built on **FastAPI** for high-performance async request handling
- RESTful endpoints for agents, memory, knowledge, and analytics
- Interactive API documentation via Swagger/OpenAPI

### 2. Agent System (`src/agents/`)
- **BaseAgent**: Abstract base class defining the agent interface
- **AgentOrchestrator**: Coordinates multiple agents in parallel or sequential workflows
- **AgentConfig**: Configuration model for agent behavior (model, temperature, capabilities)

### 3. Knowledge Management (`src/knowledge/`)
- **KnowledgeIngestor**: Abstract base for document ingestion pipelines
- **KnowledgeRetriever**: Vector-based semantic search over ingested documents
- Supports chunking, embedding generation, and re-ranking

### 4. Organizational Memory (`src/memory/`)
- **MemoryStore**: Persistent key-value store with categorization and metadata
- Supports TTL-based expiration for temporal knowledge
- Enables explainable recall of past decisions and context

### 5. Core Infrastructure (`src/core/`)
- **Settings**: Pydantic-based configuration with `.env` support
- **Logger**: Structured logging via Loguru

## Data Flow

```
User Request → API Layer → Agent Orchestrator → Individual Agents
                                                        ↓
                                              Knowledge Retriever
                                                        ↓
                                              Memory Store
                                                        ↓
                                              Response + Reasoning
```

## Technology Stack

| Component | Technology |
|-----------|-----------|
| API Framework | FastAPI + Uvicorn |
| AI/LLM | OpenAI API (gpt-4o) |
| Vector Store | ChromaDB |
| Agent Framework | LangChain |
| Database | PostgreSQL + SQLAlchemy |
| Cache/Queue | Redis + Celery |
| Auth | Python-Jose + Passlib |
| Testing | pytest + pytest-asyncio |

## Deployment

The application is containerized using Docker and can be deployed with Docker Compose:

```bash
docker-compose up -d
```

This starts the API, PostgreSQL, Redis, and Celery worker services.