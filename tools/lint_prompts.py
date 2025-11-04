import re
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "prompts.index.json"

FORBIDDEN_PHRASES = [
    "hard-coded city",
    "always output Istanbul",
    "Kadıköy example leaks"
]

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

def iter_latest_prompt_paths():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    roles = data.get("roles", {})
    for role, info in roles.items():
        latest_rel = info.get("latest")
        if not latest_rel:
            yield role, None
            continue
        yield role, ROOT / latest_rel

def main():
    errors = []
    for role, path in iter_latest_prompt_paths():
        if path is None:
            errors.append(f"{role}: missing latest in registry")
            continue
        if not path.exists():
            errors.append(f"{role}: latest path not found: {path.relative_to(ROOT)}")
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"{path}: cannot read text: {e}")
            continue
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


