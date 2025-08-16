"""
Pytest configuration and shared fixtures for the test suite.
"""

import pytest
from fastmcp import Client
from context_engine.main import mcp


@pytest.fixture(scope="session")
def mcp_server():
    """Fixture to provide the MCP server instance for testing."""
    return mcp


@pytest.fixture
async def async_mcp_client(mcp_server):
    """Fixture to provide an async MCP client for testing."""
    client = Client(mcp_server)
    async with client:
        yield client


# Configure pytest for better async handling
@pytest.fixture(scope="session", autouse=True)
def configure_async_environment():
    """Configure the async environment for all tests."""
    import asyncio
    import sys

    # Set event loop policy if needed (Windows only)
    if sys.platform == "win32" and hasattr(asyncio, "WindowsProactorEventLoopPolicy"):
        # On Windows, use a more reliable event loop
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
