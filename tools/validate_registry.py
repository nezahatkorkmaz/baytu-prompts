import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "prompts.index.json"

def main():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))

    assert "roles" in data and isinstance(data["roles"], dict), "Invalid registry schema"

    missing = []
    for role, info in data["roles"].items():
        latest = info.get("latest")
        versions = info.get("versions", [])
        if not latest:
            missing.append(f"{role}: missing latest")
            continue
        latest_path = ROOT / latest
        if not latest_path.exists():
            missing.append(f"{role}: latest path not found: {latest}")
        for v in versions:
            if not (ROOT / v).exists():
                missing.append(f"{role}: version path not found: {v}")
        if latest not in versions:
            missing.append(f"{role}: latest not listed in versions array")

    if missing:
        print("\n".join(missing))
        sys.exit(1)
    print("validate_registry: OK")

if __name__ == "__main__":
    main()


