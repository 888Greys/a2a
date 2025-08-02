# A2A Python SDK Development Guide

This guide will help you get started with developing and using the A2A Python SDK.

## Quick Start

### 1. Setup Development Environment

```bash
# Clone or navigate to the project
cd a2a-python

# Run the setup script (installs dependencies and runs tests)
python setup.py

# Or install manually:
pip install -r requirements.txt
pip install -e .
```

### 2. Run the Echo Agent

```bash
# Start the echo agent server
python samples/echo_agent/main.py
```

The agent will be available at:
- Agent endpoint: `http://localhost:8000/echo`
- Agent card: `http://localhost:8000/echo/card`
- Health check: `http://localhost:8000/health`

### 3. Test with Client

```bash
# In another terminal, run the client examples
python samples/client_examples/basic_client.py
```

## Project Structure

```
a2a-python/
├── src/a2a/                    # Core SDK code
│   ├── models/                 # Data models (Message, AgentCard, Task)
│   ├── client/                 # Client implementations
│   ├── server/                 # Server implementations
│   ├── integrations/           # Framework integrations (FastAPI)
│   └── exceptions.py           # A2A protocol exceptions
├── samples/                    # Example implementations
│   ├── echo_agent/            # Simple echo agent
│   └── client_examples/       # Client usage examples
├── tests/                     # Test suite
├── pyproject.toml            # Project configuration
├── requirements.txt          # Dependencies
└── README.md                 # Main documentation
```

## Core Components

### Models

The SDK provides Pydantic models for all A2A protocol data structures:

```python
from a2a.models.message import Message, MessageRole, TextPart
from a2a.models.agent_card import AgentCard, AgentCapabilities
from a2a.models.task import Task, TaskStatus, TaskState

# Create a message
message = Message(
    role=MessageRole.USER,
    parts=[TextPart(text="Hello, world!")]
)
```

### Client

Use the A2A client to communicate with agents:

```python
from a2a.client.a2a_client import A2AClient

async with A2AClient("http://localhost:8000/echo") as client:
    # Get agent capabilities
    card = await client.get_agent_card()
    
    # Send a message
    response = await client.send_message(message)
```

### Server

Build agents using the task manager and FastAPI integration:

```python
from fastapi import FastAPI
from a2a.server.task_manager import TaskManager
from a2a.integrations.fastapi import add_a2a_routes

app = FastAPI()
task_manager = TaskManager()

# Register message handler
async def process_message(message):
    # Your agent logic here
    return response_message

task_manager.on_message_received = process_message

# Add A2A routes
add_a2a_routes(app, task_manager, "/my-agent")
```

## Creating Custom Agents

### 1. Basic Message Handler

```python
async def process_message(message: Message) -> Message:
    # Extract text from message
    text_parts = [part for part in message.parts if part.type == "text"]
    input_text = text_parts[0].text if text_parts else ""
    
    # Process the input (your agent logic here)
    response_text = f"Processed: {input_text}"
    
    # Return response
    return Message(
        role=MessageRole.AGENT,
        message_id=str(uuid.uuid4()),
        context_id=message.context_id,
        parts=[TextPart(text=response_text)]
    )
```

### 2. Agent Card Handler

```python
async def get_agent_card(agent_url: str) -> AgentCard:
    return AgentCard(
        name="My Custom Agent",
        description="Description of what this agent does",
        url=agent_url,
        version="1.0.0",
        capabilities=AgentCapabilities(
            streaming=True,
            push_notifications=False
        ),
        default_input_modes=["text"],
        default_output_modes=["text"],
        skills=[]  # Define agent skills here
    )
```

### 3. Complete Agent Example

```python
from fastapi import FastAPI
from a2a.server.task_manager import TaskManager
from a2a.integrations.fastapi import add_a2a_routes

app = FastAPI()
task_manager = TaskManager()

# Register handlers
task_manager.on_message_received = process_message
task_manager.on_agent_card_query = get_agent_card

# Add routes
add_a2a_routes(app, task_manager, "/my-agent")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_basic.py

# Run with coverage
pytest --cov=src/a2a
```

### Writing Tests

```python
import pytest
from a2a.models.message import Message, MessageRole, TextPart

def test_message_creation():
    message = Message(
        role=MessageRole.USER,
        parts=[TextPart(text="Test")]
    )
    assert message.role == MessageRole.USER
    assert len(message.parts) == 1
```

## Development Tools

### Code Formatting

```bash
# Format code with Black
black src/ tests/ samples/

# Sort imports with isort
isort src/ tests/ samples/
```

### Type Checking

```bash
# Run mypy type checking
mypy src/
```

### Linting

```bash
# Run ruff linter
ruff check src/ tests/
```

## API Reference

### Client Methods

- `get_agent_card()` - Get agent capabilities
- `send_message(message)` - Send message, get response
- `send_message_stream(message)` - Send message, stream response
- `create_task(params)` - Create new task
- `get_task(task_id)` - Get task by ID
- `send_task_message(task_id, params)` - Send message to task
- `cancel_task(task_id)` - Cancel task

### Server Components

- `TaskManager` - Handles A2A protocol operations
- `TaskStore` - Interface for task persistence
- `InMemoryTaskStore` - In-memory task storage
- `add_a2a_routes()` - FastAPI integration

### Models

- `Message` - A2A protocol message
- `AgentCard` - Agent metadata and capabilities
- `Task` - Task with status and history
- `TextPart`, `FilePart`, `DataPart` - Message content types

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you installed the package with `pip install -e .`
2. **Connection refused**: Ensure the agent server is running
3. **Port conflicts**: Change the port in your agent or client code
4. **Dependency issues**: Update dependencies with `pip install -r requirements.txt`

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Testing Connectivity

```bash
# Test agent card endpoint
curl http://localhost:8000/echo/card

# Test health endpoint
curl http://localhost:8000/health
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Format your code
7. Submit a pull request

## Next Steps

- Explore the samples in `samples/`
- Read the A2A protocol specification at [a2a-protocol.org](https://a2a-protocol.org)
- Build your own custom agents
- Contribute to the project