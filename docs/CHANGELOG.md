## 2026-02-22

- Fixed failing pytest gates in `tests/` by removing the non-ASCII emoji from `README.md`.
- Modernized `screenshot/screencapture.py` by replacing shell-based `getstatusoutput` with `subprocess.run(...)` argument lists, removing unused imports, and updating type hints to Python 3.12 style.
- Replaced relative import usage in `screenshot/screencapture.py` with explicit module import (`import screenshot.get_window_id`) to satisfy import policy checks.
- Cleaned `screenshot/get_window_id.py` imports and type hints to remove pyflakes warnings and keep code current.
- Added missing development dependency declarations (`click`, `setuptools`) to `pip_requirements-dev.txt` for import-requirements tests.
- Normalized indentation in updated Python files to avoid mixed-indentation failures.
- Validation: `source source_me.sh && /opt/homebrew/opt/python@3.12/bin/python3.12 -m pytest tests -q` (118 passed).
- Refreshed `README.md` to a concise format with a verifiable quick-start path and curated links to `docs/`.
- Added missing common documentation pages: `docs/INSTALL.md`, `docs/USAGE.md`, `docs/TROUBLESHOOTING.md`, `docs/CODE_ARCHITECTURE.md`, `docs/FILE_STRUCTURE.md`, `docs/NEWS.md`, `docs/RELATED_PROJECTS.md`, `docs/RELEASE_HISTORY.md`, `docs/ROADMAP.md`, and `docs/TODO.md`.
- Added evidence-based "Known gaps" sections to new docs where repo evidence is incomplete, to avoid speculative documentation.
- Migrated packaging metadata from `setup.py` to `pyproject.toml` and removed `setup.py`.
- Added `pyproject.toml` console script entry point `screenshot = screenshot.screencapture:run`.
- Added `VERSION` and synchronized it with `pyproject.toml` version `1.0.0`.
- Added `pip_requirements.txt` as the runtime dependency manifest and updated docs/README installation commands to use it.
- Removed `docs/ROADMAP.md` and `docs/TODO.md` because this repo is a small app without those planning artifacts.
