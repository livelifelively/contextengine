from fastmcp import FastMCP
from fastmcp.tools import Tool
from .tools.greet import greet
from .tools.context import init_context_engine

mcp = FastMCP("Context Engine")

mcp.add_tool(Tool.from_function(greet))
mcp.add_tool(Tool.from_function(init_context_engine))


def main():
    """Entry point for the Context Engine MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
