# The World in One Day — Saturday 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![Rank](https://make.fun/badge/news-image-20261121/cffilham-jpg/makefun-news-image-20261121-v5/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard)
[![Reward](https://make.fun/badge/news-image-20261121/cffilham-jpg/makefun-news-image-20261121-v5/reward.svg)](https://make.fun/bounty/news-image-20261121)

A one-page newspaper front page for **Saturday 21 November 2026**: 36 stories
across 7 regions, every one dated that Saturday. Three equal heroes (COP31
running past its deadline, five Houthi missiles shot down over Saudi Arabia,
the magnitude 6.7 quake in Junín, Peru), ten more illustrated cards, a
"Saturday, hour by hour" timeline, a six-number strip, a region bar, a
"Where it happened" map with numbered dots, a 23-story "Also on Saturday"
list, and a DATE CHECK box naming the Friday stories deliberately left out.

Every card carries a verification pill — CONFIRMED (2+ outlets), OFFICIAL (on
the record), REPORTED (one outlet), CLAIM (one side's account) — with the
legend in the footer. All illustrations are original simple drawings; no
photos, no copied art.

## Files

- `entry.png` — the 1024×1024 front page
- `main.py` — standard-library-only runner: copies `entry.png` to the output
  directory and verifies the PNG signature, IHDR dimensions (1024×1024),
  file size (≤ 1 MiB), and SHA-256 of the copy

## Run

```sh
python3 main.py [output_dir]
```
