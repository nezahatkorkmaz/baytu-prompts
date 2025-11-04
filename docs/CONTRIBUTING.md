# Contributing

Thanks for your interest in contributing!

## Pull Requests
- Create feature branches from `main`.
- Keep changes scoped and atomic.
- Include tests and update docs when applicable.
- Ensure CI passes locally before opening a PR.

## Code Review
- At least one approval required.
- Address feedback promptly.
- Keep discussions constructive and focused on user value and safety.

## Versioning
- Semantic Versioning for prompts and tooling.
- Prompt versions live under `prompts/.../<role>/vX.Y.md`.
- Update `registry/prompts.index.json` when adding new versions.
- Update `CHANGELOG.md` with user-facing changes.

## Quality
- No fabrication: content must respect input truth.
- Localization safety: no hard-coded example leakage.
- HTML whitelist enforced: headings, paragraphs, lists, strong.


