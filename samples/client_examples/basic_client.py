"""Basic A2A client example."""

import asyncio
import uuid
from a2a.client.a2a_client import A2AClient
from a2a.client.card_resolver import A2ACardResolver
from a2a.models.message import Message, MessageRole, TextPart
from a2a.models.task import TaskSendParams
from a2a.exceptions import A2AClientException, TaskNotFoundException


async def demonstrate_agent_discovery():
    """Demonstrate agent discovery capabilities."""
    print("=== Agent Discovery ===")
    
    try:
        # Create card resolver
        resolver = A2ACardResolver("http://localhost:8000")
        
        # Get agent card
        agent_card = await resolver.get_agent_card("/echo")
        print(f"Found agent: {agent_card.name}")
        print(f"Description: {agent_card.description}")
        print(f"Version: {agent_card.version}")
        print(f"Capabilities: {agent_card.capabilities.model_dump()}")
        print(f"Skills: {len(agent_card.skills)} skills available")
        
        await resolver.close()
        
    except A2AClientException as e:
        print(f"Error discovering agent: {e}")


async def demonstrate_message_communication():
    """Demonstrate direct message communication."""
    print("\n=== Message Communication ===")
    
    try:
        # Create client
        client = A2AClient("http://localhost:8000/echo")
        
        # Create a message
        message = Message(
            role=MessageRole.USER,
            message_id=str(uuid.uuid4()),
            context_id=str(uuid.uuid4()),
            parts=[TextPart(text="Hello from Python A2A client!")]
        )
        
        print(f"Sending message: {message.parts[0].text}")
        
        # Send message and get response
        response = await client.send_message(message)
        print(f"Received response: {response.parts[0].text}")
        
        await client.close()
        
    except A2AClientException as e:
        print(f"Error in message communication: {e}")


async def demonstrate_streaming_communication():
    """Demonstrate streaming message communication."""
    print("\n=== Streaming Communication ===")
    
    try:
        # Create client
        client = A2AClient("http://localhost:8000/echo")
        
        # Create a message
        message = Message(
            role=MessageRole.USER,
            message_id=str(uuid.uuid4()),
            context_id=str(uuid.uuid4()),
            parts=[TextPart(text="Hello from streaming client!")]
        )
        
        print(f"Sending streaming message: {message.parts[0].text}")
        
        # Send message and stream response
        async for event in client.send_message_stream(message):
            print(f"Streaming event: {event}")
        
        await client.close()
        
    except A2AClientException as e:
        print(f"Error in streaming communication: {e}")


async def demonstrate_task_communication():
    """Demonstrate task-based communication."""
    print("\n=== Task Communication ===")
    
    try:
        # Create client
        client = A2AClient("http://localhost:8000/echo")
        
        # Create task parameters
        message = Message(
            role=MessageRole.USER,
            message_id=str(uuid.uuid4()),
            context_id=str(uuid.uuid4()),
            parts=[TextPart(text="Hello from task-based client!")]
        )
        
        task_params = TaskSendParams(
            session_id=str(uuid.uuid4()),
            message=message
        )
        
        print(f"Creating task with message: {message.parts[0].text}")
        
        # Create task
        task = await client.create_task(task_params)
        print(f"Created task: {task.id}")
        print(f"Task status: {task.status.state}")
        
        # Get task details
        retrieved_task = await client.get_task(task.id)
        print(f"Retrieved task history length: {len(retrieved_task.history or [])}")
        
        if retrieved_task.history:
            for i, msg in enumerate(retrieved_task.history):
                print(f"  Message {i+1} ({msg.role}): {msg.parts[0].text}")
        
        await client.close()
        
    except A2AClientException as e:
        print(f"Error in task communication: {e}")
    except TaskNotFoundException as e:
        print(f"Task not found: {e}")


async def demonstrate_task_streaming():
    """Demonstrate task-based streaming communication."""
    print("\n=== Task Streaming Communication ===")
    
    try:
        # Create client
        client = A2AClient("http://localhost:8000/echo")
        
        # Create initial task
        message = Message(
            role=MessageRole.USER,
            message_id=str(uuid.uuid4()),
            context_id=str(uuid.uuid4()),
            parts=[TextPart(text="Initial task message")]
        )
        
        task_params = TaskSendParams(
            session_id=str(uuid.uuid4()),
            message=message
        )
        
        task = await client.create_task(task_params)
        print(f"Created task: {task.id}")
        
        # Send another message to the task with streaming
        follow_up_message = Message(
            role=MessageRole.USER,
            message_id=str(uuid.uuid4()),
            context_id=str(uuid.uuid4()),
            parts=[TextPart(text="Follow-up streaming message")]
        )
        
        follow_up_params = TaskSendParams(
            message=follow_up_message
        )
        
        print(f"Sending follow-up message: {follow_up_message.parts[0].text}")
        
        # Stream the response
        async for event in client.send_task_message_stream(task.id, follow_up_params):
            print(f"Task streaming event: {event}")
        
        await client.close()
        
    except A2AClientException as e:
        print(f"Error in task streaming: {e}")


async def main():
    """Run all demonstration examples."""
    print("A2A Python Client Examples")
    print("=" * 50)
    print("Make sure the echo agent is running at http://localhost:8000/echo")
    print("You can start it with: python samples/echo_agent/main.py")
    print()
    
    # Run all demonstrations
    await demonstrate_agent_discovery()
    await demonstrate_message_communication()
    await demonstrate_streaming_communication()
    await demonstrate_task_communication()
    await demonstrate_task_streaming()
    
    print("\n=== All Examples Completed ===")


if __name__ == "__main__":
    asyncio.run(main())