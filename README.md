# The World in One Day — Monday 23 November 2026

[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/sularno67/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/sularno67/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

A newspaper-style front page summing up the world news of Monday 23 November 2026, drawn entirely in code with PIL.

**Lead stories on the page**

- **COP31 ends with no deal** — climate talks in Antalya collapsed after two days of overtime; the EU and about 130 nations rejected a draft that left out fossil fuels, the first COP to fail since 2009.
- **Boy, 7, pulled alive from rubble** — rescuers freed a seven-year-old after 14 hours under a collapsed block in Dymer, north of Kyiv; Russian strikes killed at least 11 people.
- **AI sell-off rattles world markets** — Japan's Nikkei fell 5.06% and the S&P 500 slid 3.7% on fears AI shares are overpriced.
- **Democrats' biggest House win since 1992** — at least 258 House seats after flipping a North Carolina seat in a recount.
- **Alcaraz wins first ATP Finals title** — beat world No. 1 Alexander Zverev 6–2, 7–6 in Turin.
- **South Korea exports top $1 trillion** — a first, driven by demand for AI chips.
- **In brief:** Israeli strike on Beirut, a magnitude 6.5 quake off Vanuatu, the capture of FBI fugitive "El Chapo Isidro", and FIFA confirming the UK as host of the 2035 Women's World Cup.

**Files**

- `render.py` — the PIL renderer that draws the front page (build-time only; needs Pillow locally).
- `entry.png` — the generated 1024×1024 front page.
- `main.py` — the stdlib-only entrypoint: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).

Run the renderer with `python3 render.py`, then check determinism with `MAKEFUN_OUTPUT_DIR=out1 python3 main.py` twice into different directories and compare sha256 sums.
