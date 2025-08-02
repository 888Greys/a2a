# 🍮 PomPom-A2A Examples

Welcome to the PomPom-A2A examples! This directory contains practical examples showing how to build different types of agents using the PomPom-A2A SDK.

## 🎯 Available Examples

### 🔄 Basic Examples (In `samples/`)
- **Echo Agent**: Simple agent that echoes messages back
- **Client Examples**: Comprehensive client usage demonstrations

### 🚀 Advanced Examples (Coming Soon)

#### 🤖 AI-Powered Agents
```
examples/
├── ai_chat_agent/          # OpenAI/Anthropic integration
├── local_llm_agent/        # Local LLM with Ollama
├── langchain_agent/        # LangChain integration
└── multimodal_agent/       # Text + image processing
```

#### 🔍 Specialized Agents
```
examples/
├── weather_agent/          # Weather service integration
├── code_review_agent/      # Code analysis and review
├── data_analyst_agent/     # CSV/data processing
├── translator_agent/       # Multi-language translation
├── summarizer_agent/       # Document summarization
└── search_agent/           # Web search integration
```

#### 🔗 Multi-Agent Systems
```
examples/
├── orchestrator_agent/     # Route to specialized agents
├── agent_chain/            # Sequential agent processing
├── agent_swarm/            # Parallel agent coordination
└── agent_marketplace/      # Agent discovery system
```

#### 🏢 Enterprise Examples
```
examples/
├── authenticated_agent/    # JWT/OAuth integration
├── rate_limited_agent/     # Rate limiting implementation
├── monitored_agent/        # Logging and metrics
├── database_agent/         # Persistent storage
└── microservice_agent/     # Kubernetes deployment
```

## 🚀 Quick Start

### 1. Run the Echo Agent
```bash
cd samples/echo_agent
python main.py
```

### 2. Test with Client
```bash
cd samples/client_examples
python basic_client.py
```

### 3. Create Your Own Agent
```bash
# Copy the echo agent as a template
cp -r samples/echo_agent my_custom_agent
cd my_custom_agent

# Edit main.py to implement your logic
# Then run it
python main.py
```

## 📚 Example Categories

### 🎓 Learning Examples
Perfect for understanding PomPom-A2A concepts:

1. **Hello World Agent** - Minimal agent implementation
2. **Echo Agent** - Basic message handling
3. **Stateful Agent** - Using tasks for conversation history
4. **Streaming Agent** - Real-time response streaming

### 🔧 Integration Examples
Show how to integrate with popular tools:

1. **OpenAI Agent** - GPT integration
2. **LangChain Agent** - LangChain wrapper
3. **Database Agent** - Persistent data storage
4. **API Agent** - External service integration

### 🏗️ Architecture Examples
Demonstrate advanced patterns:

1. **Microservice Agent** - Containerized deployment
2. **Load Balanced Agent** - Multiple instances
3. **Circuit Breaker Agent** - Fault tolerance
4. **Monitored Agent** - Observability

### 🎯 Use Case Examples
Real-world applications:

1. **Customer Service Bot** - Support automation
2. **Code Assistant** - Development helper
3. **Data Processor** - Analytics automation
4. **Content Creator** - Writing assistance

## 🛠️ Development Patterns

### Basic Agent Template
```python
from fastapi import FastAPI
from pompompurin_a2a import TaskManager, Message, MessageRole, TextPart
from pompompurin_a2a.integrations.fastapi import add_a2a_routes

app = FastAPI()
task_manager = TaskManager()

async def process_message(message: Message) -> Message:
    # Your agent logic here
    user_text = message.parts[0].text
    response_text = f"Processed: {user_text}"
    
    return Message(
        role=MessageRole.AGENT,
        parts=[TextPart(text=response_text)]
    )

async def get_agent_card(agent_url: str):
    return AgentCard(
        name="My Agent",
        description="Description of what this agent does",
        url=agent_url,
        version="1.0.0",
        capabilities=AgentCapabilities(streaming=True),
        skills=[]
    )

task_manager.on_message_received = process_message
task_manager.on_agent_card_query = get_agent_card
add_a2a_routes(app, task_manager, "/my-agent")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### AI Integration Pattern
```python
import openai

async def ai_agent(message: Message) -> Message:
    user_text = message.parts[0].text
    
    response = await openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_text}]
    )
    
    return Message(
        role=MessageRole.AGENT,
        parts=[TextPart(text=response.choices[0].message.content)]
    )
```

### Database Integration Pattern
```python
import asyncpg

class DatabaseAgent:
    def __init__(self):
        self.db_pool = None
    
    async def setup_database(self):
        self.db_pool = await asyncpg.create_pool(DATABASE_URL)
    
    async def process_message(self, message: Message) -> Message:
        # Store message in database
        async with self.db_pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO messages (content, timestamp) VALUES ($1, $2)",
                message.parts[0].text, datetime.utcnow()
            )
        
        # Process and return response
        return Message(
            role=MessageRole.AGENT,
            parts=[TextPart(text="Message stored and processed")]
        )
```

## 🧪 Testing Examples

### Unit Testing
```python
import pytest
from pompompurin_a2a import Message, MessageRole, TextPart

@pytest.mark.asyncio
async def test_agent_response():
    agent = MyAgent()
    message = Message(
        role=MessageRole.USER,
        parts=[TextPart(text="test input")]
    )
    
    response = await agent.process_message(message)
    assert response.role == MessageRole.AGENT
    assert "expected output" in response.parts[0].text
```

### Integration Testing
```python
import httpx
import pytest

@pytest.mark.asyncio
async def test_agent_endpoint():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/my-agent/card")
        assert response.status_code == 200
        
        card = response.json()
        assert card["name"] == "My Agent"
```

## 📦 Deployment Examples

### Docker
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  my-agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/agents
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: agents
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-agent
  template:
    metadata:
      labels:
        app: my-agent
    spec:
      containers:
      - name: agent
        image: my-agent:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
```

## 🤝 Contributing Examples

We welcome new examples! Here's how to contribute:

### 1. Create Your Example
```bash
# Create new example directory
mkdir examples/my_new_agent
cd examples/my_new_agent

# Create the basic structure
touch main.py requirements.txt README.md
```

### 2. Follow the Template
- Use the basic agent template above
- Include comprehensive documentation
- Add tests for your agent
- Provide deployment instructions

### 3. Submit a Pull Request
- Follow our contribution guidelines
- Include a clear description of your example
- Add your example to this README

## 📞 Getting Help

- **GitHub Issues**: Report bugs or request examples
- **GitHub Discussions**: Ask questions about examples
- **Discord**: Get real-time help from the community
- **Documentation**: Check the main README for detailed guides

## 🎉 Community Examples

Check out examples created by the community:

- [Awesome PomPom-A2A](https://github.com/pompom-a2a/awesome-pompom-a2a) - Curated list of community examples
- [Example Gallery](https://pompom-a2a.dev/examples) - Visual showcase of agents
- [Community Discord](https://discord.gg/pompom-a2a) - Share your creations

---

*Happy agent building! 🍮🤖*