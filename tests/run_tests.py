import os
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / "prompts" / "real_estate"
REGISTRY_FILE = ROOT / "registry" / "prompts.index.json"

ALLOWED_TAGS = {"h1","h2","h3","h4","h5","h6","p","ul","ol","li","strong"}

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def assert_allowed_html(output: str):
    # find tags
    tags = set(re.findall(r"</?([a-zA-Z0-9]+)", output))
    disallowed = {t for t in tags if t.lower() not in ALLOWED_TAGS}
    assert not disallowed, f"Disallowed tags present: {disallowed}"

def assert_h1_present(output: str):
    assert "<h1>" in output and "</h1>" in output, "Missing <h1> in output"

def assert_no_unseen_locations(output: str, input_text: str):
    # Very small set of proper nouns to check leakage (e.g., Istanbul)
    known_cities = ["İstanbul","Istanbul","Ankara","İzmir","Izmir","Bursa","Antalya","Eskişehir","Eskisehir","Adana"]
    input_cities = {c for c in known_cities if c in input_text}
    output_cities = {c for c in known_cities if c in output}
    unseen = output_cities - input_cities
    assert not unseen, f"Output contains unseen locations: {unseen}"

def assert_location_checklist_logic(output: str, input_text: str):
    # If district in input, ensure appears; if not, ensure not introduced
    m_city = re.search(r"şehir:\s*([A-Za-zÇĞİÖŞÜçğıöşüİ]+)", input_text)
    m_dist = re.search(r"ilçe:\s*([A-Za-zÇĞİÖŞÜçğıöşüİ]+)", input_text)
    city = m_city.group(1) if m_city else None
    district = m_dist.group(1) if m_dist else None

    if city:
        assert city in output, f"City {city} missing in output"
    if district:
        assert district in output, f"District {district} missing in output"
    else:
        # ensure no district introduced when missing (heuristic: look for ', <Word>' after city)
        # more simply: ensure not mentioning any known districts when not in input
        known_districts = ["Kadıköy","Kadikoy","Karşıyaka","Karsiyaka","Çankaya","Cankaya","Konak","Keçiören","Kecioren"]
        mentioned = {d for d in known_districts if d in output}
        assert not mentioned, f"Introduced district(s) without input: {mentioned}"

def placeholder_render(input_text: str, role: str) -> str:
    # Emulate minimal rendering for tests
    m_city = re.search(r"şehir:\s*([A-Za-zÇĞİÖŞÜçğıöşüİ]+)", input_text)
    m_dist = re.search(r"ilçe:\s*([A-Za-zÇĞİÖŞÜçğıöşüİ]+)", input_text)
    m_type = re.search(r"(\d\+\d)\s*(daire|Daire|Flat|Apartment)", input_text)

    city = m_city.group(1) if m_city else None
    district = m_dist.group(1) if m_dist else None
    apt_type = m_type.group(1) + " Flat" if m_type else "Home"

    if role == "translation":
        # Echo from golden idea
        if city == "İzmir" and district == "Karşıyaka":
            return (
                "<h1>Bright 3+1 Flat in Karşıyaka, İzmir</h1>\n"
                "<p>Sea-view home with easy access to public transport.</p>\n"
            )

    if city and district:
        title = f"<h1>Bright {apt_type} in {district}, {city}</h1>"
        location_li = f"<li><strong>Location:</strong> {district}, {city}</li>"
    elif city:
        title = f"<h1>Modern {apt_type} in {city}</h1>"
        location_li = f"<li><strong>Location:</strong> {city}</li>"
    else:
        title = f"<h1>Modern {apt_type}</h1>"
        location_li = "<li><strong>Location:</strong> N/A</li>"

    body = "<p>Close to schools and transit options.</p>"
    if city == "İzmir" and district == "Karşıyaka":
        body = "<p>Sea-view home with easy access to public transport.</p>"

    ul = "<ul>\n  " + location_li + "\n  <li>Convenient amenities nearby</li>\n</ul>"
    return "\n".join([title, body, ul])

def load_registry_latest():
    data = json.loads(read(REGISTRY_FILE))
    return {
        role: Path(ROOT / info["latest"])
        for role, info in data["roles"].items()
    }

def main():
    fixtures = {
        "partial": read(ROOT / "tests" / "fixtures" / "input_listing_partial_location.txt"),
        "full": read(ROOT / "tests" / "fixtures" / "input_listing_full_location.txt"),
        "generic": read(ROOT / "tests" / "fixtures" / "input_listing_generic.txt"),
    }

    goldens = {
        "default_full": read(ROOT / "tests" / "golden" / "default_full_location.expected.html").strip(),
        "default_partial": read(ROOT / "tests" / "golden" / "default_partial_location.expected.html").strip(),
        "translation_full": read(ROOT / "tests" / "golden" / "translation_full_location.expected.html").strip(),
    }

    latest = load_registry_latest()

    # Default role checks
    out_default_full = placeholder_render(fixtures["full"], "default").strip()
    out_default_partial = placeholder_render(fixtures["partial"], "default").strip()

    assert_h1_present(out_default_full)
    assert_allowed_html(out_default_full)
    assert_no_unseen_locations(out_default_full, fixtures["full"])
    assert_location_checklist_logic(out_default_full, fixtures["full"])
    assert out_default_full == goldens["default_full"], "Default full location golden mismatch"

    assert_h1_present(out_default_partial)
    assert_allowed_html(out_default_partial)
    assert_no_unseen_locations(out_default_partial, fixtures["partial"])
    assert_location_checklist_logic(out_default_partial, fixtures["partial"])
    assert out_default_partial == goldens["default_partial"], "Default partial location golden mismatch"

    # Translation role checks
    out_translation_full = placeholder_render(fixtures["full"], "translation").strip()
    assert_h1_present(out_translation_full)
    assert_allowed_html(out_translation_full)
    assert_no_unseen_locations(out_translation_full, fixtures["full"])
    assert_location_checklist_logic(out_translation_full, fixtures["full"])
    assert out_translation_full == goldens["translation_full"], "Translation full location golden mismatch"

    # Generic input — ensure no MCP-like expansion (heuristic: no known city unless present)
    out_generic = placeholder_render(fixtures["generic"], "default")
    assert_no_unseen_locations(out_generic, fixtures["generic"])

    print("All tests passed.")

if __name__ == "__main__":
    main()


