.PHONY: help  # List phony targets
help:
	@cat "Makefile" | grep '^.PHONY:' | sed -e "s/^.PHONY:/- make/"

.PHONY: run  # Run component
run:
	uv run streamlit run src/main.py

.PHONY: clean  # Clean development environment
clean:
	rm -rf .venv
