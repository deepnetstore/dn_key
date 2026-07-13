"""
dn_key firefly swarm

Flash this on a pile of keys, power 'em off battery banks, set 'em near each
other - the eyes drift into blinking together like fireflies. No master, no
pairing, no config. Touch the art to mess with the whole room.

  FACE   -> fire a white WAVE across every key. spook the room.
  LAPTOP -> cycle the swarm's COLOR. everyone follows.

DN Key (orig) only - eyes + two touch pads. Talks over ESP-NOW broadcast, so
there's no wifi to join and no bluetooth needed. Same code.py on every key.

Learned the hard way: send to the broadcast peer EXPLICITLY. send(msg) with no
peer takes esp-now's "all peers" shortcut and just dies with NOT_FOUND (0x3069),
so nothing ever leaves the antenna.

Author: ᧁꫝꪮᦓꪻ
Date: 2026 <3
"""

import time
import board
import neopixel
import touchio
import wifi
import espnow
from supervisor import ticks_ms

# --- knobs ----------------------------------------------------------------
DEBUG = False             # True spits tx/rx/touch stats to the serial console
PERIOD_MS = 1000          # one blink cycle
COUPLING = 0.15           # how hard we lean toward the neighbors we hear.
                          # gentle = smooth. crank it and drops make it twitchy.
SYNC_MS = 200             # how often we shout our phase (~5x/sec)
DECAY = 3.5               # how fast the glow fades out
COLOR_REPEAT = 5          # spam a color change this many times so it lands
WAVE_REPEAT = 6           # same for the wave - a hand on the pad detunes the
                          # antenna, so one lone packet often gets eaten
TOUCH_MARGIN = 2500       # counts above idle before we call it a touch
TOUCH_COOLDOWN_MS = 350   # ignore a pad this long after it fires (kills chatter)
WAVE_COLOR = (255, 255, 255)
COLORS = [
    (0, 255, 120),   # green
    (255, 40, 0),    # red
    (0, 120, 255),   # blue
    (255, 120, 0),   # amber
    (200, 0, 255),   # purple
]
BROADCAST = b"\xff\xff\xff\xff\xff\xff"

# ticks_ms() rolls over at 2**29 ms, so diffs have to be wrap-safe
_TICKS_PERIOD = 1 << 29
_TICKS_MAX = _TICKS_PERIOD - 1
_TICKS_HALF = _TICKS_PERIOD // 2


def ticks_diff(a, b):
    d = (a - b) & _TICKS_MAX
    return ((d + _TICKS_HALF) & _TICKS_MAX) - _TICKS_HALF


# --- hardware -------------------------------------------------------------
pixels = neopixel.NeoPixel(board.EYES, 2, brightness=0.4, auto_write=False)
face = touchio.TouchIn(board.TOUCH1)     # the hood's face
laptop = touchio.TouchIn(board.TOUCH2)   # the DN logo on the laptop


def calibrate(pad, samples=24):
    # read the idle baseline and sit the threshold well above it. don't hold a
    # pad while this runs at boot or it'll bake your finger into the baseline.
    total = 0
    for _ in range(samples):
        total += pad.raw_value
        time.sleep(0.003)
    base = total // samples
    pad.threshold = base + TOUCH_MARGIN
    return base


face_base = calibrate(face)
laptop_base = calibrate(laptop)


def show(color, level):
    v = (int(color[0] * level), int(color[1] * level), int(color[2] * level))
    pixels[0] = v
    pixels[1] = v
    pixels.write()


# --- radio ----------------------------------------------------------------
wifi.radio.enabled = True
try:
    wifi.radio.tx_power = 20   # crank it - the link is weak on battery
except Exception as err:  # noqa: BLE001
    print("tx_power set failed:", err)
now = espnow.ESPNow()
peer = espnow.Peer(mac=BROADCAST)
now.peers.append(peer)

tx_count = 0
tx_err = ""


