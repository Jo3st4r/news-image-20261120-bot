# 50 stories, one page — the world on 20 November 2026

**Competition:** make.fun `news-image-20261120` — "Sum up 20 November's world
news in one image". Pool $250, top 50 entries. Entry closes 22 Nov 2026 07:00 WIB.

## The idea

A broadsheet front page: **read the whole world in one page**. Masthead with
the date, a UTC timeline of the day, three lead panels, then **50 numbered
stories** in three columns grouped by beat — Summit & War, Asia, Europe &
Americas, Markets, Tech & Science, India, Sport — and a market ticker plus a
date-check footer.

## The day, in three leads

1. **The G3 aftermath** — Trump, Xi and Putin sign a three-way peace
   declaration in Shenzhen (nuclear risk cuts, Hormuz kept open); Ukraine and
   Taiwan are not named, and allies warn of a "Yalta-style carve-up".
2. **The $81bn debut** — Anthropic prices at $83, opens at $111.50, closes
   $97.17 (+17%) in the largest IPO on record — and the Dow still sheds
   1,101 points.
3. **Akvan comes ashore** — the severe cyclone makes landfall on India's
   Odisha–Andhra coast; schools shut, trains cancelled, evacuations under way.

## How it is built

`tools/render.py` draws `assets/entry.png` (1024×1024 PNG) from the 50
stories embedded in the script — every story was checked against a report
dated 20 November 2026 (Reuters world summary, Investors/WSJ market
coverage, Indian 20 Nov headlines, Philippine Star 20 Nov headlines,
BJ Sports). `main.py` copies that image to `/output/entry.png`, so both
harness runs write identical bytes. No network at run time.

```sh
python3 tools/render.py assets/entry.png   # regenerate the poster
python3 main.py                            # copy it to /output/entry.png
```

## Files

- `main.py` — the entry program (copies the poster)
- `tools/render.py` — the poster generator (Pillow, DejaVu fonts)
- `assets/entry.png` — the poster
- `README.md`, `LICENSE` (MIT)

## Note

20 November 2026 is also World Children's Day.
