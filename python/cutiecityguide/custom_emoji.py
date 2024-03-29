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

"""This script fetches emoji data from Cutie City and writes it into two other files."""

from __future__ import annotations

import json
import logging
import re
from collections.abc import Callable
from dataclasses import InitVar, dataclass, field
from functools import cached_property, partial
from pathlib import Path
from string import Template
from typing import Any, Final, cast

from .utils import fetch_from_url, on_script_start, on_script_success

SCRIPT_NAME: Final[str] = Path(__file__).stem

EMOJI_API_ENDPOINT: Final[str] = "https://cutie.city/api/v1/custom_emojis"
MD_FILE_REL_PATH: Final[str] = "../../../docs/cutie-city/custom-emoji.md"
INDEX_FILE_REL_PATH: Final[str] = "../assets/emoji_index.json"

MD_CATEGORY_HEADER: Final[Template] = Template(
    '??? abstract "$name ($count)"\n\n    ### $name'
)
MD_GRID_HEADER: Final[Template] = Template(
    '$indent    <div class="grid cards small-columns" markdown>'
)
MD_TAB_HEADER: Final[Template] = Template(
    '    === "$animation_label Animations"\n\n'
    + MD_GRID_HEADER.substitute(indent=" " * 4)
)
MD_EMOJI_ITEM_DEFAULT: Final[Template] = Template("$indent    - :$name: `:$name:`")
MD_EMOJI_ITEM_STATIC: Final[Template] = Template(
    "$indent    - ![:$name:]($url){.cutiemoji "
    r'loading="lazy" title="\:$name:"} `:$name:`'
)
MD_COMMENT: Final[Template] = Template("\n<!-- emoji-categories-$label -->\n")

MD_DEFAULT_TAB_HEADER: Final[str] = MD_TAB_HEADER.substitute(animation_label="Enable")
MD_STATIC_TAB_HEADER: Final[str] = MD_TAB_HEADER.substitute(animation_label="Pause")
MD_TAB_FOOTER: Final[str] = f"{' ' * 8}</div>"
MD_GRID_FOOTER: Final[str] = f"{' ' * 4}</div>"

EMOJI_URL_PATTERN: Final[re.Pattern] = re.compile(
    r"^https://media\.cutie\.city/custom_emojis/images/"
    r"([0-9/]{12}original/\w+\.[a-zA-Z]{3,4})$"
)


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

    def to_markdown(self, indent: str = " " * 4, static: bool = False) -> str:
        """Returns properly-formatted Markdown code for displaying this `Emoji`."""
        keywords = {"indent": indent, "name": self.name}
        template = MD_EMOJI_ITEM_DEFAULT

        if static and (self.default_url[-3:] != self.static_url[-3:]):
            keywords["url"] = self.static_url
            template = MD_EMOJI_ITEM_STATIC

        return template.substitute(**keywords)


@dataclass
class File:
    """A dataclass representing the information necessary to write to a given file."""

    label: str
    get_template: Callable[[str], Template | None]
    rel_path: InitVar[str]
    path: Path = field(init=False)

    def __post_init__(self, rel_path: str) -> None:
        """Finish up initialization for this `File` object (i.e. resolve its path)."""
        self.path = (Path(__file__) / rel_path).resolve()

    @cached_property
    def template(self) -> Template | None:
        """Reads the text of the `File` and tries to return a `Template` for writing."""
        return self.get_template(self.path.read_text())

    def write(
        self,
        generated_content: str,
        transform: Callable[[str], str] | None = None,
    ) -> None:
        """Pieces together the file content and writes it to the path for the `File`."""
        file_contents = cast(Template, self.template).substitute(
            **{f"generated_{self.label}": generated_content}
        )
        if transform:
            file_contents = transform(file_contents)

        num_bytes = len(file_contents.encode("utf-8"))
        logging.info(f"Writing {num_bytes} bytes to {self.label} file: '{self.path}'")
        self.path.write_text(file_contents, newline="\n")


def get_md_file_template(file_contents: str) -> Template | None:
    """Parses the existing Markdown file and returns a `Template` for writing to it."""
    search_file = partial(re.search, string=file_contents, flags=re.DOTALL)

    start_match = search_file(f"^.*?{MD_COMMENT.substitute(label='start')}")
    end_match = search_file(f"{MD_COMMENT.substitute(label='end')}.*$")

    if start_match and end_match:
        return Template(f"{start_match[0]}\n$generated_markdown\n{end_match[0]}")
    else:
        return None


def fetch_emoji_list() -> list[dict[str, Any]] | str:
    """Fetches and returns custom emoji data from the Cutie City (Mastodon) API."""
    response = fetch_from_url(EMOJI_API_ENDPOINT)

    if isinstance(response, str):
        return response  # This is an error message to be logged.

    try:
        return json.loads(response.read())
    except json.JSONDecodeError:
        return f"Response from 'GET {EMOJI_API_ENDPOINT}' is not valid JSON."


