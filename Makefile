.PHONY: help  # List phony targets
help:
	@cat "Makefile" | grep '^.PHONY:' | sed -e "s/^.PHONY:/- make/"

.PHONY: start  # Start component
start:
	uv run --group dev streamlit run src/main.py

.PHONY: clean  # Clean development environment
clean:
	rm -rf .venv

.PHONY: config  # Show streamlit config
config:
	uv run streamlit config show