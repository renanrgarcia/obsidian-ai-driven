import re


SECTION_HEADERS = ("## Notes", "## Today", "## Scheduled", "## Project Tasks", "## Habits")
TASK_PATTERN = re.compile(r"^- \[(?P<done>[ xX])\]\s*(?P<body>.*)$")


def parse_sections(content: str) -> dict[str, list[str]]:
    sections = {header: [] for header in SECTION_HEADERS}
    current_header: str | None = None

    for raw_line in content.splitlines():
        line = raw_line.rstrip("\n")
        if line in sections:
            current_header = line
            continue
        if current_header is None:
            continue
        if line == "":
            continue
        sections[current_header].append(line)

    return sections


def render_sections(sections: dict[str, list[str]], *, title: str | None = None) -> str:
    blocks: list[str] = []
    if title:
        blocks.extend([title, ""])
    for header in SECTION_HEADERS:
        blocks.append(header)
        blocks.extend(sections.get(header, []))
        blocks.append("")
    return "\n".join(blocks).rstrip() + "\n"
