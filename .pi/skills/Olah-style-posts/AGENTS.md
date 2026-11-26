# Agent instructions

Use `skills/olah-style-paper-posts/SKILL.md` as the authoritative workflow. Never write a paper explainer directly from a figure search without first checking the primary source. Keep exact paper versions, architecture topology, tensor shapes and cited metrics auditable.

## Edit discipline

- Modify the smallest appropriate scope. All article copy belongs in `examples/<slug>/index.html` (or future `posts/`), not inside the shared skill CSS.
- Update standalone SVGs when changing an inline diagram; avoid mismatched variants.
- Maintain `examples/<slug>/evidence.json` for paper results and numerical claims.
- Do not place build metadata or format boasts in article hero, byline or footer; both prohibited ResNet copy patterns are enforced by the validator.
- Keep tests deterministic and review screenshot artifacts manually when topology or CSS changes.
- Run `python -m pytest -q`, static validation and Playwright QA for touched articles.
- For GitHub changes, prefer PRs and include QA evidence; do not assert CI or Pages passed without checking.
