"""Basic tests for A2A Python SDK."""

import pytest
import uuid
from a2a.models.message import Message, MessageRole, TextPart
from a2a.models.agent_card import AgentCard, AgentCapabilities
from a2a.models.task import Task, TaskStatus, TaskState, TaskSendParams
from a2a.server.task_store import InMemoryTaskStore
from a2a.server.task_manager import TaskManager
from datetime import datetime


class TestModels:
    """Test data models."""
    
    def test_message_creation(self):
        """Test creating a message."""
        message = Message(
            role=MessageRole.USER,
            message_id=str(uuid.uuid4()),
            parts=[TextPart(text="Hello, world!")]
        )
        
        assert message.role == MessageRole.USER
        assert len(message.parts) == 1
        assert message.parts[0].text == "Hello, world!"
        assert message.parts[0].type == "text"
    
    def test_agent_card_creation(self):
        """Test creating an agent card."""
        card = AgentCard(
            name="Test Agent",
            description="A test agent",
            url="http://localhost:8000/test",
            version="1.0.0",
            capabilities=AgentCapabilities(streaming=True),
            skills=[]
        )
        
        assert card.name == "Test Agent"
        assert card.capabilities.streaming is True
        assert card.capabilities.push_notifications is False
    
    def test_task_creation(self):
        """Test creating a task."""
        task = Task(
            id=str(uuid.uuid4()),
            status=TaskStatus(
                state=TaskState.SUBMITTED,
                timestamp=datetime.utcnow()
            )
        )
        
        assert task.status.state == TaskState.SUBMITTED
        assert task.history is None
        assert task.artifacts is None


class TestTaskStore:
    """Test task store implementations."""
    
    @pytest.fixture
    def task_store(self):
        """Create a fresh task store for each test."""
        return InMemoryTaskStore()
    
    @pytest.fixture
    def sample_task(self):
        """Create a sample task for testing."""
        return Task(
            id="test-task-1",
            status=TaskStatus(
                state=TaskState.SUBMITTED,
                timestamp=datetime.utcnow()
            )
        )
    
    async def test_create_task(self, task_store, sample_task):
        """Test creating a task in the store."""
        created_task = await task_store.create_task(sample_task)
        assert created_task.id == sample_task.id
        assert await task_store.task_exists(sample_task.id)
    
    async def test_get_task(self, task_store, sample_task):
        """Test retrieving a task from the store."""
        await task_store.create_task(sample_task)
        retrieved_task = await task_store.get_task(sample_task.id)
        assert retrieved_task.id == sample_task.id
    
    async def test_update_task(self, task_store, sample_task):
        """Test updating a task in the store."""
        await task_store.create_task(sample_task)
        
        # Update the task
        sample_task.status.state = TaskState.COMPLETED
        updated_task = await task_store.update_task(sample_task)
        
        assert updated_task.status.state == TaskState.COMPLETED
        
        # Verify the update persisted
        retrieved_task = await task_store.get_task(sample_task.id)
        assert retrieved_task.status.state == TaskState.COMPLETED
    
    async def test_delete_task(self, task_store, sample_task):
        """Test deleting a task from the store."""
        await task_store.create_task(sample_task)
        assert await task_store.task_exists(sample_task.id)
        
        deleted = await task_store.delete_task(sample_task.id)
        assert deleted is True
        assert not await task_store.task_exists(sample_task.id)
    
    async def test_list_tasks(self, task_store):
        """Test listing tasks from the store."""
        # Create multiple tasks
        task1 = Task(
            id="task-1",
            session_id="session-1",
            status=TaskStatus(state=TaskState.SUBMITTED, timestamp=datetime.utcnow())
        )
        task2 = Task(
            id="task-2", 
            session_id="session-1",
            status=TaskStatus(state=TaskState.SUBMITTED, timestamp=datetime.utcnow())
        )
        task3 = Task(
            id="task-3",
            session_id="session-2", 
            status=TaskStatus(state=TaskState.SUBMITTED, timestamp=datetime.utcnow())
        )
        
        await task_store.create_task(task1)
        await task_store.create_task(task2)
        await task_store.create_task(task3)
        
        # List all tasks
        all_tasks = await task_store.list_tasks()
        assert len(all_tasks) == 3
        
        # List tasks by session
        session1_tasks = await task_store.list_tasks("session-1")
        assert len(session1_tasks) == 2
        
        session2_tasks = await task_store.list_tasks("session-2")
        assert len(session2_tasks) == 1


class TestTaskManager:
    """Test task manager functionality."""
    
    @pytest.fixture
    def task_manager(self):
        """Create a task manager for testing."""
        return TaskManager()
    
    async def test_process_message_without_handler(self, task_manager):
        """Test processing message without handler raises error."""
        message = Message(
            role=MessageRole.USER,
            parts=[TextPart(text="Test message")]
        )
        
        with pytest.raises(Exception):
            await task_manager.process_message(message)
    
    async def test_process_message_with_handler(self, task_manager):
        """Test processing message with handler."""
        # Set up a simple echo handler
        async def echo_handler(message: Message) -> Message:
            return Message(
                role=MessageRole.AGENT,
                parts=[TextPart(text=f"Echo: {message.parts[0].text}")]
            )
        
        task_manager.on_message_received = echo_handler
        
        message = Message(
            role=MessageRole.USER,
            parts=[TextPart(text="Hello")]
        )
        
        response = await task_manager.process_message(message)
        assert response.role == MessageRole.AGENT
        assert response.parts[0].text == "Echo: Hello"
    
    async def test_get_agent_card_with_handler(self, task_manager):
        """Test getting agent card with handler."""
        # Set up agent card handler
        async def card_handler(agent_url: str) -> AgentCard:
            return AgentCard(
                name="Test Agent",
                url=agent_url,
                version="1.0.0",
                capabilities=AgentCapabilities(),
                skills=[]
            )
        
        task_manager.on_agent_card_query = card_handler
        
        card = await task_manager.get_agent_card("http://localhost:8000/test")
        assert card.name == "Test Agent"
        assert card.url == "http://localhost:8000/test"