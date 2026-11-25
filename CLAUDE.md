# diving-streamlit

- Load the `developing-with-streamlit` skill before any Streamlit change. On a fresh clone `.claude/skills/` is empty: run `just skills` after `uv sync`.
- A new page is a script in `src/tools/`, registered with `st.Page` in the `pages` dict of `src/main.py`.
- Streamlit Community Cloud deploys from `uv.lock`, so every lock change ships. Its Python version is set in the app's Advanced settings, not read from the repo: keep it equal to `.python-version`.
- No automated tests: verify with `just format` then `just start` and open each page. Google login and the database need `.streamlit/secrets.toml`, which is not committed.
