from pathlib import Path

from daily_notes_bot.models import CaptureRequest


def ensure_capture_log(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not log_path.exists():
        log_path.write_text("", encoding="utf-8")


def write_capture_log(log_path: Path, capture: CaptureRequest) -> None:
    ensure_capture_log(log_path)
    content = log_path.read_text(encoding="utf-8")
    header = f"## {capture.timestamp.date().isoformat()}"
    entry = f"- {capture.timestamp.strftime('%H:%M')} [{capture.source_type}] {capture.normalized_text}"

    if not content.strip():
        log_path.write_text(f"{header}\n{entry}\n", encoding="utf-8")
        return

    lines = content.splitlines()
    output: list[str] = []
    inserted = False
    index = 0

    while index < len(lines):
        line = lines[index]
        output.append(line)
        if line == header and not inserted:
            output.append(entry)
            inserted = True
            index += 1
            while index < len(lines) and not lines[index].startswith("## "):
                output.append(lines[index])
                index += 1
            continue
        index += 1

    if not inserted:
        output = [header, entry, ""] + output

    log_path.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")
