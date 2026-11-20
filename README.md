[![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/abtravels/news-2026-11-19/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/abtravels/news-2026-11-19/reward.svg)](https://make.fun/bounty/news-image-20261119)

# The World in One Day — Thursday, 19 November 2026

A make.fun bounty entry: one image summing up Thursday 19 November 2026's
world news. The image is drawn programmatically with Python + Pillow
(`draw.py`, deterministic — re-running it writes byte-identical output), and
`main.ts` copies it to the output directory.

## The six stories

- **World Court rules** — the International Court of Justice finds Myanmar
  guilty of genocide against the Rohingya, the first such ruling against a
  state.
- **Shenzhen summit** — Trump, Xi and Putin hold their first three-way
  summit and issue a four-point peace declaration.
- **Anthropic's record IPO** — Anthropic prices its IPO at $83 a share, a
  $1.5 trillion valuation.
- **Gulf attacks widen** — Iran launches fresh strikes against Kuwait and
  Bahrain, widening attacks near the Strait of Hormuz.
- **GTA 6 goes on sale** — Grand Theft Auto VI goes on sale worldwide after
  13 years of waiting.
- **Bangladesh in turmoil** — violence hits 28 districts; Muhammad Yunus's
  ancestral home is set on fire.

## Run it

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes `out/entry.png` (1024×1024, under 1 MiB).
