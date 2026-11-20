# STATUS — news-image-20261119

**Status: BUILT, NOT SUBMITTED — blocked on GitHub, not on code.**

Date: 20 November 2026. Account: @f-alamsyah (wallet
`ApPTBAszEh5yp1NACphvdzwXcZjQanWBEsrZCyeq5ppz`). Prize $250.
Entries close 2026-11-21T00:00:00Z (Sat 21 Nov 07:00 WIB). Day cap: 3 left.

## What is ready

Local repo at `~/workspace/makefun/bounties/news-image-20261119/`,
committed locally (commit `268dd3232e759da7af664597a58f8bc3945ced10`):

| File | Notes |
|---|---|
| `main.py` | Entrypoint. Draws the 1024×1024 front-page poster with Pillow; falls back to copying `assets/entry.png` (byte-identical) if Pillow is absent. No network, no clock, no randomness. |
| `assets/entry.png` | Pre-rendered poster, 120,854 bytes (< 1 MiB). |
| `LICENSE` | MIT. |
| `README.md` | What it does, how to run, verification. |
| `.makefun/owner.json` | `{"wallet": "ApPTBAszEh5yp1NACphvdzwXcZjQanWBEsrZCyeq5ppz"}` — required because the account has no GitHub login. |
| `kit-manifest.json` | The kit endpoint's manifest response (see blocker below). |
| `.gitignore` | Excludes `__pycache__`. |

## Verification (local, 20 Nov 2026)

* `python3 main.py` → `/output/entry.png`, 1024×1024 RGB PNG,
  120,854 bytes, SHA-256
  `eb71a0297840ffaccc681ca8951fb32c87e46824c1f4446627c7ef445b2694c7`.
* Second run → **identical SHA-256** (deterministic, as the rules require:
  the program runs twice and both runs must write the same bytes).
* Pillow-blocked run → fallback copy path, **identical SHA-256**.
* Image visually checked: all text fits, no overflow; lead story (ICJ /
  Myanmar genocide ruling), Shenzhen summit, COP31, EU €45bn Ukraine
  loan, Gaza peace plan 4/26, Anthropic $83 IPO, ticker
  (Bangladesh unrest, record $190.4m Van Gogh, Mongolia president resigns).
* All stories verified against real 19 Nov 2026 reporting (UN News,
  Reuters, CNN, Le Monde, day round-ups). Nothing was fabricated.

## Why it is BLOCKED (not submitted)

1. **@f-alamsyah has no GitHub linked (`github_login: null`).**
   Submission requires a public `repo_url` + 40-char `commit_sha`, and
   no GitHub username exists to invent. Nothing was submitted.
2. **Kit tarball not retrievable.** `GET
   https://make.fun/api/competitions/news-image-20261119/kit` returns
   only a JSON manifest (`agent-fun/kit/v1`, bundle
   `1c4dd40e…fd11d`), not a tar.gz — tried `?format=tar.gz`,
   `/kit/bundle`, `/kit/download`, gzip/octet-stream `Accept` headers,
   and content-addressed `/api/bundles/<sha>` style paths; all 404 or
   still the manifest. So `RULES.txt` / `kit.json` / `cli/makefun.mjs`
   could not be unpacked and **`grade-local` could not be run**.
   The entry was instead built to the competition's own published rules
   (from `GET /api/competitions/news-image-20261119`): 1024×1024,
   ≤ 1 MiB, deterministic, no network, `main.py` at repo root — all
   verified locally. The bundle/transcripts deliverable also cannot be
   produced without the kit CLI.

## What kang still needs to provide

1. **A GitHub username** (link GitHub to the make.fun account, or give
   the username) — then create a public repo (e.g.
   `news-image-20261119`), push this directory to it, and share the
   `repo_url` + `commit_sha`.
2. **(Optional but recommended)** a way to fetch the real kit tarball
   (e.g. download it from make.fun in a browser) so `grade-local` and
   the transcript bundle can be run before submitting.
3. After that: submit via the kit CLI before **Sat 21 Nov 07:00 WIB**
   (deadline 2026-11-21T00:00:00Z). Day quota: 3 submissions left.

## Update 2026-11-20 ~22:31 WIB — GitHub username known: vedreal
- Kang's GitHub username is vedreal — https://github.com/vedreal, 11 public repos, created 2025-11-17, verified via GitHub API.
- Intended repo (ready to push, not yet pushed): https://github.com/vedreal/news-image-20261119
- STILL BLOCKED on linking: vedreal is NOT yet linked to make.fun account @f-alamsyah (github_login null at 22:24 WIB). Kang must link GitHub himself on make.fun profile; Bre cannot link it. Do NOT submit until kang confirms GitHub is linked.
