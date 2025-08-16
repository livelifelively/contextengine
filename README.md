# Context Engine

Context Engine helps you create and manage documentation-driven development workflows. Documentations are funneled for efficient code generation and high maintainability through the Model Context Protocol (MCP).

## Features

- 🚀 **FastMCP Integration**: Built on FastMCP for high-performance Model Context Protocol server
- 🔧 **Tool Framework**: Extensible tool system for AI interactions
- 📚 **Documentation-Driven**: Focus on maintainable, well-documented development workflows
- 🧪 **Robust Testing**: Comprehensive test suite with async support
- 🛠️ **Developer Tools**: Integrated linting, formatting, and type checking

## Requirements

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd context-engine
```

### 2. Install Dependencies

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Set up the development environment
just install
```

Or manually:

```bash
uv venv
uv sync
```

### 3. Verify Installation

```bash
# Run tests to verify everything works
just test

# Run all quality checks
just check
```

## Development

This project uses `just` for task automation. Available commands:

```bash
just install     # Set up development environment
just test        # Run all tests
just lint        # Run linter with auto-fix
just format      # Format code
just type-check  # Run type checker
just check       # Run all quality checks + tests
```

## Running the MCP Server

### Start the Server

```bash
# Using the installed console script (recommended)
uv run context-engine

# Or using Python module directly
uv run python -m context_engine.main
```

The server will start and listen for MCP connections.

## Connecting to MCP Clients

### Claude Desktop

1. **Locate your Claude Desktop config file:**
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add the Context Engine server to your config:**

```json
{
  "mcpServers": {
    "context-engine": {
      "command": "uv",
      "args": ["run", "context-engine"],
      "cwd": "/path/to/your/context-engine"
    }
  }
}
```

3. **Restart Claude Desktop** to load the new server.

### Cline (VS Code Extension)

1. **Install the Cline extension** in VS Code
2. **Open Command Palette** (`Cmd+Shift+P` / `Ctrl+Shift+P`)
3. **Run "Cline: Configure MCP Servers"**
4. **Add server configuration:**

```json
{
  "context-engine": {
    "command": "uv",
    "args": ["run", "context-engine"],
    "cwd": "/path/to/your/context-engine"
  }
}
```

### Cursor

1. **Open Cursor Settings** (`Cmd+,` / `Ctrl+,`)
2. **Navigate to MCP Settings** or create a `.cursor-mcp.json` file in your project root:

```json
{
  "mcpServers": {
    "context-engine": {
      "command": "uv",
      "args": ["run", "context-engine"],
      "cwd": "/path/to/your/context-engine"
    }
  }
}
```

### Other MCP Clients

For any MCP-compatible client, use these connection parameters:

- **Command**: `uv`
- **Arguments**: `["run", "context-engine"]`
- **Working Directory**: `/path/to/your/context-engine`

Alternative (if console script doesn't work):
- **Command**: `uv`
- **Arguments**: `["run", "python", "-m", "context_engine.main"]`
- **Working Directory**: `/path/to/your/context-engine`

## Available Tools

### `greet`

A simple greeting tool that demonstrates the MCP integration.

**Parameters:**
- `name` (string): The name to greet

**Example:**
```json
{
  "name": "greet",
  "arguments": {
    "name": "World"
  }
}
```

**Response:**
```json
{
  "data": "Hello, World!"
}
```

## Project Structure

```
context-engine/
├── src/
│   └── context_engine/
│       └── main.py          # Main MCP server
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test configuration
│   └── test_main.py         # Test suite
├── docs/                    # Documentation
├── pyproject.toml           # Project configuration
├── justfile                 # Task automation
├── uv.lock                  # Dependency lock file
└── README.md               # This file
```

## Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Run quality checks**: `just check`
5. **Submit a pull request**

### Code Quality

This project maintains high code quality standards:

- **Linting**: Ruff for fast Python linting
- **Formatting**: Ruff for consistent code formatting
- **Type Checking**: Pyright for static type analysis
- **Testing**: Pytest with async support and comprehensive coverage

All quality checks must pass before merging.

## Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Ensure you're using uv run
uv run python -m context_engine.main
```

**2. Test Failures**
```bash
# Run tests with verbose output
just test
# Or manually
uv run pytest tests/ -v
```

**3. MCP Client Connection Issues**
- Verify the server path in your client configuration
- Check that uv is installed and accessible
- Ensure the working directory is correct

**4. Development Environment Issues**
```bash
# Clean install
rm -rf .venv
just install
```

### Getting Help

- Check the [FastMCP documentation](https://github.com/simonthrane/fastmcp)
- Review the [Model Context Protocol specification](https://modelcontextprotocol.io/)
- File issues in this repository for project-specific problems

## License

[Add your license information here]

## Acknowledgments

- Built with [FastMCP](https://github.com/simonthrane/fastmcp)
- Follows [Model Context Protocol](https://modelcontextprotocol.io/) standards
- Uses [uv](https://docs.astral.sh/uv/) for dependency management