# Sump math

Sump pump sizing arithmetic: the pit names the liters, the liters name the pump, and the outage names the backup.

Live at https://ilanis-agent.github.io/sumpmath/

## The three tools

- **Pit plan** - liters = pi x (diameter/2)^2 x rise / 1000, rounded to one decimal, with teacup, bucket and drum bands.
- **Storm plan** - flow = liters x cycles an hour, share of a labeled 2000 L/h pump, with loafing, working-hard and undersized bands.
- **Backup plan** - liters = flow x outage hours, with short-watch, within-battery-reach (labeled 4000 L) and generator-conversation bands.

## Formulas and limits

- Liters round to one decimal and flows to whole liters (round half up), mirroring the oracle float-for-float.
- Every number the app borrows is labeled in the interface: pump capacity, battery reach, short watch.
- Illustrative planning arithmetic only. A sump is a pump, a check valve and a discharge line; the math sizes the pump, not the waterproofing. Water and electricity share no room: a GFCI outlet, a tested backup, and a plumber for anything that surprises you.

## Development

- `engine.js` - calculation and render engine (browser global `SumpMath`, CommonJS for tests).
- `oracle.py` - Python mirror of the engine; regenerates `expected.json`.
- `test.js` - runs every case through the engine and compares fields and render strings: `node test.js`.
