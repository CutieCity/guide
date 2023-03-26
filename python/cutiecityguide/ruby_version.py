# Copyright (c) 2023 Nuztalgia <nuztalgia@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

"""This script fetches the current Ruby version used by Mastodon & updates the guide."""

import logging
import re
from functools import partial
from pathlib import Path
from typing import Final

from .utils import fetch_from_url, on_script_start, on_script_success

SCRIPT_NAME: Final[str] = Path(__file__).stem

DEV_SETUP_FILE_PATH: Final[str] = "../../../docs/self-hosting/development-setup.md"
RUBY_VERSION_PATH: Final[str] = "CutieCity/mastodon/main/.ruby-version"
RUBY_VERSION_URL: Final[str] = f"https://raw.githubusercontent.com/{RUBY_VERSION_PATH}"

VERSION_PATTERN: Final[re.Pattern] = re.compile(
    r"(?:[3-9]|\d{2,})(?:\.(?:0|[1-9]\d*)){2}"
)
COMMAND_PATTERN: Final[re.Pattern] = re.compile(
    f"(?P<command>rbenv (?:global|install)) (?P<version>{VERSION_PATTERN.pattern})"
)

EXPECTED_MATCHES: Final[int] = 2


def get_file_contents(file_path: Path, file_label: str) -> str | None:
    """Returns the contents of the file, or `None` if the path or file is malformed."""
    if not file_path.is_file():
        logging.error(f"Could not resolve {file_label} file path: '{file_path}'")
        return None

    logging.info(f"Attempting to parse {file_label} file: '{file_path}'")
    file_contents = file_path.read_text()

    if (matches := len(COMMAND_PATTERN.findall(file_contents))) != EXPECTED_MATCHES:
        logging.error(
            f"Expected {EXPECTED_MATCHES} rbenv command matches, but found {matches}."
        )
        return None

    return file_contents


def fetch_ruby_version() -> str | None:
    """Returns the Ruby version set by Cutie City Mastodon, or `None` if unavailable."""
    logging.info(f"Fetching Ruby version from: '{RUBY_VERSION_URL}'")
    response = fetch_from_url(RUBY_VERSION_URL)

    if isinstance(response, str):
        logging.error(response)
        return None

    version = response.read().decode("utf-8").strip()

    if not VERSION_PATTERN.fullmatch(version):
        logging.error(f"Ruby version '{version}' doesn't match the expected pattern.")
        return None

    logging.info(f"  - SUCCESS: The current Ruby version is '{version}'.")
    return version


def replace_ruby_version(current_version: str, match: re.Match) -> str:
    """Returns a replacement `str` (with an up-to-date version) for the given match."""
    if match["version"] == current_version:
        return match[0]
    else:
        updated_command = f"{match['command']} {current_version}"
        logging.info(f"  - Updating '{match[0]}' -> '{updated_command}'.")
        return updated_command


def main() -> int:
    """Serves as the primary entry point for the `ruby_version` script."""
    on_script_start(SCRIPT_NAME)

    dev_setup_file = (Path(__file__) / DEV_SETUP_FILE_PATH).resolve()

    if (not (ruby_version := fetch_ruby_version())) or (
        not (file_contents := get_file_contents(dev_setup_file, "dev setup"))
    ):
        return 1  # An appropriate error message will already have been printed.

    repl = partial(replace_ruby_version, ruby_version)
    new_file_contents = COMMAND_PATTERN.sub(repl, file_contents)

    if new_file_contents == file_contents:
        logging.info("  - The documented Ruby version is already up-to-date.")
    else:
        logging.info(f"Writing updated contents to file: '{dev_setup_file}'")
        dev_setup_file.write_text(new_file_contents, newline="\n")

    on_script_success(SCRIPT_NAME)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
