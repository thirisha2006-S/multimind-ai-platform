# Getting Started

## Prerequisites

- Python 3.10 or higher
- Docker & Docker Compose (optional, for full stack deployment)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/thirisha2006-S/multimind-ai-platform.git
cd multimind-ai-platform
```

### 2. Set Up the Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# OR on Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -e .
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

### 5. Run the Application

```bash
# Development server
uvicorn src.api.main:app --reload
```

The server starts at `http://localhost:8000`.

### 6. Interactive API Documentation

Once the server is running, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Using Docker

### Full Stack (API + PostgreSQL + Redis)

```bash
docker-compose up -d
```

### Build and Run

```bash
docker build -t multimind-ai-platform .
docker run -p 8000:8000 --env-file .env.multimind-ai-platform
```

## Testing

```bash
pytest tests/ -v
```

## Next Steps

- [ ] Add agent implementations for specific use cases
- [ ] Configure vector store with production embeddings
- [ ] Set up authentication and role-based access
- [ ] Integrate with enterprise document storage (S3, SharePoint, etc.)