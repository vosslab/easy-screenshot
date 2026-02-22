# screenshot

`screenshot` is a macOS CLI tool for developers who need repeatable window screenshots in scripts, using app name and optional window-title filters instead of manual clicking.

## Documentation
- [docs/INSTALL.md](docs/INSTALL.md): setup steps and prerequisites for local use.
- [docs/USAGE.md](docs/USAGE.md): command options and practical examples.
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md): common failures and fixes.
- [docs/CODE_ARCHITECTURE.md](docs/CODE_ARCHITECTURE.md): module responsibilities and flow.
- [docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md): repository layout and purpose of each path.
- [docs/CHANGELOG.md](docs/CHANGELOG.md): dated record of code and documentation changes.

## Quick start
```bash
source source_me.sh
/opt/homebrew/opt/python@3.12/bin/python3.12 -m pip install -r pip_requirements.txt
/opt/homebrew/opt/python@3.12/bin/python3.12 screenshot/screencapture.py --help
```

## Testing
```bash
source source_me.sh && /opt/homebrew/opt/python@3.12/bin/python3.12 -m pytest tests -q
```