def send(msg):
    global tx_count, tx_err
    try:
        now.send(msg, peer)   # explicit peer - the "all peers" path is dead
        tx_count += 1
    except Exception as e:  # noqa: BLE001
        tx_err = str(e)


# --- state ----------------------------------------------------------------
phase_ms = 0
synced = False            # snap onto the first beat we hear, then ease in
level = 0.0
color_idx = 0
wave = False
face_prev = False
laptop_prev = False
face_last = 0
laptop_last = 0
rx_count = 0
last_rssi = 0
last_sync = ticks_ms()
last_report = ticks_ms()
last = ticks_ms()
show((0, 0, 0), 0.0)
if DEBUG:
    print("baselines face", face_base, "laptop", laptop_base)


def flash(as_wave):
    global level, wave
    level = 1.4 if as_wave else 1.0
    wave = as_wave


def send_color(idx):
    for _ in range(COLOR_REPEAT):
        send(b"C" + bytes([idx]))
        time.sleep(0.01)


def send_wave():
    for _ in range(WAVE_REPEAT):
        send(b"B")
        time.sleep(0.01)


# --- run ------------------------------------------------------------------
while True:
    t = ticks_ms()
    dt = ticks_diff(t, last) / 1000.0
    last = t
    phase_ms += int(dt * 1000)

    # soak up whatever the swarm sent us
    while True:
        pkt = now.read()
        if not pkt:
            break
        rx_count += 1
        last_rssi = getattr(pkt, "rssi", 0)
        m = pkt.msg
        if len(m) == 2 and m[0:1] == b"P":       # a neighbor's phase
            recv = m[1] * PERIOD_MS // 256
            if not synced:
                phase_ms = recv                  # fresh key -> jump on the beat
                synced = True
            else:
                diff = recv - phase_ms           # already in -> just lean toward it
                if diff > PERIOD_MS // 2:
                    diff -= PERIOD_MS
                elif diff < -PERIOD_MS // 2:
                    diff += PERIOD_MS
                phase_ms = max(0, phase_ms + int(diff * COUPLING))
        elif m == b"B":                          # somebody fired a wave
            flash(True)
            phase_ms = PERIOD_MS
        elif len(m) == 2 and m[0:1] == b"C":     # somebody changed the color
            color_idx = m[1] % len(COLORS)

    # touch the face -> wave the room (rising edge, with a cooldown)
    f = face.value
    if f and not face_prev and ticks_diff(t, face_last) > TOUCH_COOLDOWN_MS:
        face_last = t
        if DEBUG:
            print("face -> wave")
        send_wave()
        flash(True)
    face_prev = f

    # touch the laptop -> next color
    l = laptop.value
    if l and not laptop_prev and ticks_diff(t, laptop_last) > TOUCH_COOLDOWN_MS:
        laptop_last = t
        color_idx = (color_idx + 1) % len(COLORS)
        if DEBUG:
            print("laptop -> color", color_idx)
        send_color(color_idx)
        flash(False)
    laptop_prev = l

    # shout our phase - this is the glue that keeps everyone together
    if ticks_diff(t, last_sync) >= SYNC_MS:
        last_sync = t
        send(b"P" + bytes([(phase_ms * 256 // PERIOD_MS) & 0xFF]))

    # our own blink
    if phase_ms >= PERIOD_MS:
        phase_ms -= PERIOD_MS
        flash(wave)

    # burn the glow down
    if level > 0:
        level = max(0.0, level - DECAY * dt)
        show(WAVE_COLOR if wave else COLORS[color_idx], min(level, 1.0))
        if level == 0.0:
            wave = False

    if DEBUG and ticks_diff(t, last_report) >= 2000:
        last_report = t
        print("tx", tx_count, "rx", rx_count, "rssi", last_rssi,
              "phase", phase_ms, "color", color_idx, "err", repr(tx_err))

    time.sleep(0.005)
