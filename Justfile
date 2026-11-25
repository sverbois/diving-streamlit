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
