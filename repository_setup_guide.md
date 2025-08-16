# Repository Setup Guide: Best Practices from basic-memory

This guide outlines the architecture and best practices from the `basic-memory` repository to help you initiate a new repository with a similar structure and workflow.

## 1. Directory Structure

The `basic-memory` repository follows a standard Python project layout:

```
.
├── .dockerignore
├── .gitignore
├── .python-version
├── docs/
├── src/
│   └── basic_memory/
│       ├── __init__.py
│       ├── api/
│       ├── cli/
│       └── ...
├── tests/
├── test-int/
├── pyproject.toml
├── uv.lock
├── justfile
└── Dockerfile
```

- **`src/`**: Contains the main application code, following the `src-layout` pattern. This separates the source code from other project files.
- **`tests/`**: Contains unit tests.
- **`test-int/`**: Contains integration tests.
- **`docs/`**: Contains project documentation.
- **`.python-version`**: Specifies the Python version for the project, used by tools like `pyenv`.
- **`pyproject.toml`**: The heart of the project's configuration, defining dependencies, build system, and tool settings.
- **`uv.lock`**: The lock file for dependencies, ensuring reproducible builds.
- **`justfile`**: A command runner for common development tasks.
- **`Dockerfile`**: Defines the containerized environment for the application.

## 2. Package and Environment Management

The project uses `uv` for package and environment management, which is a fast, modern alternative to `pip` and `venv`.

- **Dependencies**: Dependencies are defined in `pyproject.toml` under the `[project]` and `[tool.uv.dev-dependencies]` tables.
- **Installation**: The `just install` command sets up the development environment by creating a virtual environment and installing all necessary dependencies.
- **Locking**: The `uv.lock` file ensures that the exact versions of all dependencies are used, providing reproducible environments.

## 3. Development Workflow

The `justfile` provides a set of commands for common development tasks, streamlining the workflow:

- **`just install`**: Sets up the development environment.
- **`just test`**: Runs all unit and integration tests.
- **`just lint`**: Lints the code using `ruff` and applies automatic fixes.
- **`just format`**: Formats the code using `ruff`.
- **`just type-check`**: Performs static type checking with `pyright`.
- **`just check`**: A convenience command that runs all code quality checks (linting, formatting, type-checking, and testing).
- **`just migration "message"`**: Generates a new database migration using Alembic.
- **`just release vX.Y.Z`**: Creates a new stable release.
- **`just beta vX.Y.ZbN`**: Creates a new beta release.

## 4. Code Quality and Testing

The project emphasizes code quality through a combination of linting, formatting, type-checking, and a comprehensive testing suite.

- **Linting and Formatting**: `ruff` is used for both linting and formatting, ensuring a consistent code style.
- **Type Checking**: `pyright` is used for static type analysis, helping to catch errors before runtime.
- **Testing**: `pytest` is the testing framework. The project is configured to run unit and integration tests in parallel for faster execution. Code coverage is also measured to ensure a high level of test coverage.

## 5. Distribution and Deployment

The application is designed to be distributed as both a Python package and a Docker container.

- **Python Package**: The `pyproject.toml` file is configured to build the project into a wheel using `hatchling`. The `just release` and `just beta` commands automate the versioning and tagging process for releases, which are then built and published to PyPI via GitHub Actions.
- **Docker Container**: The `Dockerfile` provides a multi-stage build process that creates a lean, production-ready container. It uses `uv` to install dependencies from the lock file, ensuring a reproducible build. The container is configured to run the MCP server by default.

## 6. How to Initiate a New Repository

To create a new repository with these best practices, follow these steps:

1.  **Create the directory structure**:
    ```bash
    mkdir my-new-project
    cd my-new-project
    mkdir -p src/my_project_name docs tests test-int
    touch src/my_project_name/__init__.py
    ```

2.  **Create the configuration files**:
    - Create a `.python-version` file with your desired Python version (e.g., `3.12.1`).
    - Create a `pyproject.toml` file, using the `basic-memory` repository as a template. Adjust the project name, author, and dependencies as needed.
    - Create a `justfile` with the common development commands.
    - Create a `Dockerfile` for containerizing your application.

3.  **Initialize the environment**:
    ```bash
    # If you're using pyenv, set the local Python version
    pyenv local $(cat .python-version)

    # Create a virtual environment and install dependencies
    uv venv
    uv sync
    ```

4.  **Set up Git**:
    ```bash
    git init
    # Create a .gitignore file
    git add .
    git commit -m "Initial commit"
    ```

By following this guide, you can set up a new repository with a robust and modern development environment, based on the excellent practices demonstrated in the `basic-memory` project.
