#!/usr/bin/env python3
"""news-image-20261119 — sum up 19 November 2026's world news in one image.

Writes exactly one image to /output/entry.png (1024x1024 PNG, < 1 MiB).

How it works
------------
* Preferred path: draw the front-page poster from scratch with Pillow.
  Every story in it was verified against real reporting of 19 Nov 2026
  (UN News, Reuters, CNN, Le Monde, and the day's news round-ups):
    1. ICJ rules Myanmar committed genocide against the Rohingya —
       the first time the World Court has held a state responsible.
    2. Trump, Xi and Putin hold their first three-way summit in Shenzhen.
    3. COP31 climate talks in Antalya, ministers trying to unblock them.
    4. EU proposes a EUR 45bn loan for Ukraine.
    5. Aid groups score the Gaza peace plan 4 out of 26.
    6. Anthropic prices a record IPO at $83 a share.
    7. Ticker: Bangladesh unrest; record $190.4m Van Gogh sale;
       Mongolia's president resigns.
* Fallback path: if Pillow is not installed in the grading environment,
  copy the pre-rendered image shipped in this repo (assets/entry.png),
  which was produced by this same drawing code. The output is identical
  either way.

Determinism: no network, no clock, no randomness, no environment input.
Running this program twice writes byte-identical output.
Only the Python standard library is required for the fallback path.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.join(HERE, "assets", "entry.png")
OUT_DIR = "/output"
OUT_PATH = os.path.join(OUT_DIR, "entry.png")

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (246, 241, 231, 255)
INK = (24, 24, 24, 255)
RED = (178, 34, 34, 255)
NAVY = (31, 58, 95, 255)
GOLD = (176, 141, 58, 255)
GREY = (90, 86, 78, 255)
LIGHT_LINE = (24, 24, 24, 255)
CARD = (255, 253, 247, 255)
DARK_STRIP = (24, 24, 24, 255)

# ---------------------------------------------------------------- fonts
_FONT_CANDIDATES = {
    "serif_bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
    ],
    "serif": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
    ],
    "sans_bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    ],
    "sans": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    ],
}


def _load_fonts():
    """Return a dict of ImageFont objects, falling back to the bitmap font."""
    from PIL import ImageFont

    fonts = {}

    def pick(kind, size):
        for path in _FONT_CANDIDATES[kind]:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    continue
        return ImageFont.load_default()

    fonts["masthead"] = pick("serif_bold", 50)
    fonts["dateline"] = pick("sans_bold", 20)
    fonts["kicker"] = pick("sans_bold", 19)
    fonts["headline"] = pick("serif_bold", 48)
    fonts["headline2"] = pick("serif_bold", 32)
    fonts["body"] = pick("serif", 22)
    fonts["body2"] = pick("serif", 21)
    fonts["card_head"] = pick("sans_bold", 20)
    fonts["card_body"] = pick("serif", 20)
    fonts["ticker"] = pick("sans_bold", 15)
    fonts["footer"] = pick("sans", 16)
    fonts["chip"] = pick("sans_bold", 19)
    return fonts


def _wrap(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def _draw_wrapped(draw, x, y, text, font, max_width, fill, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = int(font.size * 1.32)
    for line in _wrap(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def _text_h(font):
    return int(font.size * 1.32)


def _center(draw, cx, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)


def _rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def _draw_scales(draw, cx, cy, s, fill):
    """Simple scales-of-justice emblem, drawn from straight lines."""
    # top beam
    draw.line([(cx - s, cy - s * 0.55), (cx + s, cy - s * 0.55)],
              fill=fill, width=5)
    draw.line([(cx, cy - s * 0.85), (cx, cy + s * 0.75)], fill=fill, width=5)
    draw.ellipse([cx - 7, cy - s * 0.98, cx + 7, cy - s * 0.72], fill=fill)
    for sign in (-1, 1):
        x = cx + sign * s
        draw.line([(x, cy - s * 0.55), (x, cy + s * 0.05)], fill=fill, width=4)
        # pan: shallow triangle bowl
        draw.polygon([(x - s * 0.42, cy + s * 0.05),
                      (x + s * 0.42, cy + s * 0.05),
                      (x, cy + s * 0.48)], outline=fill, width=4)
    # base
    draw.line([(cx - s * 0.45, cy + s * 0.75), (cx + s * 0.45, cy + s * 0.75)],
              fill=fill, width=5)


def _draw_globe(draw, cx, cy, r, fill):
    """Simple globe: circle with two meridian arcs and one latitude line."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fill, width=4)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 250, 470, fill=fill, width=3)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 70, 290, fill=fill, width=3)
    draw.ellipse([cx - int(r * 0.45), cy - r, cx + int(r * 0.45), cy + r],
                 outline=fill, width=3)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=fill, width=3)


