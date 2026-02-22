# Usage

This tool captures screenshots from matching macOS windows by app name and optional title filtering.

## Primary command
- Local invocation: `/opt/homebrew/opt/python@3.12/bin/python3.12 screenshot/screencapture.py [OPTIONS] APPLICATION_NAME`.
- The command requires a non-empty `APPLICATION_NAME`.

## Common options
- `-t, --title TEXT`: match only windows whose title contains the provided text.
- `-f, --filename TEXT`: set output file name for a single screenshot.
- `-a, --all_windows`: capture all matching windows.
- `-o, --output TEXT`: image format (`png`, `pdf`, `jpg`, or `tiff`).
- `-s, --shadow`: include window shadow in output.
- `-w, --window_selection_options TEXT`: pass window selection flags such as `exclude_desktop on_screen_only`.

## Examples
- Show available options:
  - `/opt/homebrew/opt/python@3.12/bin/python3.12 screenshot/screencapture.py --help`
- Capture the first matching Terminal window:
  - `/opt/homebrew/opt/python@3.12/bin/python3.12 screenshot/screencapture.py Terminal`
- Capture Terminal windows whose title includes `build`:
  - `/opt/homebrew/opt/python@3.12/bin/python3.12 screenshot/screencapture.py Terminal -t build`
- Capture all matching windows as JPG:
  - `/opt/homebrew/opt/python@3.12/bin/python3.12 screenshot/screencapture.py Terminal -a -o jpg`

## Outputs
- Screenshots are written in the current working directory unless `--filename` is set.
- Generated default filenames include app name, title, and a timestamp.

## Known gaps
- Add stable filename conventions and output-directory guidance for automation pipelines.
- Add examples that demonstrate `--window_selection_options` combinations with expected behavior.
