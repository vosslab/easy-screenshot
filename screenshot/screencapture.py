#!/usr/bin/env python3

from datetime import datetime
import subprocess
from typing import Iterator

import click

import screenshot.get_window_id

FILE_EXT = ".png"
STATUS_OK = 0
STATUS_FAIL = 1

IMG_TYPES = ("png", "pdf", "jpg", "tiff")


class ScreencaptureEx(Exception):
	pass


def take_screenshot(window: int, filename: str, options: list[str] | None = None) -> str:
	if options is None:
		options = []

	for option in options:
		if "-t" in option and not any(img_type in option.lower() for img_type in IMG_TYPES):
			raise ScreencaptureEx(f"Bad option {option}. File type unknown.")

	command = ["screencapture", *options, "-l", str(window), filename]
	result = subprocess.run(command, capture_output=True, text=True, check=False)

	if result.returncode != STATUS_OK:
		error_text = result.stderr.strip() or result.stdout.strip()
		raise ScreencaptureEx(f"Error: screencapture output: {error_text}")

	return filename


def get_filename(*args) -> str:
	return " ".join(map(str, args + (datetime.now(),))) + FILE_EXT


def gen_windows(application_name: str, title: str, window_selection_options: str) -> Iterator[int]:
	windows = screenshot.get_window_id.gen_window_ids(
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


@click.command()
@click.option(
	"-w",
	"--window_selection_options",
	default=screenshot.get_window_id.USER_OPTS_STR,
	help=(
		"Options: "
		+ ", ".join(screenshot.get_window_id.WINDOW_OPTIONS)
		+ "\nDefault: "
		+ screenshot.get_window_id.USER_OPTS_STR
	),
)
@click.option("-t", "--title", default="", help="Title of window from APPLICATION_NAME to capture.")
@click.option("-f", "--filename", default=None, help="Filename to save the captured PNG as.")
@click.option(
	"-a",
	"--all_windows",
	is_flag=True,
	default=False,
	help="Capture all windows matching parameters.",
)
@click.option(
	"-o",
	"--output",
	default="png",
	help="Image format to create, default is png (other options include pdf, jpg, tiff)",
)
@click.option("-s", "--shadow", is_flag=True, help="Capture the shadow of the window.")
@click.argument("application_name")
def run(application_name: str,
		title: str,
		filename: str,
		window_selection_options: str,
		output: str,
		shadow: bool,
		all_windows: bool) -> None:
	options: list[str] = []

	if output:
		options.extend(["-t", output])

	if not shadow:
		options.append("-o")

	try:
		if all_windows:
			if filename:
				print(
					f"Taking screenshots of all windows belonging to {application_name}, "
					"filename option ignored."
				)

			for generated_filename in screenshot_windows(
				application_name,
				title,
				window_selection_options,
				options,
			):
				print(generated_filename)
		else:
			print(screenshot_window(application_name, title, filename, window_selection_options, options))
		raise SystemExit(STATUS_OK)
	except ScreencaptureEx as error:
		print("Error:", error)
		raise SystemExit(STATUS_FAIL)


if __name__ == "__main__":
	run()
