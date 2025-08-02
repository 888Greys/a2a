"""Simple echo agent implementation using A2A Python SDK."""

import uuid
from fastapi import FastAPI
from a2a.server.task_manager import TaskManager
from a2a.models.message import Message, MessageRole, TextPart
from a2a.models.agent_card import AgentCard, AgentCapabilities
from a2a.integrations.fastapi import add_a2a_routes


# Create FastAPI app
app = FastAPI(
    title="A2A Echo Agent",
    description="A simple echo agent that repeats messages back to the user",
    version="1.0.0"
)

# Create task manager
task_manager = TaskManager()


async def process_message(message: Message) -> Message:
    """
    Process an incoming message and return an echo response.
    
    Args:
        message: The incoming message
        
    Returns:
        Message: Echo response
    """
    # Extract text from the message
    text_parts = [part for part in message.parts if part.type == "text"]
    if not text_parts:
        response_text = "Echo: (No text content found)"
    else:
        original_text = text_parts[0].text
        response_text = f"Echo: {original_text}"
    
    # Create response message
    return Message(
        role=MessageRole.AGENT,
        message_id=str(uuid.uuid4()),
        context_id=message.context_id,
        parts=[TextPart(text=response_text)]
    )


async def get_agent_card(agent_url: str) -> AgentCard:
    """
    Return agent card with capabilities and metadata.
    
    Args:
        agent_url: The URL where this agent is hosted
        
    Returns:
        AgentCard: Agent capabilities and metadata
    """
    return AgentCard(
        name="Echo Agent",
        description="A simple agent that echoes messages back to the user",
        url=agent_url,
        version="1.0.0",
        capabilities=AgentCapabilities(
            streaming=True,
            push_notifications=False,
            state_transition_history=False
        ),
        default_input_modes=["text"],
        default_output_modes=["text"],
        skills=[]
    )


# Register handlers with task manager
task_manager.on_message_received = process_message
task_manager.on_agent_card_query = get_agent_card

# Add A2A routes to the FastAPI app
add_a2a_routes(app, task_manager, "/echo")

# Add a root endpoint for basic info
@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "name": "A2A Echo Agent",
        "description": "A simple echo agent implementation",
        "version": "1.0.0",
        "agent_endpoint": "/echo",
        "agent_card": "/echo/card"
    }


# Add health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "a2a-echo-agent"}


if __name__ == "__main__":
    import uvicorn
    
    print("Starting A2A Echo Agent...")
    print("Agent will be available at: http://localhost:8000/echo")
    print("Agent card: http://localhost:8000/echo/card")
    print("Health check: http://localhost:8000/health")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )