# =========================
# tars_voice.py (FINAL - NO PERMISSION ERROR)
# =========================

import asyncio
import edge_tts
from playsound import playsound
import threading
import uuid
import os

VOICE = "en-US-JennyNeural"


# =========================
# ASYNC SPEAK
# =========================
async def _speak_async(text, filename):
    communicate = edge_tts.Communicate(text=text, voice=VOICE)
    await communicate.save(filename)


def _run_speak(text):
    try:
        # 🔥 UNIQUE FILE NAME EVERY TIME
        filename = f"tars_{uuid.uuid4().hex}.mp3"

        asyncio.run(_speak_async(text, filename))
        playsound(filename)

        # cleanup (optional but good)
        if os.path.exists(filename):
            os.remove(filename)

    except Exception as e:
        print("❌ VOICE ERROR:", e)


def speak(text):
    threading.Thread(target=_run_speak, args=(text,), daemon=True).start()


# =========================
# RESPONSES
# =========================
def tars_response(cmd):
    import random

    responses = {
        "MOVE_FORWARD": [
            "Moving forward.",
            "Advancing.",
            "Going ahead.",
            "Forward. Try not to regret this.",
            "Proceeding. Confidence: questionable."
        ],
        "MOVE_BACKWARD": [
            "Reversing.",
            "Moving backward.",
            "Retreating. Smart.",
            "Backtracking. I approve."
        ],
        "TURN_LEFT": [
            "Turning left.",
            "Rotating left.",
            "Left turn. Bold choice.",
            "Left. Let’s hope this was intentional."
        ],
        "TURN_RIGHT": [
            "Turning right.",
            "Rotating right.",
            "Right turn initiated.",
            "Right. This could go either way."
        ],
        "STOP": [
            "Stopping.",
            "System halted.",
            "Finally, a good decision.",
            "Stopped. Crisis avoided."
        ]
    }

    return random.choice(responses.get(cmd, ["I have no idea what that means."]))