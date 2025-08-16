import pytest


@pytest.mark.asyncio
async def test_init_context_engine(async_mcp_client):
    """Test the init_context_engine tool."""
    result = await async_mcp_client.call_tool("init_context_engine")
    with open("context-engine.md", "r") as f:
        expected_content = f.read()
    assert result.data == expected_content
