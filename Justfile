_default:
    @just --list --unsorted

# Start the app
start:
    uv run --group dev streamlit run src/main.py

# Install Streamlit agent skills for Claude Code
skills:
    uv run streamlit skills --yes

# Clean development environment
clean:
    rm -rf .venv

# Show streamlit config
config:
    uv run streamlit config show

# Run the tests
test:
    uv run --group dev pytest

# Check lint and format without changing files
lint:
    uv run ruff check
    uv run ruff format --check

# Fix lint and format the code
format:
    uv run ruff format
    uv run ruff check --fix
