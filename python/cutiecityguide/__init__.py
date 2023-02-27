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

"""This file contains a custom emoji index and generator to use with pymdownx.emoji."""

from typing import Any
from xml.etree import ElementTree


def emoji_generator(
    _index, _shortname, _alias, _uc, alt, title, category, options, _md
) -> ElementTree.Element:
    """Returns an image `Element` object for displaying the requested emoji in HTML."""
    attributes = {
        "alt": alt,
        "class": "cutiemoji",
        "loading": "lazy",
        "src": f"https://media.cutie.city/custom_emojis/images/{category}",
        "title": title or alt,
    }

    for key, value in options.get("attributes", {}).items():
        attributes[key] = value

    return ElementTree.Element("img", attributes)


def emoji_index(_options, _md) -> dict[str, Any]:
    """Returns an index of Cutie City emoji in the format expected by pymdownx.emoji."""
    from json import loads
    from pathlib import Path

    from .emoji_script import INDEX_FILE_REL_PATH

    index_path = (Path(__file__) / INDEX_FILE_REL_PATH).resolve()

    return {
        "name": "cutiemoji",
        "emoji": loads(index_path.read_text()),
        "aliases": {},
    }


__all__ = [
    "emoji_generator",
    "emoji_index",
]
