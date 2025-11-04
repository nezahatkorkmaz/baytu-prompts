import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROLES = ["default", "translation", "assistant"]

REQUIRED_HEADINGS = [
    "MCP Fixed Parameters",
    "Location Integrity",
    "HTML Output Spec"
]

RE_VALIDATION_ONLY = re.compile(r"\bvalidation-only\b", re.IGNORECASE)
RE_JSON_FENCE = re.compile(r"```json\s*(.*?)```", re.DOTALL | re.IGNORECASE)

def check_required_sections(path: Path, text: str):
    missing = []
    for h in REQUIRED_HEADINGS:
        if h.lower() not in text.lower():
            missing.append(f"Missing heading '{h}'")
    if not RE_VALIDATION_ONLY.search(text):
        missing.append("Missing 'validation-only' rule mention")
    if not RE_JSON_FENCE.search(text):
        missing.append("Missing JSON fenced MCP block")
    return missing

def main():
    problems = []
    for role in ROLES:
        v31 = ROOT / "prompts" / "real_estate" / role / "v3.1.md"
        if not v31.exists():
            problems.append(f"{role}: v3.1 prompt not found")
            continue
        text = v31.read_text(encoding="utf-8")
        issues = check_required_sections(v31, text)
        problems.extend([f"{v31}: {msg}" for msg in issues])

    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print("check_required_sections: OK")

if __name__ == "__main__":
    main()


