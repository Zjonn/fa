import mdformat

from argparse import ArgumentParser
from pathlib import Path

SCRIPT_NAME = Path(__file__).name

MAX_LINE_LENGTH = 150

LUA_DESC_LINE = '        "{line}"'
LUA_FILE = """Changelog = {{
    version = {version},
    description = {{
{description}
    }}
}},
"""

HEADER_SEPARATOR = "#" * MAX_LINE_LENGTH
HEADER = f"""{HEADER_SEPARATOR}
#{f"This file was autogenerated using {SCRIPT_NAME:}":^{MAX_LINE_LENGTH - 2}}#
#{{source:^{MAX_LINE_LENGTH - 2}}}#
{HEADER_SEPARATOR}

"""


def get_parser():
    ap = ArgumentParser(description="Converts Markdown release file to Lua.")
    ap.add_argument(
        "input_file",
        help="Markdown file",
        type=Path,
    )
    ap.add_argument(
        "output_file",
        help="Lua file",
        type=Path,
    )
    return ap


def convert_changelog(markdown: Path, lua: Path):
    version = markdown.stem

    source_info = f"Source: {markdown}"
    header = HEADER.format(source=source_info)
    lua_content = markdown2lua(version, markdown.read_text())
    lua.write_text(header + lua_content)


def markdown2lua(version: str, content: str) -> str:
    formatted_md = mdformat.text(
        content,
        options={
            "wrap": MAX_LINE_LENGTH,
        },
    )

    escaped_md = escape_special_symbols(formatted_md)
    return LUA_FILE.format(
        version=version,
        description=",\n".join(
            LUA_DESC_LINE.format(line=line) for line in escaped_md.splitlines()
        ),
    )


def escape_special_symbols(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    convert_changelog(args.input_file, args.output_file)
