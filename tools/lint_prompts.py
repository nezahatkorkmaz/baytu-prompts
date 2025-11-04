import re
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = (ROOT / "prompts" / "real_estate").rglob("*.md")

FORBIDDEN_PHRASES = [
    "hard-coded city",
    "always output Istanbul",
    "Kadıköy example leaks"
]

MAX_LINE = 120
RE_HEADING = re.compile(r"^#{1,6}\s+\S")

def check_line_length(path: Path, lines):
    for i, line in enumerate(lines, 1):
        if len(line.rstrip("\n")) > MAX_LINE:
            return f"{path}:{i} line too long ({len(line.rstrip())}>{MAX_LINE})"
    return None

def check_heading_order(path: Path, lines):
    # simple: headings must start with h1 then nondecreasing depth by at most +1
    last_level = 0
    for i, line in enumerate(lines, 1):
        m = RE_HEADING.match(line)
        if not m:
            continue
        level = len(line.split()[0])
        if last_level == 0 and level != 1:
            return f"{path}:{i} first heading must be level-1"
        if last_level and level > last_level + 1:
            return f"{path}:{i} heading level jumps from {last_level} to {level}"
        last_level = level
    return None

def extract_json_blocks(text: str):
    blocks = []
    fence_pattern = re.compile(r"```json\s*(.*?)```", re.DOTALL | re.IGNORECASE)
    for m in fence_pattern.finditer(text):
        blocks.append(m.group(1).strip())
    return blocks

def check_json_blocks_well_formed(path: Path, text: str):
    for block in extract_json_blocks(text):
        try:
            json.loads(block)
        except json.JSONDecodeError as e:
            return f"{path} invalid JSON block: {e}"
    return None

def check_forbidden_phrases(path: Path, text: str):
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in text.lower():
            return f"{path} contains forbidden phrase: {phrase}"
    return None

def main():
    errors = []
    for path in PROMPTS:
        content = path.read_text(encoding="utf-8")
        lines = content.splitlines(True)
        for fn in (check_line_length, check_heading_order):
            err = fn(path, lines)
            if err:
                errors.append(err)
        for fn in (check_json_blocks_well_formed, check_forbidden_phrases):
            err = fn(path, content)
            if err:
                errors.append(err)
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print("lint_prompts: OK")

if __name__ == "__main__":
    main()


