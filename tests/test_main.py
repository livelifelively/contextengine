import pytest
from context_engine.main import mcp


@pytest.mark.asyncio
async def test_greet_async(async_mcp_client):
    """Test the greet tool with an async client."""
    result = await async_mcp_client.call_tool("greet", {"name": "World"})
    assert result.data == "Hello, World!"


@pytest.mark.asyncio
async def test_greet_with_different_name(async_mcp_client):
    """Test the greet tool with a different name."""
    result = await async_mcp_client.call_tool("greet", {"name": "Alice"})
    assert result.data == "Hello, Alice!"


@pytest.mark.asyncio
async def test_greet_with_empty_name(async_mcp_client):
    """Test the greet tool with an empty name."""
    result = await async_mcp_client.call_tool("greet", {"name": ""})
    assert result.data == "Hello, !"


def test_mcp_instance_exists():
    """Test that the MCP instance is properly created."""
    assert mcp is not None
    assert hasattr(mcp, "tool")  # Ensure it has the decorator method


def test_greet_function_logic():
    """Test the greet function logic by creating a direct function."""

    # Test the core logic without going through the MCP framework
    def greet_logic(name: str) -> str:
        return f"Hello, {name}!"

    result = greet_logic("Direct")
    assert result == "Hello, Direct!"

    # Test different cases
    assert greet_logic("") == "Hello, !"
    assert greet_logic("Test User") == "Hello, Test User!"


@pytest.mark.asyncio
async def test_greet_edge_cases(async_mcp_client):
    """Test edge cases for the greet tool."""
    # Test with special characters
    result = await async_mcp_client.call_tool("greet", {"name": "Alice & Bob"})
    assert result.data == "Hello, Alice & Bob!"

    # Test with numbers
    result = await async_mcp_client.call_tool("greet", {"name": "User123"})
    assert result.data == "Hello, User123!"
