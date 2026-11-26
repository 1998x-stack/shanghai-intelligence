# Cross-repository PR acceptance and first-batch quality review — 2026-11-22

**Scope:** 5 PRs initially open in three repositories, release and live-site checks, targeted follow-up fixes, and first-batch source audits of xm-posts and math-posts. This is an evidence ledger, not a claim that every page and mathematical argument was reviewed.

## 1. Original P0 backlog — completed

| Repo | Original PR | Final disposition | Commit / reason | Premerge check |
| --- | --- | --- | --- | --- |
| [xm-posts](https://github.com/1998x-stack/xm-posts) | [#179](https://github.com/1998x-stack/xm-posts/pull/179) | CLOSED UNMERGED | Redundant implementation of #180; explanatory comment on #179 | File overlap and branch conflict reviewed |
| xm-posts | [#180](https://github.com/1998x-stack/xm-posts/pull/180) | MERGED | `363d0d3f7a63f62baf4f73fa117f81c7a76a840d` | [PR validation success](https://github.com/1998x-stack/xm-posts/actions/runs/44981906723) |
| [LLM-data-tutorial](https://github.com/1998x-stack/LLM-data-tutorial) | [#6](https://github.com/1998x-stack/LLM-data-tutorial/pull/6) | MERGED | `3ea0c82d78179e13037d70a0854221851a57e5cd` | [PR static quality success](https://github.com/1998x-stack/LLM-data-tutorial/actions/runs/44982284046) |
| LLM-data-tutorial | [#8](https://github.com/1998x-stack/LLM-data-tutorial/pull/8) | MERGED AFTER REPAIRS | `ba1960aabd9e51cd846c4df2c69d0d360bc187d4` | [Final PR static CI success](https://github.com/1998x-stack/LLM-data-tutorial/actions/runs/44993123478) |
| [vllm-tutorial](https://github.com/1998x-stack/vllm-tutorial) | [#2](https://github.com/1998x-stack/vllm-tutorial/pull/2) | MERGED | `b5fc2382376d7350f4a31c29fd747f317eb8611e` | [PR static, Chromium and interaction QA success](https://github.com/1998x-stack/vllm-tutorial/actions/runs/44981861431) |

**Dedupe evidence:** xm-posts #179 and #180 changed the same two files, `scripts/verify_deployed_related.py` and `tests/test_deployed_archive_smoke.py`. Both implemented exact C51 archive traversal via `rel=next`, loop/domain/page-limit guards and canonical RSS checking. Retained #180 and closed #179 rather than merging a conflicting duplicate.

**Conflict evidence:** LLM-data #8 originally diverged from main and was unmergeable. Constructed a two-parent reconciliation commit `c5a79c536d30b19422f8cf695845b2c327c707d3` using exactly the 24 desired changed paths on latest main, preserving the merged chapter 17 fix from #6 (identical `17.html` blob SHA on main and the reconciled branch). Did not force-push or discard main history.

**Content QA and regressions fixed before #8 merge:** `evidence/06.json` correctly used RFC `standard` claim kind, but new validator excluded it; validator and unit test amended. New versions of chapters 21–25 had removed five existing teaching labs, and chapters 23/25 lacked their former MathML. Restored interactive labs and relevant math while keeping upgraded source ledgers and version-pinned text. Corrected chapter 21 sample math and applied evidence-claim coverage tests compatible with legitimate chapter-ledger counts. Final CI successful; earlier failed runs are intentionally not hidden.

## 2. Main-branch CI, Pages and public smoke

| Repo / release | Main static quality | Pages publication | Live/public check | Evidence |
| --- | --- | --- | --- | --- |
| xm-posts `363d0d3` | PASS | PASS | **PASS**: deployed C51 HTML, PDF, archive, RSS, related reading | [Validate & publish 44992687703](https://github.com/1998x-stack/xm-posts/actions/runs/44992687703) — both jobs successful, including public verifier |
| LLM-data `3ea0c82` (#6) | PASS | PASS | Not independently asserted for this intermediate commit | [quality 44992708626](https://github.com/1998x-stack/LLM-data-tutorial/actions/runs/44992708626); [Pages 44992708143](https://github.com/1998x-stack/LLM-data-tutorial/actions/runs/44992708143) |
| LLM-data `ba1960a` (#8) | PASS | PASS | Covered by the subsequent byte-verifying release | [quality 44993162951](https://github.com/1998x-stack/LLM-data-tutorial/actions/runs/44993162951); [Pages 44993162458](https://github.com/1998x-stack/LLM-data-tutorial/actions/runs/44993162458) |
| LLM-data `645d8ad` (follow-up #9) | PASS | PASS | **PASS**: 13 public site files byte-identical to checked-out main | [quality and public check 44993503873](https://github.com/1998x-stack/LLM-data-tutorial/actions/runs/44993503873); [Pages 44993503547](https://github.com/1998x-stack/LLM-data-tutorial/actions/runs/44993503547) |
| vLLM `b5fc238` (#2) | PASS | PASS (separate built-in workflow) | FAIL: custom publish job attempted forbidden Pages settings mutation (HTTP 403) | [custom 44992729564](https://github.com/1998x-stack/vllm-tutorial/actions/runs/44992729564); [Pages 44992729171](https://github.com/1998x-stack/vllm-tutorial/actions/runs/44992729171) |
| vLLM `ba86796` (follow-up #3) | PASS | PASS | FAIL: live verifier found legacy 28.html has no H1; new chapters 01–18 and public bytes tested through chapter 18 | [custom 44993136317](https://github.com/1998x-stack/vllm-tutorial/actions/runs/44993136317); [Pages 44993135930](https://github.com/1998x-stack/vllm-tutorial/actions/runs/44993135930) |
| vLLM `6e03739` (follow-up [#4](https://github.com/1998x-stack/vllm-tutorial/pull/4)) | PASS | PASS (legacy source, via GitHub branch Pages) | **PASS**: 15 public assets byte-identical; modernized H1 gates and legacy chapter 28 H2 gate | [PR 44993479758](https://github.com/1998x-stack/vllm-tutorial/actions/runs/44993479758); [main quality + public smoke 44993652459](https://github.com/1998x-stack/vllm-tutorial/actions/runs/44993652459); [Pages 44993652261](https://github.com/1998x-stack/vllm-tutorial/actions/runs/44993652261) |

**Important:** github.com's "pages build and deployment" being green is not itself an end-to-end client-side Chromium or public content-verification result. In this record, **PASS live** is only used for an actual runner public-site smoke invocation with successful job steps. No GPU or real-vLLM model benchmark was run. The LLM-data post-deploy checker verifies byte consistency of representative pages and SVGs, not browser interactions for all chapters.

## 3. First-batch deep-review progress (parallel)

### math-posts

- Current content registry: **132** registered items, **126 published**, **6 draft**.
- Read each of the 6 draft `evidence.json` records and created [issue #33](https://github.com/1998x-stack/math-posts/issues/33).
- Blockers: Jianping Q20 distinction between secant and tangent endpoint despite corrected discriminant `400−960k²`; Fengxian Q20 vertical-line counterexample; Songjiang Q08/Q09/Q16 missing relation glyphs in source; Songjiang Q20 undefined `k`.
- **L3/L4 NOT VERIFIED:** original user-uploaded PDFs were not available in this audit session. Do not publish drafts based on reconstructed symbols, answer-key inference or editorial hypotheses.
- Queue: obtain original unambiguous PDF scans, independently verify all math and SVG, run responsive Chromium/print/PDF tests, only then change `draft` to `published`.

### xm-posts

- Current registry: **106 published**.
- Inspected first 15 article HTML files: all 15 have one H1, labelled MathML and SVG opening tags, and balanced `figure`/`figcaption` tag counts. Inspected 15 `evidence.json` records: all claims in these files have nonempty source URL, locator and status; benchmark Transformer and ResNet each contain 3 claims.
- Registered [issue #182](https://github.com/1998x-stack/xm-posts/issues/182) with per-topic source/maths/SVG/Chromium/PDF review queue.
- **L3/L4 NOT VERIFIED:** static structure and evidence-field completeness do not prove experimental numbers, the SVG computation topology or browser appearance are scientifically correct.

### vLLM unfinished chapter remediation

- [Issue #5](https://github.com/1998x-stack/vllm-tutorial/issues/5): old 19–28 chapters have H2 but no H1/main; they were not part of PR #2's modernized 01–18 cohort. Modernize those ten independently, add evidence / diagrams / browser checks, and only then broaden the modern semantic QA gate to all 28.

## 4. Remaining acceptance gates

1. **COMPLETED:** vLLM #4 merged as `6e03739ea1a60dc542627d2ca73433a11533f20d`; [main custom QA and public smoke](https://github.com/1998x-stack/vllm-tutorial/actions/runs/44993652459) passed and [branch Pages build](https://github.com/1998x-stack/vllm-tutorial/actions/runs/44993652261) passed. Existing Pages source is `legacy` and the workflow correctly avoids an unauthorized settings mutation.
2. **COMPLETED:** LLM-data #9 merged as `645d8ad3f3c8d880dc161a0b49791c1f6616f5e1`; [public byte checks](https://github.com/1998x-stack/LLM-data-tutorial/actions/runs/44993503873) passed on 13 listed assets, and [Pages](https://github.com/1998x-stack/LLM-data-tutorial/actions/runs/44993503547) passed.
3. **OPEN QUALITATIVE WORK:** continue manual scientific and source-image reviews tracked in math-posts #33, xm-posts #182 and vLLM #5. The independent algebra check for Jianping Q20 and Transformer §05 toy attention example are recorded as narrow verified subclaims on those issues; do not generalize to whole articles.
4. Treat all non-run visual/math/GPU checks as **NOT VERIFIED** rather than silently PASS. Other production automation can open new PRs after this acceptance snapshot; specifically xm-posts #181 (Mamba) was opened during this work and is outside the original five-PR queue.

All GitHub links above are public proof points. This report distinguishes **MERGED / CLOSED**, **CI PASS**, **PAGES PASS**, **PUBLIC SMOKE PASS**, and **NOT VERIFIED**.
