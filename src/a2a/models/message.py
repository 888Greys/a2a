"""Message models for A2A protocol."""

from typing import List, Optional, Union, Any, Dict
from pydantic import BaseModel, Field
from enum import Enum


class MessageRole(str, Enum):
    """Message role enumeration."""
    USER = "user"
    AGENT = "agent"


class TextPart(BaseModel):
    """Text content part of a message."""
    type: str = Field(default="text", description="Type of the part")
    text: str = Field(description="Text content")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class FileContent(BaseModel):
    """File content representation."""
    name: Optional[str] = Field(default=None, description="File name")
    mime_type: Optional[str] = Field(default=None, description="MIME type")
    bytes: Optional[str] = Field(default=None, description="Base64 encoded bytes")
    uri: Optional[str] = Field(default=None, description="URI to file")


class FilePart(BaseModel):
    """File content part of a message."""
    type: str = Field(default="file", description="Type of the part")
    file: FileContent = Field(description="File content")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class DataPart(BaseModel):
    """Data content part of a message."""
    type: str = Field(default="data", description="Type of the part")
    data: Dict[str, Any] = Field(description="Data content")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


# Union type for all part types
Part = Union[TextPart, FilePart, DataPart]


class Message(BaseModel):
    """A2A protocol message."""
    role: MessageRole = Field(description="Role of the message sender")
    parts: List[Part] = Field(description="Message content parts")
    message_id: Optional[str] = Field(default=None, description="Unique message identifier")
    context_id: Optional[str] = Field(default=None, description="Context identifier for conversation")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True