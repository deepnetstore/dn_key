# dn_key_firefly_swarm

A swarm light game for the DN Key (orig). Flash the same `code.py` onto a bunch
of keys, power them from battery banks, and set them near each other - their
eyes drift into blinking in unison, like fireflies. No master, no pairing, no
config. Touch the art to play with the whole room.

## What it does

- **Sync** - each key broadcasts its blink phase a few times a second over
  ESP-NOW and nudges toward the phases it hears. The swarm converges to blinking
  together and stays there, even as packets drop. A key that reboots snaps back
  into the group's rhythm on the first heartbeat it hears.
- **Touch the FACE** - sends a bright white WAVE through the swarm; every key
  flashes. Spook the room.
- **Touch the LAPTOP logo** - cycles the swarm's COLOR; every key follows.

## Flashing a swarm

Copy `code.py` onto each key's drive (`DN-S3-PY` / `DEEPNET-PY`). It's the same
file on every key - there's no "server" key. Then power each one and place them
together.

## Power matters

These broadcast over a weak 2.4 GHz link, and an under-powered key transmits
weakly - a sleeping phone or a low-current power bank will make one key seem
unresponsive or slow to sync. Give each key a solid power source (a real USB
port or a bank that doesn't throttle) and the swarm behaves. This is also why
color and wave are sent several times: to punch through the lossy link.

## Tuning (top of `code.py`)

- `PERIOD_MS` - blink cycle length (default 1s).
- `COUPLING` - how hard a key pulls toward its neighbors. Gentle (0.15) looks
  smooth; crank it and sync gets faster but jittery when packets drop.
- `SYNC_MS` - how often each key broadcasts its phase.
- `COLORS` - the color cycle. First entry is the startup color.
- `DEBUG` - set `True` to print tx/rx/touch stats to the serial console.

## Notes

- **DN Key (orig) only.** It uses `board.EYES` and the two touch pads. The
  DN Key Pro has different hardware (RGB LED, buttons, TFT) and would run a
  different build.
- `FACE` / `LAPTOP` are mapped to `TOUCH1` / `TOUCH2`. If they feel swapped on
  your unit, flip the two `touchio.TouchIn(...)` lines.
- Don't hold a touch pad while the key powers on - it calibrates its idle
  baseline at boot.
- Runs on both the S3 and S2 (ESP-NOW rides Wi-Fi, so no Bluetooth needed).
