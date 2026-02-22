# Usage

This tool captures screenshots from matching macOS windows by app name and optional title filtering.

## Primary command
- Local invocation: `/opt/homebrew/opt/python@3.12/bin/python3.12 -m screenshot.screencapture [OPTIONS]`.
- Default behavior with no `--application` is interactive selection mode.

## Common options
- `-t, --title TEXT`: match only windows whose title contains the provided text.
- `-A, --application TEXT`: target a specific application in non-interactive mode.
- `-f, --filename TEXT`: set output file name for a single screenshot.
- `--multi`: capture all matching windows (default captures one).
- `--preview`: list matching windows (id, app, title) and exit without capture.
- `--dry-run`: alias for `--preview`.
- `--select`: interactive mode with numbered app/window selection in the terminal.
- `--include-desktop`: include desktop windows in discovery (default excludes desktop windows).
- `--include-offscreen`: include windows that are not currently on screen.
- `--with-shadow`: include window shadow in output (default is no shadow).
- `-o, --output TEXT`: image format (`png`, `pdf`, `jpg`, or `tiff`).

## Examples
- Show available options:
  - `/opt/homebrew/opt/python@3.12/bin/python3.12 -m screenshot.screencapture --help`
- Run default interactive mode:
  - `/opt/homebrew/opt/python@3.12/bin/python3.12 -m screenshot.screencapture`
- Capture the first matching Terminal window:
  - `/opt/homebrew/opt/python@3.12/bin/python3.12 -m screenshot.screencapture --application Terminal`
- Capture Terminal windows whose title includes `build`:
  - `/opt/homebrew/opt/python@3.12/bin/python3.12 -m screenshot.screencapture --application Terminal -t build`
- Capture all matching windows as JPG:
  - `/opt/homebrew/opt/python@3.12/bin/python3.12 -m screenshot.screencapture --application Terminal --multi -o jpg`
- List available Terminal windows before choosing a title filter:
  - `/opt/homebrew/opt/python@3.12/bin/python3.12 -m screenshot.screencapture --application Terminal --preview`
- List Terminal windows including off-screen windows:
  - `/opt/homebrew/opt/python@3.12/bin/python3.12 -m screenshot.screencapture --application Terminal --preview --include-offscreen`
- Run interactive selection mode (choose app, then choose window):
  - `/opt/homebrew/opt/python@3.12/bin/python3.12 -m screenshot.screencapture --select`

## Outputs
- Screenshots are written in the current working directory unless `--filename` is set.
- Generated default filenames include app name, title, and a timestamp.

## Known gaps
- Add stable filename conventions and output-directory guidance for automation pipelines.
- Add examples that demonstrate `--include-desktop` and `--include-offscreen` combinations.
