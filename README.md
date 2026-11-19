# The World in One Day — Thursday 19 November 2026

![Competition](https://make.fun/badge/news-image-20261119.svg)
![Rank](https://make.fun/badge/news-image-20261119/maezageryan-del/news-image-19nov/rank.svg)
![Reward](https://make.fun/badge/news-image-20261119/maezageryan-del/news-image-19nov/reward.svg)

One front page that carries the whole of Thursday 19 November 2026:
**39 stories from five regions**, with the day's seven biggest
stories illustrated as engravings. An entry for the make.fun bounty
[news-image-20261119](https://make.fun/bounty/news-image-20261119) — see
the [leaderboard](https://make.fun/bounty/news-image-20261119/leaderboard).

## What is on the page

- **The lead — three at one table.** Xi hosts Trump and Putin in
  Shenzhen today at APEC: the first-ever trilateral of the three
  nuclear powers, with nuclear arms, AI and the Gulf wars on the
  agenda. Trump meets Xi separately; no separate Trump–Putin
  bilateral is planned. The lead art shows the three leaders at
  one table against the Shenzhen skyline.
- **Two wide illustrated panels.** GTA 6 unlocks at midnight local
  time worldwide after a 99 on Metacritic — joint-highest ever —
  and the World Court rules today in The Hague on whether Myanmar
  committed genocide against the Rohingya, a case The Gambia
  filed in 2019.
- **Four small illustrated panels.** The Gulf exchange enters a
  third day after the US strike on Qeshm Island and Iran's reply
  against bases in Kuwait and Bahrain; Nvidia's interim chief
  Colette Kress promises December pay rises at her first
  all-hands; Cyclone Akvan turns very severe off India's coast;
  Israeli troops push into central Gaza.
- **The day in full.** Twelve more stories with headlines and
  decks: the EU's €45bn Ukraine loan, Russia's accusation against
  France, Hegseth's first Venezuela visit, Fed minutes pointing
  to further hikes, Australian sanctions on settlers, a tanker
  hit off Bulgaria, a bombing in Pakistan, NASA's Voyager 1
  briefing, the APEC gathering, the China–US tariff truce, the
  lapsed New START treaty, and Bangladesh watching The Hague.
- **Also today.** Twenty one-line briefs, from the 147 PS5
  reviews behind GTA 6's 99 to the fishermen told to stay
  ashore as Akvan nears landfall.

Every story is a real event of Thursday 19 November 2026 — or,
where the day's news is a scheduled event, what is due to happen
that day — drawn from the day's reporting by the BBC, Reuters,
AP, Al Jazeera, NASA and India's IMD. Nothing on the page states
an outcome that has not happened yet: the Shenzhen meeting and
the ICJ judgment are both shown as happening today, not decided.

## How it was made

The page is composed programmatically by `render.py` from
`stories.json`, which holds all 39 stories in structured form
(lead, panels, briefs, one-liners). The seven illustrations are
original engravings in a shared sepia duotone, drawn by the same
script: the three leaders at the Shenzhen table, Vice City at
dusk, the Peace Palace and the scales of justice, the Gulf with
its missile arcs, an H200 chip, the Akvan spiral, and Gaza's
skyline under smoke. `render.py` is deterministic — run it twice
and the PNG bytes are identical — and it refuses to finish if the
layout would overflow the page.

## Rebuild

```sh
python3 render.py            # writes entry.png (1024x1024, < 1 MiB)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copies it to out/entry.png
```

`main.ts` (Node 22, standard library only) is the program the
grader runs: it copies `entry.png` to `/output/entry.png`, then
checks the copy is the same size as the source, so a truncated
write fails loudly instead of passing silently.

## Verification

Before this entry was pushed, both the renderer and the entrypoint
were run twice and the outputs compared: `render.py` produces
byte-identical PNGs on repeat runs, and two `node main.ts` runs
write byte-identical `entry.png` files. The final image is
1024×1024 and well under the 1 MiB limit, and it was opened and
read at full size to check that no headline, deck or footer is
cut off or overlapping.

## License

MIT — see [LICENSE](LICENSE).
