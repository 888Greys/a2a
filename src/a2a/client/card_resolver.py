"""A2A agent card resolver for discovering agent capabilities."""

from typing import Optional, Dict, Any
import httpx
from ..models.agent_card import AgentCard
from ..exceptions import A2AClientException


class A2ACardResolver:
    """Resolves agent card information from A2A-compatible endpoints."""

    def __init__(
        self, 
        base_url: str, 
        timeout: float = 30.0,
        headers: Optional[Dict[str, str]] = None
    ):
        """
        Initialize card resolver.
        
        Args:
            base_url: Base URL to resolve agent cards from
            timeout: Request timeout in seconds
            headers: Additional headers to include in requests
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.headers = headers or {}
        self.client = httpx.AsyncClient(
            timeout=timeout,
            headers=self.headers
        )

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def get_agent_card(self, agent_path: str = "") -> AgentCard:
        """
        Get agent card from the specified path.
        
        Args:
            agent_path: Optional path to append to base URL (e.g., "/echo")
            
        Returns:
            AgentCard: Agent capabilities and metadata
            
        Raises:
            A2AClientException: If the request fails or agent card is invalid
        """
        try:
            url = f"{self.base_url}{agent_path}/card"
            response = await self.client.get(url)
            response.raise_for_status()
            
            card_data = response.json()
            return AgentCard(**card_data)
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise A2AClientException(f"Agent card not found at {url}")
            else:
                raise A2AClientException(f"HTTP error {e.response.status_code} getting agent card")
        except httpx.RequestError as e:
            raise A2AClientException(f"Request failed: {str(e)}")
        except ValueError as e:
            raise A2AClientException(f"Invalid agent card format: {str(e)}")
        except Exception as e:
            raise A2AClientException(f"Unexpected error: {str(e)}")

    async def discover_agents(self, paths: Optional[list[str]] = None) -> Dict[str, AgentCard]:
        """
        Discover multiple agents from different paths.
        
        Args:
            paths: List of paths to check for agents (e.g., ["/echo", "/researcher"])
                  If None, will try to discover from common paths
            
        Returns:
            Dict[str, AgentCard]: Mapping of path to agent card
            
        Raises:
            A2AClientException: If discovery fails
        """
        if paths is None:
            # Common agent paths to try
            paths = [
                "",  # Root path
                "/echo",
                "/researcher", 
                "/assistant",
                "/agent"
            ]
        
        discovered_agents = {}
        
        for path in paths:
            try:
                agent_card = await self.get_agent_card(path)
                discovered_agents[path] = agent_card
            except A2AClientException:
                # Skip paths that don't have agents
                continue
        
        return discovered_agents

    async def validate_agent_endpoint(self, agent_path: str = "") -> bool:
        """
        Validate that an endpoint is a valid A2A agent.
        
        Args:
            agent_path: Optional path to append to base URL
            
        Returns:
            bool: True if endpoint is a valid A2A agent
        """
        try:
            await self.get_agent_card(agent_path)
            return True
        except A2AClientException:
            return False

    async def get_agent_capabilities(self, agent_path: str = "") -> Dict[str, Any]:
        """
        Get just the capabilities portion of an agent card.
        
        Args:
            agent_path: Optional path to append to base URL
            
        Returns:
            Dict[str, Any]: Agent capabilities
            
        Raises:
            A2AClientException: If the request fails
        """
        agent_card = await self.get_agent_card(agent_path)
        return agent_card.capabilities.model_dump()

    async def get_agent_skills(self, agent_path: str = "") -> list[Dict[str, Any]]:
        """
        Get the skills offered by an agent.
        
        Args:
            agent_path: Optional path to append to base URL
            
        Returns:
            List[Dict[str, Any]]: List of agent skills
            
        Raises:
            A2AClientException: If the request fails
        """
        agent_card = await self.get_agent_card(agent_path)
        return [skill.model_dump() for skill in agent_card.skills]