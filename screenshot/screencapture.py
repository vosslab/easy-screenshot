#!/usr/bin/env python3

import argparse
from datetime import datetime
import re
import subprocess
import unicodedata
from typing import Iterator

import rich.console
import rich.prompt
import rich.table
import screenshot.get_window_id as get_window_id

FILE_EXT = ".png"
STATUS_OK = 0
STATUS_FAIL = 1

IMG_TYPES = ("png", "pdf", "jpg", "tiff")
CONSOLE = rich.console.Console()


class ScreencaptureEx(Exception):
	pass


def sanitize_filename_component(value: str) -> str:
	"""
	Convert text into an ASCII-safe filename component.
	"""
	ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
	ascii_value = re.sub(r"[^A-Za-z0-9 .-]+", " ", ascii_value)
	ascii_value = re.sub(r"\s+", " ", ascii_value).strip()
	if not ascii_value:
		return "untitled"
	ascii_value = ascii_value.replace(" ", "_")
	return ascii_value


def take_screenshot(window: int, filename: str, options: list[str] | None = None) -> str:
	if options is None:
		options = []

	for index, option in enumerate(options):
		if option != "-t":
			continue
		if index + 1 >= len(options):
			raise ScreencaptureEx("Bad option -t. File type missing.")
		output_type = options[index + 1].lower()
		if output_type not in IMG_TYPES:
			raise ScreencaptureEx(f"Bad option -t {output_type}. File type unknown.")

	command = ["screencapture", *options, "-l", str(window), filename]
	result = subprocess.run(command, capture_output=True, text=True, check=False)

	if result.returncode != STATUS_OK:
		error_text = result.stderr.strip() or result.stdout.strip()
		raise ScreencaptureEx(f"Error: screencapture output: {error_text}")

	return filename


def get_filename(*args) -> str:
	clean_parts = [sanitize_filename_component(str(part)) for part in args if str(part).strip()]
	timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
	clean_parts.append(timestamp)
	base_name = "_".join(clean_parts).strip("_")
	if not base_name:
		base_name = f"screenshot_{timestamp}"
	return base_name + FILE_EXT


def gen_windows(application_name: str, title: str, window_selection_options: str) -> Iterator[int]:
	windows = get_window_id.gen_window_ids(
		application_name,
		title,
		window_selection_options,
	)

	try:
		yield next(windows)

	except StopIteration as error:
		raise ScreencaptureEx(
			f"Window with parent {application_name} and title {title} not found."
		) from error

	yield from windows


def screenshot_windows(
	application_name: str,
	title: str = "",
	window_selection_options: str = "",
	options: list[str] | None = None,
) -> Iterator[str]:
	windows = gen_windows(application_name, title, window_selection_options)

	for window in windows:
		yield take_screenshot(window, get_filename(application_name, title), options)


def screenshot_window(
	application_name: str,
	title: str = "",
	filename: str = "",
	window_selection_options: str = "",
	options: list[str] | None = None,
) -> str:
	windows = gen_windows(application_name, title, window_selection_options)
	window = next(windows)
	filename = filename if filename else get_filename(application_name, title)
	return take_screenshot(window, filename, options)


def preview_windows(application_name: str, title: str, window_selection_options: str) -> int:
	"""
	List matching windows for an application and optional title filter.
	"""
	windows = get_window_id.get_window_info(window_selection_options)
	parent_filter = application_name.lower()
	title_filter = title.lower()
	matches = []
	for window in windows:
		owner = str(window.get("owner_name", ""))
		window_title = str(window.get("title", ""))
		window_id = int(window.get("window_id", 0))
		if parent_filter not in owner.lower():
			continue
		if title_filter and title_filter not in window_title.lower():
			continue
		matches.append((window_id, owner, window_title))

	if not matches:
		print(f"No windows found for app={application_name!r} title_filter={title!r}.")
		return STATUS_FAIL

	print("Matching windows:")
	for window_id, owner, window_title in matches:
		print(f"{window_id}\t{owner}\t{window_title}")
	return STATUS_OK


def resolve_window_selection_options(args: argparse.Namespace) -> str:
	"""
	Resolve effective window query options from flags.
	"""
	options = []
	if not args.include_desktop:
		options.append("exclude_desktop")
	if not args.include_offscreen:
		options.append("on_screen_only")
	return " ".join(options)


def build_capture_options(output: str, with_shadow: bool) -> list[str]:
	"""
	Build screencapture CLI option list.
	"""
	options: list[str] = []
	if output:
		options.extend(["-t", output])
	if not with_shadow:
		options.append("-o")
	return options


def select_application(window_selection_options: str) -> str:
	"""
	Interactively select an application name from discovered windows.
	"""
	windows = get_window_id.get_window_info(window_selection_options)
	app_names = sorted(
		{
			str(window.get("owner_name", "")).strip()
			for window in windows
			if str(window.get("owner_name", "")).strip()
		}
	)
	if not app_names:
		raise ScreencaptureEx("No applications found in shareable content.")

	table = rich.table.Table(title="Applications")
	table.add_column("#", style="cyan", justify="right")
	table.add_column("Application", style="green")
	for index, app_name in enumerate(app_names, start=1):
		table.add_row(str(index), app_name)
	CONSOLE.print(table)

	if len(app_names) == 1:
		CONSOLE.print("Only one application matched. Auto-selecting #1.")
		return app_names[0]

	choices = [str(i) for i in range(1, len(app_names) + 1)]
	selection = rich.prompt.Prompt.ask(
		"Select application number",
		choices=choices,
		default="1",
	)
	return app_names[int(selection) - 1]


