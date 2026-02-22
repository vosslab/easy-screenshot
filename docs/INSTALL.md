# Install

This project is a macOS command-line tool that uses ScreenCaptureKit window metadata and the system `screencapture` command.

## Prerequisites
- macOS with the built-in `screencapture` utility available on `PATH`.
- Python 3.12.
- `pip` for installing Python packages.

## Local setup
- Clone this repository and change into the repo root.
- Run `source source_me.sh`.
- Install runtime dependencies with `/opt/homebrew/opt/python@3.12/bin/python3.12 -m pip install -r pip_requirements.txt`.

## Verify installation
- Run `/opt/homebrew/opt/python@3.12/bin/python3.12 -m screenshot.screencapture --help`.
- If the help text renders, the local install path is ready.

## Known gaps
- Add explicit macOS version compatibility notes after validation across multiple versions.
