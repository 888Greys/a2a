# Contributing to PomPom-A2A 🍮

Thank you for your interest in contributing to PomPom-A2A! We're excited to have you join our community of developers building the future of agent communication.

## 🌟 Ways to Contribute

- 🐛 **Bug Reports**: Help us identify and fix issues
- ✨ **Feature Requests**: Suggest new features and improvements
- 📝 **Documentation**: Improve our docs, examples, and guides
- 🔧 **Code Contributions**: Submit bug fixes and new features
- 🎨 **Examples**: Create sample agents and use cases
- 🧪 **Testing**: Help improve our test coverage
- 💬 **Community**: Help others in discussions and issues

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/yourusername/pompompurin-a2a.git
cd pompompurin-a2a

# Add the original repository as upstream
git remote add upstream https://github.com/yourusername/pompompurin-a2a.git
```

### 2. Set Up Development Environment

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Verify installation
pytest
```

### 3. Create a Branch

```bash
# Create a new branch for your contribution
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number
```

## 🔧 Development Workflow

### Code Style

We use several tools to maintain code quality:

```bash
# Format code
black src/ tests/ samples/
isort src/ tests/ samples/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/

# Run all checks
python scripts/check.py  # If available
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/pompompurin_a2a --cov-report=html

# Run specific test file
pytest tests/test_client.py

# Run specific test
pytest tests/test_client.py::test_send_message -v
```

### Documentation

```bash
# Build documentation locally (if using Sphinx)
cd docs/
make html

# Serve documentation
python -m http.server 8000 -d docs/_build/html
```

## 📝 Contribution Guidelines

### Bug Reports

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected behavior** vs **actual behavior**
4. **Environment details**:
   - Python version
   - PomPom-A2A version
   - Operating system
   - Relevant dependencies

**Template:**
```markdown
## Bug Description
Brief description of the issue.

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Environment
- Python: 3.12.0
- PomPom-A2A: 0.1.0
- OS: Ubuntu 22.04
- FastAPI: 0.104.1

## Additional Context
Any other relevant information.
```

### Feature Requests

For feature requests, please provide:

1. **Clear description** of the feature
2. **Use case** and motivation
3. **Proposed implementation** (if you have ideas)
4. **Alternatives considered**

### Pull Requests

#### Before Submitting

1. **Check existing issues** to avoid duplicates
2. **Discuss major changes** in an issue first
3. **Write tests** for new functionality
4. **Update documentation** as needed
5. **Follow code style** guidelines

#### PR Checklist

- [ ] Tests pass locally (`pytest`)
- [ ] Code is formatted (`black`, `isort`)
- [ ] Code passes linting (`ruff`)
- [ ] Type checking passes (`mypy`)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (for notable changes)
- [ ] Commit messages are clear and descriptive

#### PR Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
```

## 🏗️ Project Structure

```
pompompurin-a2a/
├── src/
│   └── pompompurin_a2a/        # Main package
│       ├── __init__.py
│       ├── client/             # Client implementations
│       ├── server/             # Server implementations
│       ├── models/             # Data models
│       ├── integrations/       # Framework integrations
│       └── exceptions.py       # Exception classes
├── tests/                      # Test suite
├── samples/                    # Example implementations
├── docs/                       # Documentation
├── scripts/                    # Development scripts
└── pyproject.toml             # Project configuration
```

## 🧪 Testing Guidelines

### Writing Tests

```python
import pytest
from pompompurin_a2a import Message, MessageRole, TextPart

class TestMessage:
    def test_create_message(self):
        message = Message(
            role=MessageRole.USER,
            parts=[TextPart(text="Hello")]
        )
        assert message.role == MessageRole.USER
        assert len(message.parts) == 1

    @pytest.mark.asyncio
    async def test_async_functionality(self):
        # Test async functions
        result = await some_async_function()
        assert result is not None
```

### Test Categories

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows
- **Performance Tests**: Test performance characteristics

### Test Naming

- Use descriptive test names: `test_send_message_returns_response`
- Group related tests in classes: `TestA2AClient`
- Use fixtures for common setup: `@pytest.fixture`

## 📚 Documentation Guidelines

### Code Documentation

```python
async def send_message(self, message: Message) -> Message:
    """
    Send a message to the agent and get a response.
    
    Args:
        message: The message to send to the agent
        
    Returns:
        Message: The agent's response
        
    Raises:
        A2AClientException: If the request fails
        
    Example:
        >>> client = A2AClient("http://localhost:8000/agent")
        >>> message = Message(role=MessageRole.USER, parts=[TextPart(text="Hello")])
        >>> response = await client.send_message(message)
        >>> print(response.parts[0].text)
    """
```

### README Updates

When adding features, update:
- Feature list
- Usage examples
- API reference
- Installation instructions (if needed)

## 🎯 Specific Contribution Areas

### 🔌 New Integrations

We welcome integrations with other frameworks:

```python
# Example: Django integration
from pompompurin_a2a.integrations.django import add_a2a_urls

urlpatterns = [
    path('agent/', include(add_a2a_urls(task_manager, 'my-agent'))),
]
```

### 🤖 Sample Agents

Create example agents for common use cases:

```python
# samples/weather_agent/main.py
async def weather_agent(message: Message) -> Message:
    location = extract_location(message.parts[0].text)
    weather = await get_weather(location)
    return create_weather_response(weather)
```

### 🧪 Testing Utilities

Help improve our testing infrastructure:

```python
# pompompurin_a2a/testing.py
class MockA2AClient:
    """Mock client for testing agents."""
    
    async def send_message(self, message: Message) -> Message:
        # Mock implementation
        pass
```

### 📖 Documentation

- Add examples to the README
- Create tutorials and guides
- Improve API documentation
- Add type hints and docstrings

## 🏆 Recognition

Contributors will be:
- Listed in our [Contributors](https://github.com/yourusername/pompompurin-a2a/graphs/contributors) page
- Mentioned in release notes for significant contributions
- Invited to join our community Discord
- Eligible for contributor swag (when available)

## 🤝 Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- Be respectful and considerate
- Use inclusive language
- Accept constructive feedback gracefully
- Focus on what's best for the community
- Show empathy towards other community members

## 📞 Getting Help

- 💬 **Discord**: [Join our community](https://discord.gg/pompom-a2a)
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/pompompurin-a2a/issues)
- 💡 **Discussions**: [GitHub Discussions](https://github.com/yourusername/pompompurin-a2a/discussions)
- 📧 **Email**: team@pompom-a2a.dev

## 🎉 Thank You!

Every contribution, no matter how small, helps make PomPom-A2A better for everyone. We appreciate your time and effort in helping build the future of agent communication!

---

*Made with 💖 and 🍮 by the PomPom-A2A community*