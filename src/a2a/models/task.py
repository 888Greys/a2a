"""Task models for A2A protocol."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from enum import Enum
from .message import Message, Part


class TaskState(str, Enum):
    """Task state enumeration."""
    SUBMITTED = "submitted"
    WORKING = "working"
    INPUT_REQUIRED = "input-required"
    COMPLETED = "completed"
    CANCELED = "canceled"
    FAILED = "failed"
    UNKNOWN = "unknown"


class TaskStatus(BaseModel):
    """Task status information."""
    state: TaskState = Field(description="Current task state")
    message: Optional[Message] = Field(default=None, description="Status message")
    timestamp: datetime = Field(description="Status timestamp")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Artifact(BaseModel):
    """Task artifact."""
    name: Optional[str] = Field(default=None, description="Artifact name")
    description: Optional[str] = Field(default=None, description="Artifact description")
    parts: List[Part] = Field(description="Artifact content parts")
    index: int = Field(default=0, description="Artifact index")
    append: Optional[bool] = Field(default=None, description="Whether to append to existing artifact")
    last_chunk: Optional[bool] = Field(default=None, description="Whether this is the last chunk")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class Task(BaseModel):
    """A2A protocol task."""
    id: str = Field(description="Task identifier")
    session_id: Optional[str] = Field(default=None, description="Session identifier")
    status: TaskStatus = Field(description="Current task status")
    artifacts: Optional[List[Artifact]] = Field(default=None, description="Task artifacts")
    history: Optional[List[Message]] = Field(default=None, description="Task message history")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True


class TaskSendParams(BaseModel):
    """Parameters for sending a task message."""
    session_id: Optional[str] = Field(default=None, description="Session identifier")
    message: Message = Field(description="Message to send")
    push_notification: Optional[Dict[str, Any]] = Field(default=None, description="Push notification config")


class TaskQueryParams(BaseModel):
    """Parameters for querying a task."""
    id: str = Field(description="Task identifier")
    history_length: Optional[int] = Field(default=None, description="Length of history to retrieve")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class TaskStatusUpdateEvent(BaseModel):
    """Task status update event for streaming."""
    id: str = Field(description="Task identifier")
    status: TaskStatus = Field(description="Updated task status")
    final: bool = Field(default=False, description="Whether this is the final update")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class TaskArtifactUpdateEvent(BaseModel):
    """Task artifact update event for streaming."""
    id: str = Field(description="Task identifier")
    artifact: Artifact = Field(description="Updated artifact")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")