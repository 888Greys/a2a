# PomPom-A2A Development Makefile

.PHONY: help install install-dev test test-cov lint format type-check clean build publish docs serve-docs

# Default target
help:
	@echo "🍮 PomPom-A2A Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  install      Install package in production mode"
	@echo "  install-dev  Install package in development mode with dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  test         Run tests"
	@echo "  test-cov     Run tests with coverage report"
	@echo "  lint         Run linting (ruff)"
	@echo "  format       Format code (black + isort)"
	@echo "  type-check   Run type checking (mypy)"
	@echo "  check        Run all checks (lint + format + type-check)"
	@echo ""
	@echo "Examples:"
	@echo "  run-echo     Start the echo agent"
	@echo "  run-client   Run client examples"
	@echo ""
	@echo "Build & Publish:"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build package"
	@echo "  publish      Publish to PyPI (requires PYPI_TOKEN)"
	@echo ""
	@echo "Documentation:"
	@echo "  docs         Build documentation"
	@echo "  serve-docs   Serve documentation locally"

# Installation
install:
	pip install .

install-dev:
	pip install -e ".[dev]"

# Testing
test:
	pytest

test-cov:
	pytest --cov=src/pompompurin_a2a --cov-report=html --cov-report=term-missing

# Code Quality
lint:
	ruff check src/ tests/ samples/

format:
	black src/ tests/ samples/
	isort src/ tests/ samples/

type-check:
	mypy src/

check: lint format type-check
	@echo "✅ All checks passed!"

# Examples
run-echo:
	python samples/echo_agent/main.py

run-client:
	python samples/client_examples/basic_client.py

# Build & Publish
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish: build
	twine upload dist/*

# Documentation
docs:
	@echo "📚 Building documentation..."
	@echo "Documentation will be available in the README.md"

serve-docs:
	@echo "📖 Serving documentation..."
	@echo "Open http://localhost:8000 to view the README"
	python -m http.server 8000

# Development helpers
setup: install-dev
	@echo "🍮 PomPom-A2A development environment ready!"
	@echo ""
	@echo "Next steps:"
	@echo "  make test        # Run tests"
	@echo "  make run-echo    # Start echo agent"
	@echo "  make run-client  # Test client"

# CI/CD helpers
ci-test: install-dev lint type-check test

# Quick development cycle
dev: format lint type-check test
	@echo "🚀 Development cycle complete!"