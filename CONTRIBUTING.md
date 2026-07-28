# Contributing to Multimind AI Platform

Thank you for your interest in contributing to Multimind AI! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests: `pytest tests/ -v`
6. Commit your changes with a clear, descriptive message
7. Push to your fork and open a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/thirisha2006-S/multimind-ai-platform.git
cd multimind-ai-platform

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Copy environment file
cp .env.example .env
```

## Code Style

- Use **ruff** for linting
- Use **black** for formatting
- Follow PEP 8 conventions
- Write docstrings for all public modules, classes, and functions

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Pull Request Process

1. Ensure your code passes linting and all tests
2. Update documentation if needed
3. Describe the changes in your PR
4. Link any related issues

## Questions?

Open an issue on GitHub or reach out to the team at thirishasriram079@gmail.com.