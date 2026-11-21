# news-image-20261120 — The Morning Dispatch, Friday 20 November 2026

A make.fun bounty entry. `main.ts` copies `entry.png` to
`/output/entry.png`. The image is a newspaper front page summing up
Friday 20 November 2026 in six stories, drawn programmatically with
Python PIL (see `render.py`) — no AI-generated image, so every word
stays crisp and readable. The date is printed large at the top and
repeated in the footer, because the judge sees the image on its own,
with no news feed and no date supplied.

## The six stories

1. **NVIDIA SINKS 14% AS SEC EXAMINES ITS ACCOUNTS** — SEC
   enforcement staff are reviewing Nvidia's accounting; shares closed
   at $125.53, down 14.01%, about $491 billion of market value wiped
   out in a day, down 23% on the week — the worst week since 2008 —
   and falling for a seventh straight trading day.
2. **KYIV HIT BY OVERNIGHT MISSILE AND DRONE ATTACK** — Russian
   missiles and drones killed eight people across Ukraine, six in
   Kyiv, damaging the Austrian and Dutch embassies, St Volodymyr's
   Cathedral and a Dnipro bridge; France has asked the UN Security
   Council to meet.
3. **EU AND UK STRIKE LANDMARK THREE-PART AGREEMENT** — At the
   second EU-UK summit in Brussels, deals on food trade, linked
   carbon markets and youth mobility, with up to 100,000 young people
   able to move in each direction.
4. **COP31 DRAFT DROPS ALL FOSSIL-FUEL PHASE-OUT LANGUAGE** — A new
   draft in Antalya deletes every reference to phasing out fossil
   fuels, keeps a 35-by-35 electrification target and acknowledges
   the world will overshoot 1.5°C.
5. **CYCLONE AKVAN MAKES LANDFALL; 372,000 EVACUATED** — Landfall
   near Gopalpur in Odisha with winds of 70–80 km/h, gusting to 90;
   some 372,000 people were moved to safety, with no major damage or
   casualties reported.
6. **SENATE PASSES ENERGY PERMITTING BILL 62–33** — The bipartisan
   American Affordability and Jobs Act speeds up approvals for energy
   projects and requires data centres to pay their own power costs;
   it now goes to the House.

## How to run

Regenerate the image:

```sh
python3 render.py
```

Copy it to the output directory:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes `out/entry.png` (1024×1024 PNG, under 1 MiB). Running
`main.ts` twice produces byte-identical output.
