# Changelog

All notable changes to PomPom-A2A will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- WebSocket support for real-time communication
- Agent registry for centralized discovery
- Load balancing capabilities
- Circuit breaker pattern for fault tolerance

## [0.1.0] - 2025-01-02

### Added
- 🎉 Initial release of PomPom-A2A
- Complete A2A Protocol v0.2.6 implementation
- Message-based communication (stateless)
- Task-based communication (stateful)
- Streaming support with Server-Sent Events
- Agent capability discovery via agent cards
- FastAPI integration with automatic route generation
- Comprehensive client library with async support
- Type-safe models with Pydantic validation
- In-memory task storage implementation
- Complete test suite with pytest
- Echo agent sample implementation
- Client examples demonstrating all features
- Development tools and setup scripts

### Core Features
- **TaskManager**: Complete task lifecycle management
- **A2AClient**: Full-featured client with streaming support
- **A2ACardResolver**: Agent discovery and capability resolution
- **FastAPI Integration**: One-line agent hosting
- **Type Safety**: Full type hints throughout
- **Async Support**: Built for modern Python async/await
- **Error Handling**: Comprehensive exception hierarchy
- **Testing**: Mock clients and test utilities

### Supported Communication Patterns
- Direct message sending with immediate response
- Streaming responses with Server-Sent Events
- Task creation and management
- Task message sending with history
- Task cancellation and status tracking
- Agent capability discovery

### Framework Support
- FastAPI (primary)
- Extensible architecture for Flask, Django

### Python Compatibility
- Python 3.8+
- Full async/await support
- Type hints compatible with mypy

### Documentation
- Comprehensive README with examples
- Development guide with best practices
- API documentation with type hints
- Sample implementations and use cases

## [0.0.1] - 2025-01-01

### Added
- Project initialization
- Basic project structure
- Initial development setup