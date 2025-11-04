import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "prompts.index.json"

def main():
    problems = []
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    roles = data.get("roles", {})
    for role, info in roles.items():
        latest_rel = info.get("latest")
        if not latest_rel:
            problems.append(f"{role}: missing latest in registry")
            continue
        latest_path = ROOT / latest_rel
        if not latest_path.exists():
            problems.append(f"{role}: latest path not found: {latest_rel}")
            continue
        try:
            text = latest_path.read_text(encoding="utf-8")
        except Exception as e:
            problems.append(f"{latest_rel}: cannot read text: {e}")
            continue
        if not text.strip():
            problems.append(f"{latest_rel}: file is empty")

    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print("check_required_sections: OK")

if __name__ == "__main__":
    main()


