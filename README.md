# Real Estate Prompt Registry

A production-grade Prompt-as-Code repository for managing versioned prompts for a real-estate listing system. Use the registry to resolve the latest active prompts per role.

## What this repo provides

- Versioned prompts for three roles: `default`, `translation`, `assistant`
- Localization integrity and no-fabrication constraints
- MCP fixed parameters (Google Places) support where applicable in prompts
- CI checks: prompt linting, registry validation, required sections, and golden tests
- A prompt registry JSON that maps “latest” aliases to current files
- Clear docs for contributing and the release flow

## Product Evolution Summary (embedded across docs)

- Version 0 (current system intents)
  - Before: Only data cleaning and bare HTML output. Superficial SEO, no content transformation.
  - After mindset for V1: Professional copywriter approach; add content enrichment, market context, quality standards.
  - Output: Cleaned data; lacks persuasive language.

- Version 1
  - Before: Need to move from data cleaner to pro content creator.
  - After mindset for V2: Strategic marketing, buyer psychology, adaptive comms, SEO integration.
  - Output: More readable, has SEO keywords but lacks strategic depth.

- Version 2
  - Before: Professional content transformation achieved but limited strategic direction.
  - After mindset for V3: Few-shot localization; remove hard-coded cities; variable-driven examples; guarantee using the real location from input.
  - Output: Strong marketing tone, but no performance metrics/systematic optimization yet.

- Version 3
  - Before: Strategic direction still limited. Hard-coded examples (e.g., Istanbul, Kadıköy) made the AI always output Istanbul even for other cities.
  - After: Outputs now contain the correct location per city; few-shot examples steer the model to the right pattern; location-agnostic quality standard is ensured.

Active prompts: resolve per role via `registry/prompts.index.json` (`latest`).

## How to use

- Pick a role (`default`, `translation`, `assistant`).
- Use the registry at `registry/prompts.index.json` to resolve the `latest` version for each role.
- Consumers should load the referenced file and supply listing inputs to generate validated HTML outputs.

## Quick start

Requirements:
- Python 3.10+

Install dependencies (none required beyond the standard library). To run checks and tests:

```bash
python -m pip install --upgrade pip
python tools/lint_prompts.py
python tools/validate_registry.py
python tools/check_required_sections.py
python tests/run_tests.py
```

## Running CI locally

The CI workflow mirrors the commands above. See `.github/workflows/ci.yml`. Ensure your prompts conform to:
- Required checks run against the files referenced as `latest`
- Proper JSON MCP block
- HTML tag whitelist in outputs

## Directory structure

See the repository tree in the root of this archive, or browse:
- `prompts/real_estate/...` for all prompt versions
- `registry/` for the prompt index and policies
- `tests/` for fixtures and golden outputs
- `tools/` for lint and validation utilities
- `docs/` for contribution and release process

## Choosing prompt versions

- Stable selection: use the explicit version path (e.g., `prompts/real_estate/default/v3.md`)
- Rolling selection: resolve `latest` via `registry/prompts.index.json`

## License

MIT — see `LICENSE`.


