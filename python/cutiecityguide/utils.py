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

"""This module contains common utility functions used by multiple scripts."""

import logging
from http.client import HTTPResponse
from urllib.error import HTTPError
from urllib.request import urlopen


def fetch_from_url(url: str, timeout_seconds: int = 10) -> HTTPResponse | str:
    """Returns the `HTTPResponse` for the given `url`, or an error message string."""
    try:
        return urlopen(url, timeout=timeout_seconds)
    except HTTPError as error:
        return f"'GET {url}' failed: {error.status} ({error.reason})"
    except TimeoutError:
        return f"'GET {url}' timed out after {timeout_seconds} seconds."


def on_script_start(script_name: str) -> None:
    """Initializes `logging` and logs an introduction message for the given script."""
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    logging.info(f"Starting the Cutie City `{script_name}` script.")


def on_script_success(script_name: str) -> None:
    """Prints a completion (i.e. success) message for the given script."""
    logging.info(f"Successfully finished the Cutie City `{script_name}` script.")