def select_window(application_name: str, title: str, window_selection_options: str) -> int:
	"""
	Interactively select one window id from filtered app windows.
	"""
	windows = get_window_id.get_window_info(window_selection_options)
	parent_filter = application_name.lower()
	title_filter = title.lower()
	matches = []
	for window in windows:
		owner = str(window.get("owner_name", ""))
		window_title = str(window.get("title", ""))
		window_id = int(window.get("window_id", 0))
		if parent_filter not in owner.lower():
			continue
		if title_filter and title_filter not in window_title.lower():
			continue
		matches.append((window_id, owner, window_title))

	if not matches:
		raise ScreencaptureEx(
			f"No windows found for app={application_name!r} title_filter={title!r}."
		)

	table = rich.table.Table(title=f"Windows for {application_name}")
	table.add_column("#", style="cyan", justify="right")
	table.add_column("Window ID", style="magenta", justify="right")
	table.add_column("Application", style="green")
	table.add_column("Title", style="white")
	for index, (window_id, owner, window_title) in enumerate(matches, start=1):
		table.add_row(str(index), str(window_id), owner, window_title or "<untitled>")
	CONSOLE.print(table)

	if len(matches) == 1:
		CONSOLE.print("Only one window matched. Auto-selecting #1.")
		return matches[0][0]

	choices = [str(i) for i in range(1, len(matches) + 1)]
	selection = rich.prompt.Prompt.ask(
		"Select window number",
		choices=choices,
		default="1",
	)
	return matches[int(selection) - 1][0]


def interactive_select_capture(args: argparse.Namespace) -> int:
	"""
	Run interactive application/window selection and capture once.
	"""
	application_name = args.application
	window_selection_options = resolve_window_selection_options(args)
	if not application_name:
		application_name = select_application(window_selection_options)
	window_id = select_window(application_name, args.title, window_selection_options)
	filename = args.filename if args.filename else get_filename(application_name, args.title)
	options = build_capture_options(args.output, args.with_shadow)
	print(take_screenshot(window_id, filename, options))
	return STATUS_OK


def parse_args() -> argparse.Namespace:
	"""
	Parse CLI arguments for screenshot capture.
	"""
	parser = argparse.ArgumentParser(
		description="Capture macOS window screenshots by application name and optional title.",
	)
	parser.add_argument(
		"-A",
		"--application",
		default="",
		help="Application name to match (for example Terminal).",
	)
	parser.add_argument(
		"--include-desktop",
		action="store_true",
		help="Include desktop windows in discovery (default: desktop excluded).",
	)
	parser.add_argument(
		"--include-offscreen",
		action="store_true",
		help="Include off-screen windows in discovery (default: on-screen only).",
	)
	parser.add_argument(
		"-t",
		"--title",
		default="",
		help="Title substring to match within APPLICATION_NAME windows.",
	)
	parser.add_argument(
		"-f",
		"--filename",
		default="",
		help="Output filename for a single screenshot.",
	)
	parser.add_argument(
		"--multi",
		action="store_true",
		help="Capture all matching windows (default captures one).",
	)
	parser.add_argument(
		"--preview",
		action="store_true",
		help="Show matching windows and exit without capturing.",
	)
	parser.add_argument(
		"--dry-run",
		action="store_true",
		help="Alias for --preview.",
	)
	parser.add_argument(
		"--select",
		action="store_true",
		help="Interactive selection mode: pick app and window by number, then capture.",
	)
	parser.add_argument(
		"-o",
		"--output",
		default="png",
		choices=IMG_TYPES,
		help="Output image format.",
	)
	parser.add_argument(
		"--with-shadow",
		action="store_true",
		help="Capture window shadow (default is no shadow).",
	)
	return parser.parse_args()


def run(args: argparse.Namespace) -> int:
	"""
	Run screenshot capture using parsed arguments.
	"""
	if not args.application and not args.select and not args.preview and not args.dry_run:
		args.select = True

	if args.select and args.multi:
		print("Error: --select cannot be combined with --multi.")
		return STATUS_FAIL

	if args.preview or args.dry_run:
		if not args.application:
			print("Error: --application is required with --preview/--dry-run.")
			return STATUS_FAIL
		window_selection_options = resolve_window_selection_options(args)
		return preview_windows(args.application, args.title, window_selection_options)

	if args.select:
		try:
			return interactive_select_capture(args)
		except ScreencaptureEx as error:
			print("Error:", error)
			return STATUS_FAIL

	if not args.application:
		print("Error: --application is required in non-interactive mode.")
		return STATUS_FAIL

	window_selection_options = resolve_window_selection_options(args)
	options = build_capture_options(args.output, args.with_shadow)

	try:
		if args.multi:
			if args.filename:
				print(
					f"Taking screenshots of all windows belonging to {args.application}, "
					"filename option ignored."
				)

			for generated_filename in screenshot_windows(
				args.application,
				args.title,
				window_selection_options,
				options,
			):
				print(generated_filename)
		else:
			print(
				screenshot_window(
					args.application,
					args.title,
					args.filename,
					window_selection_options,
					options,
				)
			)
		return STATUS_OK
	except ScreencaptureEx as error:
		print("Error:", error)
		return STATUS_FAIL


def main() -> None:
	"""
	Program entry point for CLI execution.
	"""
	args = parse_args()
	status_code = run(args)
	raise SystemExit(status_code)


if __name__ == "__main__":
	main()