def organize_emoji(
    all_emoji: list[dict[str, Any]]
) -> tuple[dict[str, list[Emoji]], dict[str, dict[str, str]]]:
    """Returns a tuple consisting of two differently-organized emoji dictionaries."""
    emoji_by_category: Final[dict[str, list[Emoji]]] = {}
    emoji_index: Final[dict[str, dict[str, str]]] = {}

    for emoji_data in all_emoji:
        if (category := emoji_data["category"]) not in emoji_by_category:
            emoji_by_category[category] = []

        emoji = Emoji.create(**emoji_data)

        if emoji_url_match := EMOJI_URL_PATTERN.match(emoji.default_url):
            emoji_url = emoji_url_match.group(1)
        else:
            raise ValueError(f"Unexpected emoji url pattern: '{emoji.default_url}'")

        emoji_by_category[category].append(emoji)
        emoji_index[f":{emoji.name}:"] = {
            "name": emoji.name.replace("_", " "),
            "category": emoji_url,  # This is a hack to pass a non-unicode identifier.
        }

    return emoji_by_category, {k: emoji_index[k] for k in sorted(emoji_index.keys())}


def generate_emoji_md_code(emoji_by_category: dict[str, list[Emoji]]) -> str:
    """Returns properly-formatted Markdown code for displaying *all* custom emoji."""
    markdown_components = []

    for category in sorted(emoji_by_category):
        # noinspection PyTypeChecker
        emoji_list = sorted(emoji_by_category[category])

        markdown_components.append(
            MD_CATEGORY_HEADER.substitute(name=category, count=len(emoji_list))
        )

        if any(emoji.default_url.endswith("gif") for emoji in emoji_list):
            markdown_components += [
                MD_DEFAULT_TAB_HEADER,
                "\n".join([emoji.to_markdown() for emoji in emoji_list]),
                MD_TAB_FOOTER,
                MD_STATIC_TAB_HEADER,
                "\n".join([emoji.to_markdown(static=True) for emoji in emoji_list]),
                MD_TAB_FOOTER,
            ]
        else:
            markdown_components += [
                MD_GRID_HEADER.substitute(indent=""),
                "\n".join([emoji.to_markdown(indent="") for emoji in emoji_list]),
                MD_GRID_FOOTER,
            ]

    return "\n\n".join(markdown_components)


def transform_md_text(original_text: str, emoji_count: int, category_count: int) -> str:
    """Makes final adjustments to the Markdown code before it's written to file."""
    intermediate_text = re.sub(
        pattern=r"\*\*[0-9]{3,}\*\* custom emoji",
        repl=f"**{emoji_count}** custom emoji",
        string=original_text,
        count=1,
    )
    return re.sub(
        pattern=r"\*\*[0-9]+\*\* categories",
        repl=f"**{category_count}** categories",
        string=intermediate_text,
        count=2,
    )


def write_files(
    markdown_file: File,
    index_file: File,
    emoji_by_category: dict[str, list[Emoji]],
    emoji_index: dict[str, dict[str, str]],
) -> None:
    """Properly formats the given emoji data as code & writes it to the given files."""
    counts = {"category_count": len(emoji_by_category), "emoji_count": len(emoji_index)}
    logging.info(
        f"  - SUCCESS: Sorted {counts['emoji_count']} emoji"
        f" into {counts['category_count']} categories."
    )

    logging.info(f"Formatting markup code for '{markdown_file.path.name}'.")
    markdown_file.write(
        generate_emoji_md_code(emoji_by_category),
        partial(transform_md_text, **counts),
    )

    logging.info(f"Formatting emoji index for '{index_file.path.name}'.")
    index_file.write(json.dumps(emoji_index, indent=2))


def main() -> int:
    """Serves as the primary entry point for the `custom_emoji` script."""
    on_script_start(SCRIPT_NAME)

    markdown_file = File("markdown", get_md_file_template, MD_FILE_REL_PATH)
    index_file = File(
        "index", lambda _: Template("$generated_index\n"), INDEX_FILE_REL_PATH
    )

    for file in [markdown_file, index_file]:
        if not file.path.is_file():
            logging.error(f"Could not resolve {file.label} file path: '{file.path}'")
            return 1

        logging.info(f"Attempting to parse {file.label} file: '{file.path}'")

        if not file.template:
            logging.error(f"Could not find the target region in the {file.label} file.")
            return 1

    logging.info(f"Requesting all custom emoji from: '{EMOJI_API_ENDPOINT}'")

    if isinstance(all_emoji := fetch_emoji_list(), list) and all_emoji:
        logging.info(f"  - SUCCESS: Found a total of {len(all_emoji)} custom emoji.")
    else:
        logging.error(all_emoji or "Response did not contain any custom emoji.")
        return 1

    logging.info("Sorting all custom emoji by category and index.")

    try:
        write_files(markdown_file, index_file, *organize_emoji(all_emoji))
    except ValueError as error:
        logging.error(error.args[0])
        return 1

    on_script_success(SCRIPT_NAME)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
