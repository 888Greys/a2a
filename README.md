# 🍮 PomPom-A2A

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![PyPI Version](https://img.shields.io/pypi/v/pompompurin-a2a.svg)](https://pypi.org/project/pompompurin-a2a/)
[![Tests](https://github.com/yourusername/pompompurin-a2a/workflows/tests/badge.svg)](https://github.com/yourusername/pompompurin-a2a/actions)

> *A delightfully simple Python SDK for the Agent2Agent (A2A) protocol, as sweet and reliable as Pompompurin himself! 🐶*

**PomPom-A2A** makes building AI agents as easy as enjoying a pudding! This Python SDK provides a complete, production-ready implementation of the [Agent2Agent (A2A) Protocol](https://a2a-protocol.org), enabling seamless communication between AI agents and applications.

## ✨ Why PomPom-A2A?

- 🍮 **Sweet & Simple**: Clean, intuitive API that's easy to learn
- 🚀 **Production Ready**: Battle-tested with comprehensive test suite
- 🔄 **Full A2A Support**: Complete protocol v0.2.6 implementation
- ⚡ **Async First**: Built for modern Python with async/await
- 🎯 **Type Safe**: Full type hints with Pydantic validation
- 🌐 **Framework Agnostic**: Works with FastAPI, Flask, Django
- 🤖 **AI Ready**: Perfect for LangChain, OpenAI, and other AI frameworks

## 🚀 Quick Start

### Installation

```bash
pip install pompompurin-a2a
```

### Create Your First Agent (30 seconds!)

```python
from fastapi import FastAPI
from pompompurin_a2a import TaskManager, Message, MessageRole, TextPart, AgentCard, AgentCapabilities
from pompompurin_a2a.integrations.fastapi import add_a2a_routes

app = FastAPI()
task_manager = TaskManager()

# Define your agent's behavior
async def my_agent_logic(message: Message) -> Message:
    user_text = message.parts[0].text
    response = f"🍮 PomPom says: I received '{user_text}'"
    
    return Message(
        role=MessageRole.AGENT,
        parts=[TextPart(text=response)]
    )

# Define your agent's capabilities
async def get_agent_info(agent_url: str) -> AgentCard:
    return AgentCard(
        name="My PomPom Agent",
        description="A friendly agent powered by PomPom-A2A",
        url=agent_url,
        version="1.0.0",
        capabilities=AgentCapabilities(streaming=True),
        skills=[]
    )

# Wire everything up
task_manager.on_message_received = my_agent_logic
task_manager.on_agent_card_query = get_agent_info
add_a2a_routes(app, task_manager, "/my-agent")

# Run with: uvicorn main:app --reload
```

### Test Your Agent

```python
import asyncio
from pompompurin_a2a import A2AClient, Message, MessageRole, TextPart

async def test_agent():
    async with A2AClient("http://localhost:8000/my-agent") as client:
        # Discover agent capabilities
        card = await client.get_agent_card()
        print(f"Connected to: {card.name}")
        
        # Send a message
        message = Message(
            role=MessageRole.USER,
            parts=[TextPart(text="Hello PomPom!")]
        )
        response = await client.send_message(message)
        print(f"Agent replied: {response.parts[0].text}")

asyncio.run(test_agent())
```

## 🎯 Use Cases

### 🤖 AI-Powered Agents
```python
import openai

async def ai_chat_agent(message: Message) -> Message:
    response = await openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message.parts[0].text}]
    )
    return Message(
        role=MessageRole.AGENT,
        parts=[TextPart(text=response.choices[0].message.content)]
    )
```

### 🔍 Specialized Service Agents
```python
async def weather_agent(message: Message) -> Message:
    location = extract_location(message.parts[0].text)
    weather = await get_weather_data(location)
    return Message(
        role=MessageRole.AGENT,
        parts=[TextPart(text=f"Weather in {location}: {weather}")]
    )
```

### 📊 Data Analysis Agents
```python
async def data_analyst_agent(message: Message) -> Message:
    # Handle CSV uploads, perform analysis
    if has_file_attachment(message):
        data = load_csv_from_message(message)
        insights = analyze_data(data)
        return create_analysis_response(insights)
```

### 🔗 Agent Orchestration
```python
async def orchestrator_agent(message: Message) -> Message:
    # Route to specialized agents based on intent
    intent = classify_intent(message.parts[0].text)
    
    if intent == "weather":
        return await call_agent("http://weather-agent:8000", message)
    elif intent == "code_review":
        return await call_agent("http://code-agent:8000", message)
    else:
        return await call_agent("http://general-agent:8000", message)
```

## 📚 Core Concepts

### Messages
```python
from pompompurin_a2a import Message, MessageRole, TextPart, FilePart

# Text message
message = Message(
    role=MessageRole.USER,
    parts=[TextPart(text="Hello!")]
)

# Multi-modal message
message = Message(
    role=MessageRole.USER,
    parts=[
        TextPart(text="Analyze this image:"),
        FilePart(file={"uri": "https://example.com/image.jpg"})
    ]
)
```

### Tasks (Stateful Conversations)
```python
# Create a persistent conversation
task = await client.create_task(TaskSendParams(
    session_id="user-123",
    message=initial_message
))

# Continue the conversation
response = await client.send_task_message(
    task.id, 
    TaskSendParams(message=follow_up_message)
)
```

### Streaming Responses
```python
# Stream real-time responses
async for event in client.send_message_stream(message):
    if event.get("type") == "message":
        print(f"Streaming: {event['data']['parts'][0]['text']}")
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Your Agent    │    │   PomPom-A2A    │    │   A2A Client    │
│                 │    │      SDK        │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │   Agent     │◄┼────┼►│ TaskManager │◄┼────┼►│ A2AClient   │ │
│ │   Logic     │ │    │ │             │ │    │ │             │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
│                 │    │ ┌─────────────┐ │    │                 │
│ ┌─────────────┐ │    │ │  FastAPI    │ │    │                 │
│ │ Agent Card  │◄┼────┼►│ Integration │ │    │                 │
│ │   Config    │ │    │ │             │ │    │                 │
│ └─────────────┘ │    │ └─────────────┘ │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Advanced Features

### Custom Task Storage
```python
from pompompurin_a2a.server import TaskStore

class DatabaseTaskStore(TaskStore):
    async def create_task(self, task: Task) -> Task:
        # Store in your database
        return await self.db.save_task(task)

task_manager = TaskManager(task_store=DatabaseTaskStore())
```

### Middleware & Authentication
```python
from fastapi import Depends, HTTPException

async def verify_api_key(api_key: str = Header(...)):
    if not is_valid_api_key(api_key):
        raise HTTPException(401, "Invalid API key")

# Add authentication to your agent
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Your auth logic here
    return await call_next(request)
```

### Multi-Agent Systems
```python
# Agent discovery and communication
resolver = A2ACardResolver("http://agent-registry:8000")
available_agents = await resolver.discover_agents([
    "/weather", "/translator", "/calculator"
])

for path, card in available_agents.items():
    print(f"Found {card.name} at {path}")
```

## 🚀 Deployment

### Docker
```dockerfile
FROM python:3.12-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose (Multi-Agent Setup)
```yaml
version: '3.8'
services:
  weather-agent:
    build: ./weather-agent
    ports: ["8001:8000"]
  
  chat-agent:
    build: ./chat-agent
    ports: ["8002:8000"]
  
  orchestrator:
    build: ./orchestrator
    ports: ["8000:8000"]
    depends_on: [weather-agent, chat-agent]
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pompom-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pompom-agent
  template:
    metadata:
      labels:
        app: pompom-agent
    spec:
      containers:
      - name: agent
        image: your-registry/pompom-agent:latest
        ports:
        - containerPort: 8000
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src/pompompurin_a2a

# Run specific test
pytest tests/test_client.py::test_send_message
```

### Testing Your Agents
```python
import pytest
from pompompurin_a2a.testing import MockA2AClient

@pytest.mark.asyncio
async def test_my_agent():
    client = MockA2AClient()
    response = await client.send_message(test_message)
    assert "expected response" in response.parts[0].text
```

## 🔮 Roadmap & Future Implementations

### 🚧 Coming Soon (v0.2.0)
- [ ] **WebSocket Support** - Real-time bidirectional communication
- [ ] **Agent Registry** - Centralized agent discovery service
- [ ] **Load Balancing** - Distribute requests across agent instances
- [ ] **Circuit Breaker** - Fault tolerance for agent communication
- [ ] **Metrics & Monitoring** - Prometheus/Grafana integration

### 🎯 Planned Features (v0.3.0)
- [ ] **Agent Marketplace** - Share and discover community agents
- [ ] **Visual Agent Builder** - GUI for creating agents
- [ ] **Agent Chains** - Visual workflow builder
- [ ] **Multi-Modal Support** - Enhanced image/video/audio handling
- [ ] **Agent Memory** - Long-term conversation memory

### 🌟 Advanced Integrations (v0.4.0)
- [ ] **LangChain Integration** - Native LangChain agent wrapper
- [ ] **Hugging Face Hub** - Direct model integration
- [ ] **Vector Database** - Built-in RAG capabilities
- [ ] **Agent Analytics** - Performance insights and optimization
- [ ] **Enterprise Features** - SSO, audit logs, compliance

### 🔧 Developer Experience (Ongoing)
- [ ] **CLI Tool** - `pompom create-agent my-agent`
- [ ] **VS Code Extension** - Agent development tools
- [ ] **Agent Templates** - Pre-built agent templates
- [ ] **Hot Reload** - Development mode with auto-restart
- [ ] **Debug Dashboard** - Real-time agent debugging

### 🌐 Ecosystem Expansions
- [ ] **JavaScript SDK** - Browser and Node.js support
- [ ] **Go SDK** - High-performance agent runtime
- [ ] **Rust SDK** - Ultra-fast agent core
- [ ] **Mobile SDKs** - iOS and Android agent clients

## 📖 Examples Repository

Check out our [examples repository](https://github.com/yourusername/pompompurin-a2a-examples) for:

- 🤖 **AI Chat Agents** (OpenAI, Anthropic, Local LLMs)
- 🌤️ **Weather Service Agent**
- 📊 **Data Analysis Agent**
- 🔍 **Web Scraping Agent**
- 🎨 **Image Generation Agent**
- 🔗 **Multi-Agent Orchestration**
- 📱 **Mobile App Integration**
- 🐳 **Docker Deployment Examples**

## 🤝 Contributing

We love contributions! Here's how you can help make PomPom-A2A even better:

### 🐛 Bug Reports
Found a bug? [Open an issue](https://github.com/yourusername/pompompurin-a2a/issues) with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details

### ✨ Feature Requests
Have an idea? [Start a discussion](https://github.com/yourusername/pompompurin-a2a/discussions) or open an issue!

### 🔧 Development Setup
```bash
git clone https://github.com/yourusername/pompompurin-a2a.git
cd pompompurin-a2a
pip install -e ".[dev]"
pytest  # Run tests
```

### 📝 Documentation
Help improve our docs:
- Fix typos or unclear explanations
- Add examples and use cases
- Translate to other languages

## 🏆 Community

- 💬 **Discord**: [Join our community](https://discord.gg/pompom-a2a)
- 🐦 **Twitter**: [@PomPomA2A](https://twitter.com/PomPomA2A)
- 📧 **Email**: team@pompom-a2a.dev
- 📖 **Blog**: [pompom-a2a.dev/blog](https://pompom-a2a.dev/blog)

## 📄 License

This project is licensed under the [Apache 2.0 License](LICENSE) - see the LICENSE file for details.

## 🙏 Acknowledgements

- Inspired by the adorable [Pompompurin](https://www.sanrio.com/characters/pompompurin) 🍮
- Built on the [A2A Protocol](https://a2a-protocol.org) specification
- Thanks to the [A2A .NET SDK](https://github.com/a2aproject/a2a-dotnet) for inspiration
- Special thanks to all our [contributors](https://github.com/yourusername/pompompurin-a2a/graphs/contributors)

---

<div align="center">

**Made with 💖 and 🍮 by the PomPom-A2A Team**

*Building the future of agent communication, one pudding at a time!*

[⭐ Star us on GitHub](https://github.com/yourusername/pompompurin-a2a) | [📦 Install from PyPI](https://pypi.org/project/pompompurin-a2a/) | [📚 Read the Docs](https://github.com/yourusername/pompompurin-a2a#readme)

</div>