from fastmcp import FastMCP

mcp = FastMCP("Context Engine")


@mcp.tool
def greet(name: str) -> str:
    """
    Returns a greeting to the given name.
    """
    return f"Hello, {name}!"


def main():
    """Entry point for the Context Engine MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
