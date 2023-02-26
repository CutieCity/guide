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

"""This script fetches emoji data from Cutie City and writes it into a Markdown file."""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from string import Template
from typing import Any, Final
from urllib.error import HTTPError
from urllib.request import urlopen

EMOJI_API_ENDPOINT: Final[str] = "https://cutie.city/api/v1/custom_emojis"
OUTPUT_FILE_REL_PATH: Final[str] = "../../docs/cutie-city/custom-emoji.md"

MD_CATEGORY_HEADER: Final[Template] = Template(
    '??? category "$name ($count)"\n\n    ### $name'
)
MD_TAB_HEADER: Final[Template] = Template(
    '    === "$animation_label Animations"\n\n'
    '        <div class="grid cards small-columns" markdown>'
)
MD_EMOJI_ITEM: Final[Template] = Template(
    '        - ![:$name:]($url){title=":$name:"} `:$name:`'
)

MD_DEFAULT_TAB_HEADER: Final[str] = MD_TAB_HEADER.substitute(animation_label="Enable")
MD_STATIC_TAB_HEADER: Final[str] = MD_TAB_HEADER.substitute(animation_label="Pause")
MD_TAB_FOOTER: Final[str] = f"{' ' * 8}</div>"
MD_COMMENT: Final[Template] = Template("\n<!-- emoji-categories-$label -->\n")


@dataclass(frozen=True, kw_only=True, order=True)
class Emoji:
    """A dataclass representing the information necessary to display a custom emoji."""

    name: str
    default_url: str
    static_url: str

    @classmethod
    def create(cls, **emoji_data: Any) -> Emoji:
        """Creates and returns a new `Emoji` instance based on the given data."""
        return cls(
            name=emoji_data["shortcode"],
            default_url=(url := emoji_data.get("url", "")),
            static_url=emoji_data.get("static_url", url),
        )

    def to_markdown(self, static: bool = False) -> str:
        """Returns properly-formatted Markdown code for displaying this `Emoji`."""
        url = self.static_url if static else self.default_url
        return MD_EMOJI_ITEM.substitute(name=self.name, url=url)


def get_file_template(file_contents: str) -> Template | None:
    """Parses the existing file and returns a `Template` for writing the new data."""
    search_file = partial(re.search, string=file_contents, flags=re.DOTALL)

    start_match = search_file(f"^.*?{MD_COMMENT.substitute(label='start')}")
    end_match = search_file(f"{MD_COMMENT.substitute(label='end')}.*$")

    if start_match and end_match:
        start_content, end_content = start_match.group(0), end_match.group(0)
        return Template(f"{start_content}\n$output_markdown\n{end_content}")
    else:
        return None


def fetch_emoji_list(timeout_seconds: int = 10) -> list[dict[str, Any]] | str:
    """Fetches and returns custom emoji data from the Cutie City (Mastodon) API."""
    try:
        with urlopen(EMOJI_API_ENDPOINT, timeout=timeout_seconds) as response:
            return json.loads(response.read())
    except HTTPError as error:
        return f"'GET {EMOJI_API_ENDPOINT}' failed: {error.status} ({error.reason})"
    except TimeoutError:
        return f"'GET {EMOJI_API_ENDPOINT}' timed out after {timeout_seconds} seconds."
    except json.JSONDecodeError:
        return f"Response from 'GET {EMOJI_API_ENDPOINT}' is not valid JSON."


def build_output_markdown(emoji_by_category: dict[str, list[Emoji]]) -> str:
    """Returns properly-formatted Markdown code for displaying *all* custom emoji."""
    output_markdown = []

    for category in sorted(emoji_by_category):
        # noinspection PyTypeChecker
        emoji_list = sorted(emoji_by_category[category])

        output_markdown += [
            MD_CATEGORY_HEADER.substitute(name=category, count=len(emoji_list)),
            MD_DEFAULT_TAB_HEADER,
            "\n".join([emoji.to_markdown() for emoji in emoji_list]),
            MD_TAB_FOOTER,
            MD_STATIC_TAB_HEADER,
            "\n".join([emoji.to_markdown(static=True) for emoji in emoji_list]),
            MD_TAB_FOOTER,
        ]
        logging.info(f"  - SUCCESS: Generated markdown for '{category}'.")

    return "\n\n".join(output_markdown)


def main() -> int:
    """Serves as the primary entry point for (and executes) this entire script."""
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    logging.info("Starting 'custom-emoji' script.")

    output_file: Final[Path] = (Path(__file__) / OUTPUT_FILE_REL_PATH).resolve()
    emoji_by_category: Final[dict[str, list[Emoji]]] = {}

    if not output_file.is_file():
        logging.error(f"Could not resolve output file path: '{output_file}'")
        return 1

    logging.info(f"Attempting to parse output file: '{output_file}'")

    if file_template := get_file_template(output_file.read_text()):
        logging.info("  - SUCCESS: Found this script's target region.")
    else:
        logging.error("Could not find this script's target region in the output file.")
        return 1

    logging.info(f"Requesting all custom emoji from: '{EMOJI_API_ENDPOINT}'")

    if isinstance(all_emoji := fetch_emoji_list(), list) and all_emoji:
        logging.info(f"  - SUCCESS: Found a total of {len(all_emoji)} custom emoji.")
    else:
        logging.error(all_emoji or "Response did not contain any custom emoji.")
        return 1

    for emoji_data in all_emoji:
        if (category := emoji_data["category"]) not in emoji_by_category:
            emoji_by_category[category] = []
        emoji_by_category[category].append(Emoji.create(**emoji_data))

    logging.info(f"Processing {len(emoji_by_category)} custom emoji categories.")
    file_contents = file_template.substitute(
        output_markdown=build_output_markdown(emoji_by_category)
    )
    logging.info(f"Writing {len(file_contents.encode('utf-8'))} bytes to output file.")
    output_file.write_text(file_contents, newline="\n")

    logging.info("Successfully finished 'custom-emoji' script.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
