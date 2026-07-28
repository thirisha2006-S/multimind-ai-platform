<div align="center">

# Multimind AI Platform

**Multimind AI** is an AI Operating System for enterprises that unifies organizational knowledge, documents, projects, employees, and business intelligence into one secure, multi-agent platform with explainable AI, organizational memory, and decision support.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

</div>

## Overview

Multimind AI is an enterprise-grade AI Operating System that orchestrates multiple AI agents to provide:

- **Multi-Agent Coordination** — Collaborative agents that work together on complex enterprise tasks
- **Organizational Memory** — Persistent knowledge storage with explainable retrieval
- **Knowledge Management** — Document ingestion, chunking, and vector-based semantic search
- **Decision Support** — AI-powered recommendations with full reasoning transparency
- **Security & Compliance** — Role-based access control and audit logging

## Architecture

```
multimind-ai-platform/
├── src/
│   ├── api/                  # FastAPI application layer
│   │   ├── main.py           # Application entry point
│   │   └── routers/          # API route definitions
│   ├── agents/               # Multi-agent system
│   │   ├── base.py           # Base agent class
│   │   └── orchestrator.py   # Agent coordination engine
│   ├── core/                 # Core infrastructure
│   │   ├── config.py         # Application settings
│   │   ├── logger.py         # Logging configuration
│   │   └── ...
│   ├── knowledge/            # Knowledge management
│   │   ├── ingestor.py       # Document ingestion
│   │   └── retriever.py      # Vector-based retrieval
│   └── memory/               # Organizational memory
│       └── store.py          # Memory storage engine
├── config/                   # Environment configs
├── deploy/                   # Deployment configurations
├── docs/                     # Documentation
├── tests/                    # Test suite
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.10+
- Docker & Docker Compose (for full stack)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/thirisha2006-S/multimind-ai-platform.git
cd multimind-ai-platform

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the application
uvicorn src.api.main:app --reload
```

### Using Docker Compose

```bash
docker-compose up -d
```

The API will be available at `http://localhost:8000`. The interactive API docs are at `http://localhost:8000/docs`.

## Features

| Feature | Description |
|---------|-------------|
| Multi-Agent System | Orchestrate multiple AI agents to tackle complex tasks collaboratively |
| Explainable AI | Every agent decision includes reasoning and confidence scores |
| Knowledge Ingestion | Upload and process documents into a searchable knowledge base |
| Vector Search | Semantic search over organizational documents using embeddings |
| Organizational Memory | Persistent memory that retains context across sessions |
| Decision Support | AI-driven insights and recommendations for business decisions |
| REST API | Full-featured API for integration with enterprise systems |

## Project Structure

```
src/
├── api/                    # API layer (FastAPI)
│   ├── main.py             # App creation with lifespan hooks
│   └── routers/            # Route modules (agents, memory, knowledge, etc.)
├── agents/                 # Multi-agent system
│   ├── base.py             # AgentConfig, AgentResponse, BaseAgent (ABC)
│   └── orchestrator.py     # AgentOrchestrator for parallel/sequential execution
├── core/                   # Infrastructure
│   ├── config.py           # Pydantic settings with env file support
│   └── logger.py           # Loguru-based logging setup
├── knowledge/              # Knowledge management
│   ├── ingestor.py         # DocumentIngestor (ABC) for chunking docs
│   └── retriever.py        # KnowledgeRetriever with vector search
└── memory/                 # Organizational memory
    └── store.py            # MemoryStore for persistent key-value memory
```

## Configuration

All configuration is managed through environment variables. See `.env.example` for available options.

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@localhost:5432/multimind` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `OPENAI_API_KEY` | OpenAI API key | — |
| `DEBUG` | Enable debug mode | `False` |

## Running Tests

```bash
pytest tests/ -v
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Contact

For questions or support, reach out to the team at thirishasriram079@gmail.com.
