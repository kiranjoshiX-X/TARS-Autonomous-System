# =========================
# voice.py (UPGRADED INTELLIGENCE ++ STABLE)
# =========================

import queue
import sounddevice as sd
import vosk
import json
import threading
import time
import re

# =========================
# MIC PRIORITY
# =========================
PRIMARY_MIC = 2
FALLBACK_MIC = 1

def get_mic():
    devices = sd.query_devices()

    print("\n🎤 Scanning microphones...\n")

    for idx, label in [(PRIMARY_MIC, "Headphone Mic"), (FALLBACK_MIC, "Laptop Mic")]:
        try:
            dev = devices[idx]
            if dev["max_input_channels"] > 0:
                print(f"🎧 Using {label}: {dev['name']} (Index {idx})")
                return idx
        except:
            continue

    for i, d in enumerate(devices):
        if d["max_input_channels"] > 0:
            print(f"🎧 Using Auto Mic: {d['name']} (Index {i})")
            return i

    raise RuntimeError("No mic found")

DEVICE_INDEX = get_mic()

# =========================
# MODEL
# =========================
model = vosk.Model("vosk-model-small-en-us-0.15")

audio_q = queue.Queue()
command_q = queue.Queue()

def callback(indata, frames, time_, status):
    audio_q.put(bytes(indata))

def listen_loop():
    recognizer = vosk.KaldiRecognizer(model, 16000)

    print("🎧 TARS LISTENER ONLINE")

    with sd.RawInputStream(
        device=DEVICE_INDEX,
        samplerate=16000,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=callback
    ):
        print("✅ Microphone connected\n")

        while True:
            data = audio_q.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip().lower()

                if text:
                    print(f"🧠 FINAL HEARD: {text}")
                    command_q.put(text)

threading.Thread(target=listen_loop, daemon=True).start()

# =========================
# 🔥 TEXT CLEANING LAYER (UPGRADED)
# =========================
def clean_text(text):
    if not text:
        return ""

    text = text.lower().strip()

    # remove weird spacing / symbols
    text = re.sub(r"[^a-z0-9\s]", "", text)

    corrections = {
        # movement fixes
        "for world": "forward",
        "for word": "forward",
        "fall forward": "forward",
        "forwarded": "forward",

        # idle fixes (your main issue 🔥)
        "idol": "idle",
        "ideal": "idle",
        "i dull": "idle",
        "go idol": "idle",
        "go idle": "idle",
        "go i did": "idle",

        # wake fixes
        "week": "wake",
        "rick": "wake",

        # direction fixes
        "write": "right",
        "ride": "right",
    }

    for wrong, correct in corrections.items():
        if wrong in text:
            text = text.replace(wrong, correct)

    print(f"🔧 CLEANED INPUT: {text}")  # debug (very useful)

    return text

# =========================
# CLEAN FETCH
# =========================
last = ""
last_time = 0

def listen_command():
    global last, last_time

    if command_q.empty():
        return None

    cmd = command_q.get()

    # 🔥 CLEAN FIRST
    cmd = clean_text(cmd)

    # 🔧 smarter duplicate suppression
    if cmd == last and time.time() - last_time < 1.2:
        return None

    last = cmd
    last_time = time.time()

    return cmd

# =========================
# INTENT PARSER (UPGRADED)
# =========================
def map_command(text):
    if not text:
        return None

    text = text.lower()

    intents = []

    # wake / greeting
    if any(word in text for word in ["tars", "wake", "morning", "hello"]):
        intents.append("WAKE")

    # movement
    if "forward" in text:
        intents.append("MOVE_FORWARD")

    if "back" in text:
        intents.append("MOVE_BACKWARD")

    if "left" in text:
        intents.append("TURN_LEFT")

    if "right" in text:
        intents.append("TURN_RIGHT")

    if "stop" in text or "halt" in text:
        intents.append("STOP")

    # modes
    if "idle" in text or "random" in text:
        intents.append("IDLE")

    if "manual" in text:
        intents.append("WAKE")

    return intents if intents else None