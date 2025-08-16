from context_engine.application.service import create_greeting


def greet(name: str) -> str:
    """
    Returns a greeting to the given name.
    """
    return create_greeting(name)
