# Release Flow

This project uses a simple dev → staging → prod model for prompts and tooling.

## Steps
1. Branch from `main` for feature work.
2. Open PR; ensure CI passes.
3. Merge to `main` (dev).
4. Tag release with `vX.Y.0` (e.g., `v3.1.0`) when ready.
5. Update `registry/prompts.index.json` to set `latest` as needed.
6. Publish release notes referencing `CHANGELOG.md`.

## Discipline
- Always record changes in `CHANGELOG.md`.
- Keep prompts backward compatible within a minor line when possible.
- Avoid breaking consumers by changing `latest` without notice.


