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

import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any, cast
from xml.etree import ElementTree as etree


def emoji_generator(
    index, shortname, _alias, _uc, alt, title, category, options, md
) -> etree.Element:
    """Returns an image `Element` object for displaying the requested emoji in HTML."""
    attributes = {"alt": alt, "title": title or alt}

    if category:
        attributes |= {
            "class": "cutiemoji",
            "loading": "lazy",
            "src": f"https://media.cutie.city/custom_emojis/images/{category}",
        }
        element = etree.Element("img", attributes)
    else:
        element = etree.Element("span", attributes | {"class": "twemoji"})

        svg_path = md.inlinePatterns["emoji"].emoji_index["emoji"][shortname]["path"]
        element.text = md.htmlStash.store(Path(svg_path).read_text())

    for key, value in options.get("attributes", {}).items():
        element.set(key, value)

    return element


def emoji_index(_options, _md) -> dict[str, Any]:
    """Returns an index of Cutie City emoji in the format expected by pymdownx.emoji."""
    from importlib.util import find_spec
    from json import loads

    from cutiecityguide.custom_emoji import INDEX_FILE_REL_PATH

    emoji_index_path = Path(__file__) / INDEX_FILE_REL_PATH
    emoji_index = loads(emoji_index_path.resolve().read_text())

    if material_spec := find_spec("material"):
        material_directory = Path(cast(str, material_spec.origin)).parent

        for name, path in _get_bundled_icons(material_directory / ".icons"):
            if name not in emoji_index:
                emoji_index[name] = {"name": name, "path": path}

    return {
        "name": "cutiemoji",
        "emoji": emoji_index,
        "aliases": {},
    }


def _get_bundled_icons(source_directory) -> Iterator[tuple[str, Any]]:
    icon_sets = [
        (re.compile(f"^:{subdirectory_name}_"), f":{short_name}_")
        for short_name, subdirectory_name in {
            "fa": "fontawesome",
            "md": "material",
            "oi": "octicons",
            "si": "simple",
        }.items()
    ]

    for absolute_path in source_directory.glob("**/*.svg"):
        relative_path = absolute_path.relative_to(source_directory)
        name = f':{relative_path.with_suffix("").as_posix().replace("/", "_")}:'

        for pattern, prefix in icon_sets:
            name = pattern.sub(prefix, name)

        yield name, str(absolute_path)


__all__ = [
    "emoji_generator",
    "emoji_index",
]
