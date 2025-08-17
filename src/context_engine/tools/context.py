"""
Context Engine Tool - MCP Interface
Provides the init_context_engine tool for MCP clients
"""


def init_context_engine(random_string: str = "") -> str:
    """
    Initializes the conversation by providing the context of the Context Engine's principles and methodology.
    
    Args:
        random_string: Dummy parameter for no-parameter tools
        
    Returns:
        String containing the methodology context
    """
    try:
        context = """
# Context Engine - Documentation-Driven Development Workflow

## Overview
Context Engine helps you create and manage documentation-driven development workflows. 
Documentations are funneled for efficient code generation and high maintainability through the Model Context Protocol (MCP).

## Core Principles

### 1. Documentation-First Approach
- All development decisions should be documented before implementation
- Documentation serves as the single source of truth
- Code should reflect and implement documented requirements

### 2. MCP Integration
- Built on FastMCP for high-performance Model Context Protocol server
- Extensible tool system for AI interactions
- Seamless integration with MCP-compatible clients

### 3. Maintainable Workflows
- Focus on maintainable, well-documented development workflows
- Robust testing with comprehensive test suites
- Developer tools for linting, formatting, and type checking

## Available Tools

### greet
A simple greeting tool that demonstrates the MCP integration.
- **Parameters**: name (string) - The name to greet
- **Example**: `{"name": "World"}` returns `"Hello, World!"`

### init_context_engine
This tool that provides the full context of Context Engine principles and methodology.
- **Parameters**: random_string (string) - Dummy parameter for no-parameter tools
- **Returns**: Complete methodology context

## Development Workflow

1. **Document First**: Write clear documentation of what needs to be built
2. **Plan Architecture**: Design the system architecture based on documentation
3. **Implement**: Write code that implements the documented requirements
4. **Test**: Ensure code matches documented behavior
5. **Maintain**: Keep documentation and code in sync

## Best Practices

- Always document before coding
- Use clear, concise language in documentation
- Keep documentation close to code
- Regular reviews and updates of documentation
- Test documentation accuracy through implementation

## MCP Client Integration

This Context Engine MCP server can be integrated with:
- Claude Desktop
- Cline (VS Code Extension)
- Cursor
- Any MCP-compatible client

The server provides tools that help maintain documentation-driven development workflows and ensure high code quality through proper documentation practices.
"""
        
        return context.strip()
        
    except Exception as e:
        return f"❌ Error initializing Context Engine: {str(e)}"