def draw_image():
    from PIL import Image, ImageDraw

    fonts = _load_fonts()
    img = Image.new("RGBA", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin
    X0, X1 = M, W - M

    # outer double border
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    d.rectangle([22, 22, W - 23, H - 23], outline=INK, width=1)

    # ---------------- masthead ----------------
    y = 36
    _center(d, W // 2, y, "THE WORLD IN ONE PAGE", fonts["masthead"], INK)
    y += 62
    _rule(d, X0, y, X1, width=3, fill=RED)
    y += 10
    _center(d, W // 2, y, "T H U R S D A Y  •  1 9  N O V E M B E R  2 0 2 6",
            fonts["dateline"], RED)
    y += 30
    _rule(d, X0, y, X1, width=3, fill=INK)
    y += 12

    # ---------------- lead story: ICJ ----------------
    _center(d, W // 2, y, "THE HAGUE  —  A FIRST IN 80 YEARS",
            fonts["kicker"], NAVY)
    y += 26
    lead_head = "WORLD COURT FINDS MYANMAR GUILTY OF GENOCIDE"
    y = _draw_wrapped(d, X0, y, lead_head, fonts["headline"], X1 - X0, INK,
                      leading=54)
    y += 4
    _rule(d, X0, y, X1, width=1, fill=GREY)
    y += 10
    # body text left, scales emblem right
    body_w = 640
    lead_body = (
        "The International Court of Justice rules Myanmar committed "
        "genocide against the Rohingya in 2017 — the first time the "
        "World Court has held a state responsible. The Gambia brought "
        "the case in 2019; the court orders reparations and the safe "
        "return of the displaced."
    )
    _draw_wrapped(d, X0, y, lead_body, fonts["body"], body_w, INK)
    # emblem panel
    ex0, ey0, ex1, ey1 = 716, y - 6, X1, y + 148
    d.rectangle([ex0, ey0, ex1, ey1], outline=NAVY, width=2)
    _draw_scales(d, (ex0 + ex1) // 2, (ey0 + ey1) // 2 + 10, 46, NAVY)
    d.text(((ex0 + ex1) // 2 - 34, ey1 - 26), "I C J", font=fonts["chip"],
           fill=NAVY)
    y = ey1 + 12
    _rule(d, X0, y, X1, width=3, fill=INK)
    y += 10

    # ---------------- second story: Shenzhen summit ----------------
    _center(d, W // 2, y, "THREE LEADERS, ONE TABLE",
            fonts["kicker"], RED)
    y += 24
    _center(d, W // 2, y, "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
            fonts["headline2"], INK)
    y += 44
    # three flag-colour discs: US, China, Russia
    discs = [
        ("USA", NAVY),
        ("CHN", RED),
        ("RUS", (90, 90, 90, 255)),
    ]
    disc_r = 30
    total_w = 3 * (disc_r * 2) + 2 * 26
    sx = W // 2 - total_w // 2
    for i, (label, colour) in enumerate(discs):
        cx = sx + i * (disc_r * 2 + 26) + disc_r
        cy = y + disc_r
        d.ellipse([cx - disc_r, cy - disc_r, cx + disc_r, cy + disc_r],
                  fill=colour)
        d.ellipse([cx - disc_r, cy - disc_r, cx + disc_r, cy + disc_r],
                  outline=INK, width=2)
        _center(d, cx, cy - 12, label,
                fonts["chip"], (255, 255, 255, 255))
    y += disc_r * 2 + 10
    summit_body = (
        "The first three-way summit ends with a four-point “Declaration "
        "toward Peace” and new talks on nuclear risk — but no major deal "
        "on Ukraine."
    )
    _draw_wrapped(d, X0 + 60, y, summit_body, fonts["body2"], X1 - X0 - 120,
                  INK)
    y += _text_h(fonts["body2"]) * 2 + 10
    _rule(d, X0, y, X1, width=3, fill=INK)
    y += 10

    # ---------------- 2x2 grid ----------------
    cards = [
        ("CLIMATE  •  ANTALYA", RED,
         "COP31 ministers race to unblock the climate talks in Antalya."),
        ("EUROPE  •  BRUSSELS", NAVY,
         "The EU proposes a €45 billion loan to keep Ukraine funded."),
        ("GAZA", GOLD,
         "Aid groups score the Gaza peace plan 4 out of 26."),
        ("MARKETS  •  NEW YORK", NAVY,
         "Anthropic prices a record IPO at $83 a share."),
    ]
    gap = 12
    cw = (X1 - X0 - gap) // 2
    ch = 96
    for i, (head, colour, text) in enumerate(cards):
        cx0 = X0 + (i % 2) * (cw + gap)
        cy0 = y + (i // 2) * (ch + gap)
        d.rectangle([cx0, cy0, cx0 + cw, cy0 + ch], fill=CARD,
                    outline=INK, width=2)
        d.rectangle([cx0, cy0, cx0 + 8, cy0 + ch], fill=colour)
        _draw_wrapped(d, cx0 + 22, cy0 + 9, head, fonts["card_head"],
                      cw - 36, colour, leading=24)
        _draw_wrapped(d, cx0 + 22, cy0 + 37, text, fonts["card_body"],
                      cw - 36, INK, leading=25)
    y += 2 * ch + gap + 12

    # ---------------- ticker ----------------
    _rule(d, X0, y, X1, width=3, fill=INK)
    y += 8
    ty0 = y
    d.rectangle([X0, ty0, X1, ty0 + 46], fill=DARK_STRIP)
    ticker = (
        "ALSO:  Bangladesh unrest   •   Record $190.4m Van Gogh sale   •   "
        "Mongolia's president resigns"
    )
    tw = d.textlength(ticker, font=fonts["ticker"])
    d.text(((W - tw) / 2, ty0 + 13), ticker, font=fonts["ticker"],
           fill=(255, 255, 255, 255))
    y = ty0 + 46 + 10
    _center(d, W // 2, y, "ONE IMAGE  •  THE DAY'S WORLD NEWS  •  19 NOVEMBER 2026",
            fonts["footer"], GREY)

    return img.convert("RGB")


def _write_png(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, format="PNG", optimize=True)


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    try:
        from PIL import Image  # noqa: F401  (Pillow present?)
        img = draw_image()
        _write_png(img, OUT_PATH)
        method = "drawn with Pillow"
    except ImportError:
        if not os.path.exists(ASSET):
            raise SystemExit(
                "Pillow is not installed and no pre-rendered asset "
                "was found at assets/entry.png"
            )
        shutil.copyfile(ASSET, OUT_PATH)
        method = "copied pre-rendered assets/entry.png"

    size = os.path.getsize(OUT_PATH)
    with open(OUT_PATH, "rb") as f:
        head = f.read(8)
    assert head == b"\x89PNG\r\n\x1a\n", "output is not a PNG"
    assert size <= 1024 * 1024, f"output {size} bytes exceeds 1 MiB"
    print(f"wrote {OUT_PATH} ({size} bytes, sha256={_sha256(OUT_PATH)}) [{method}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
