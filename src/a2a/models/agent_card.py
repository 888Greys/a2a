"""Agent card models for A2A protocol."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AgentCapabilities(BaseModel):
    """Agent capabilities specification."""
    streaming: bool = Field(default=False, description="Supports streaming responses")
    push_notifications: bool = Field(default=False, description="Supports push notifications")
    state_transition_history: bool = Field(default=False, description="Supports state transition history")


class AgentProvider(BaseModel):
    """Agent provider information."""
    organization: str = Field(description="Organization name")
    url: Optional[str] = Field(default=None, description="Organization URL")


class AgentAuthentication(BaseModel):
    """Agent authentication configuration."""
    schemes: List[str] = Field(description="Supported authentication schemes")
    credentials: Optional[str] = Field(default=None, description="Authentication credentials")


class AgentSkill(BaseModel):
    """Agent skill definition."""
    id: str = Field(description="Skill identifier")
    name: str = Field(description="Skill name")
    description: Optional[str] = Field(default=None, description="Skill description")
    tags: Optional[List[str]] = Field(default=None, description="Skill tags")
    examples: Optional[List[str]] = Field(default=None, description="Usage examples")
    input_modes: Optional[List[str]] = Field(default=None, description="Supported input modes")
    output_modes: Optional[List[str]] = Field(default=None, description="Supported output modes")


class AgentCard(BaseModel):
    """Agent card containing metadata and capabilities."""
    name: str = Field(description="Agent name")
    description: Optional[str] = Field(default=None, description="Agent description")
    url: str = Field(description="Agent URL")
    provider: Optional[AgentProvider] = Field(default=None, description="Agent provider")
    version: str = Field(description="Agent version")
    documentation_url: Optional[str] = Field(default=None, description="Documentation URL")
    capabilities: AgentCapabilities = Field(description="Agent capabilities")
    authentication: Optional[AgentAuthentication] = Field(default=None, description="Authentication info")
    default_input_modes: List[str] = Field(default=["text"], description="Default input modes")
    default_output_modes: List[str] = Field(default=["text"], description="Default output modes")
    skills: List[AgentSkill] = Field(default=[], description="Agent skills")