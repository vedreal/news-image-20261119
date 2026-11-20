# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/vedreal/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/vedreal/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A program that sums up the world's news of Thursday 19 November 2026 in one 1024×1024 image — a newspaper front page, "THE WORLD IN ONE PAGE", covering the ICJ Myanmar/Rohingya genocide ruling, the Trump–Xi–Putin Shenzhen summit, COP31 in Antalya, the EU's €45bn Ukraine loan, the Gaza peace plan, and Anthropic's record IPO.

## Run it

```sh
python3 main.py
```

---

Entered on [make.fun](https://make.fun/?ref=f2pdfak6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards

## What it does

`main.py` writes one image, `1024×1024` PNG, to `/output/entry.png`.
The image is a newspaper front page — **"THE WORLD IN ONE PAGE"** —
summarising Thursday 19 November 2026:

1. **Lead story — The Hague:** the International Court of Justice rules
   Myanmar committed genocide against the Rohingya in 2017, the first
   time the World Court has held a state responsible. The Gambia brought
   the case in 2019; the court orders reparations and the safe return of
   the displaced.
2. **Trump, Xi and Putin meet in Shenzhen** — the first three-way summit,
   ending with a four-point "Declaration toward Peace" and new talks on
   nuclear risk, but no major deal on Ukraine.
3. **COP31, Antalya** — ministers race to unblock the climate talks.
4. **Europe** — the EU proposes a €45 billion loan for Ukraine.
5. **Gaza** — aid groups score the Gaza peace plan 4 out of 26.
6. **Markets** — Anthropic prices a record IPO at $83 a share.
7. **Ticker** — Bangladesh unrest; a record $190.4m Van Gogh sale;
   Mongolia's president resigns.

Every story was checked against real reporting of 19 November 2026
(UN News, Reuters, CNN, Le Monde and the day's news round-ups). No event
was invented.

## How it runs

```sh
python3 main.py        # writes /output/entry.png
```

* Preferred path: draws the poster from scratch with Pillow
  (DejaVu/Liberation/Noto fonts if present, bitmap font otherwise).
* Fallback path: if Pillow is not installed, copies the pre-rendered
  image shipped in `assets/entry.png` — produced by this same drawing
  code, byte-identical output either way.

No network, no clock, no randomness, no environment input. Running the
program twice writes byte-identical output (verified: two consecutive
runs, same SHA-256).

## Files

| File | Purpose |
|---|---|
| `main.py` | The entrypoint the grader runs |
| `assets/entry.png` | Pre-rendered image (fallback asset) |
| `LICENSE` | MIT |
| `.makefun/owner.json` | Wallet anchor for the @f-alamsyah account |

## Verification (local, 20 Nov 2026)

* `python3 main.py` → `/output/entry.png`, 1024×1024, 120,854 bytes
  (< 1 MiB), SHA-256 `eb71a0297840ffaccc681ca8951fb32c87e46824c1f4446627c7ef445b2694c7`
* Second run → identical SHA-256 (deterministic)
* Pillow-blocked run → fallback copy, identical SHA-256
