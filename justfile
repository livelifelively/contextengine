install:
    uv venv
    uv sync

test:
    uv run pytest tests/ -v
    @echo "Integration tests directory exists but is empty, skipping..."

lint:
    uv run ruff check . --fix

format:
    uv run ruff format .

type-check:
    uv run pyright

check:
    just lint
    just format
    just type-check
    just test
