# diving-streamlit

- Load the `developing-with-streamlit` skill before any Streamlit change. On a fresh clone `.claude/skills/` is empty: run `just skills` after `uv sync`.
- A new page is a script in `src/tools/`, registered with `st.Page` in the `pages` dict of `src/main.py`.
- Streamlit Community Cloud deploys from `uv.lock`, so every lock change ships. Its Python version is set in the app's Advanced settings, not read from the repo: keep it equal to `.python-version`.
- Calculations without `st.` live in `src/utils.py`, tunable constants in `src/config.py`; pages keep widgets and display.
- `just test` covers `src/utils.py` only: verify pages with `just format` then `just start` and open each page. Google login and the database need `.streamlit/secrets.toml`, which is not committed.
- The database is Neon Postgres behind `[connections.db]`, set in both the local secrets and the app's Secrets settings. Both point to the same database, so local runs write production data: clean up any test rows.
- Community Cloud wipes its disk on every reboot and redeploy: anything that must persist goes to Neon.
