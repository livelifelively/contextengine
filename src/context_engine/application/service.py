def create_greeting(name: str) -> str:
    """
    Creates a greeting for the given name.
    """
    return f"Hello, {name}!"


def get_initial_context() -> str:
    """
    Reads the context-engine.md file and returns its content.
    """
    with open("context-engine.md", "r") as f:
        return f.read()
