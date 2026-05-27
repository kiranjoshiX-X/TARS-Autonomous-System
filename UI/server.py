# =========================================================
# F.R.I.D.A.Y AI OPERATING SYSTEM
# =========================================================

from flask import Flask, send_from_directory
from flask_socketio import SocketIO

import os
import sys
import time
import random
import threading
import asyncio

import requests
import edge_tts
import ollama

# =========================================================
# CONNECT ROOT
# =========================================================

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from state import robot_state

# =========================================================
# FLASK
# =========================================================

app = Flask(__name__)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)

# =========================================================
# CONFIG
# =========================================================

CITY = "Bangalore"

WEATHER_API_KEY = "130a68433e6c5cec8f561ff1cdde0d8c"

VOICE = "en-US-AriaNeural"

AI_MODEL = "phi3:mini"

# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are FRIDAY.

A futuristic female AI assistant.

PERSONALITY:
- calm
- intelligent
- witty
- concise
- loyal
- cinematic
- subtle dry humor

RULES:
- maximum 1 short sentence
- maximum 18 words
- no markdown
- no narration
- no roleplay
- no emojis
- no essays
- no bullet points
- no fantasy dialogue
- speak naturally
- complete proper sentences
- never say "As an AI"
- never say "FRIDAY:"
- never explain yourself
"""

# =========================================================
# ROUTES
# =========================================================

@app.route("/")
def index():

    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route("/static/<path:filename>")
def static_files(filename):

    return send_from_directory(
        "static",
        filename
    )

# =========================================================
# VOICE
# =========================================================

voice_lock = threading.Lock()

async def generate_voice(text, filename):

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE
    )

    await communicate.save(filename)

def speak(text):

    with voice_lock:

        try:

            if not os.path.exists("static"):
                os.makedirs("static")

            filename = "static/voice.mp3"

            # DELETE OLD FILE
            if os.path.exists(filename):
                os.remove(filename)

            asyncio.run(
                generate_voice(text, filename)
            )

            # SMALL DELAY
            time.sleep(0.15)

            # SEND TO FRONTEND
            socketio.emit(
                "play_voice",
                {
                    "file": f"/static/voice.mp3?cache={time.time()}"
                }
            )

        except Exception as e:

            print("VOICE ERROR:", e)

# =========================================================
# WEATHER
# =========================================================

def get_weather():

    try:

        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={CITY}"
            f"&appid={WEATHER_API_KEY}"
            f"&units=metric"
        )

        data = requests.get(url).json()

        temp = round(data["main"]["temp"], 1)
        feels = round(data["main"]["feels_like"], 1)
        humidity = data["main"]["humidity"]

        desc = data["weather"][0]["description"]

        return (
            f"{CITY} has {desc}. "
            f"Temperature {temp} degrees Celsius. "
            f"Feels like {feels}. "
            f"Humidity {humidity} percent."
        )

    except Exception as e:

        print("WEATHER ERROR:", e)

        return "Weather systems temporarily unavailable."

# =========================================================
# AI
# =========================================================

def clean_ai_response(text):

    text = (
        text
        .replace('"', "")
        .replace("FRIDAY:", "")
        .replace("As an AI", "")
        .replace("\n", " ")
        .strip()
    )

    banned_words = [

        "###",
        "solution",
        "document",
        "markdown",
        "instruction",
        "assistant",
        "user:",
        "<|",
        "chapter",
        "example"
    ]

    for word in banned_words:

        if word.lower() in text.lower():

            return "That response concerns me slightly."

    # CLEAN SENTENCE
    if "." in text:
        text = text.split(".")[0] + "."

    # SAFETY
    if len(text) < 3:
        return "Systems operational."

    # LIMIT
    if len(text) > 140:
        text = text[:140]

    return text

def ask_ai(user_text):

    try:

        response = ollama.chat(

            model=AI_MODEL,

            messages=[

                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },

                {
                    "role": "user",
                    "content": user_text
                }

            ],

            options={

                "temperature": 0.4,
                "top_p": 0.7,
                "top_k": 20,

                "num_predict": 22,

                "num_ctx": 128,

                "repeat_penalty": 1.2,

                "stop": [
                    "\n",
                    "User:",
                    "Assistant:",
                    "###",
                    "<|"
                ]
            }
        )

        ai_text = response["message"]["content"]

        return clean_ai_response(ai_text)

    except Exception as e:

        print("AI ERROR:", e)

        return "Neural systems temporarily unstable."

# =========================================================
# INTENT DETECTION
# =========================================================

def detect_intent(cmd):

    cmd = cmd.lower().strip()

    words = cmd.split()

    # =========================
    # MOVEMENT
    # =========================

    if any(word in words for word in [
        "forward",
        "ahead"
    ]):
        return "FORWARD"

    elif any(word in words for word in [
        "back",
        "backward",
        "reverse"
    ]):
        return "BACKWARD"

    elif "left" in words:
        return "LEFT"

    elif "right" in words:
        return "RIGHT"

    elif "stop" in words:
        return "STOP"

    elif "idle" in words:
        return "IDLE"

    # =========================
    # WEATHER
    # =========================

    elif any(word in words for word in [
        "weather",
        "temperature",
        "climate"
    ]):
        return "WEATHER"

    # =========================
    # STATUS
    # =========================

    elif any(word in words for word in [
        "status",
        "battery",
        "system"
    ]):
        return "STATUS"

    # =========================
    # JOKES
    # =========================

    elif any(word in words for word in [
        "joke",
        "funny"
    ]):
        return "JOKE"

    return "CHAT"

# =========================================================
# RESPONSE HELPERS
# =========================================================

FORWARD_RESPONSES = [
    "Moving forward.",
    "Advancing ahead.",
    "Proceeding carefully.",
    "Forward movement engaged."
]

BACKWARD_RESPONSES = [
    "Moving backward.",
    "Reversing carefully.",
    "Backward movement engaged."
]

LEFT_RESPONSES = [
    "Turning left.",
    "Rotating left.",
    "Left turn engaged."
]

RIGHT_RESPONSES = [
    "Turning right.",
    "Rotating right.",
    "Right turn engaged."
]

STOP_RESPONSES = [
    "Motion halted.",
    "Stopping movement.",
    "Systems standing by."
]

JOKES = [
    "Your cable management remains deeply concerning.",
    "I've seen safer engineering in microwave tutorials.",
    "Your debugging strategy appears emotionally driven."
]

# =========================================================
# TELEMETRY LOOP
# =========================================================

def telemetry_loop():

    while True:

        socketio.emit(
            "telemetry",
            robot_state
        )

        time.sleep(0.1)

# =========================================================
# COMMAND HANDLER
# =========================================================

@socketio.on("command")
def handle_command(data):

    cmd = data.get("cmd", "").strip()

    intent = detect_intent(cmd)

    # =====================================================
    # MOVEMENT
    # =====================================================

    if intent == "FORWARD":

        robot_state["position"][1] += 1

        response = random.choice(FORWARD_RESPONSES)

    elif intent == "BACKWARD":

        robot_state["position"][1] -= 1

        response = random.choice(BACKWARD_RESPONSES)

    elif intent == "LEFT":

        response = random.choice(LEFT_RESPONSES)

    elif intent == "RIGHT":

        response = random.choice(RIGHT_RESPONSES)

    elif intent == "STOP":

        response = random.choice(STOP_RESPONSES)

    # =====================================================
    # WEATHER
    # =====================================================

    elif intent == "WEATHER":

        response = get_weather()

    # =====================================================
    # STATUS
    # =====================================================

    elif intent == "STATUS":

        battery = robot_state["battery"]

        pos = robot_state["position"]

        response = (
            f"Battery at {battery} percent. "
            f"Position {pos[0]}, {pos[1]}."
        )

    # =====================================================
    # JOKES
    # =====================================================

    elif intent == "JOKE":

        response = random.choice(JOKES)

    # =====================================================
    # AI CHAT
    # =====================================================

    else:

        response = ask_ai(cmd)

    # =====================================================
    # LOGGING
    # =====================================================

    robot_state["log"].append(response)

    if len(robot_state["log"]) > 20:
        robot_state["log"].pop(0)

    # =====================================================
    # TELEMETRY
    # =====================================================

    robot_state["battery"] = max(
        5,
        robot_state["battery"] - random.randint(0, 1)
    )

    robot_state["sensors"]["front"] = random.randint(10, 120)
    robot_state["sensors"]["left"] = random.randint(10, 120)
    robot_state["sensors"]["right"] = random.randint(10, 120)

    # =====================================================
    # UI
    # =====================================================

    socketio.emit(
        "tars_response",
        {"text": response}
    )

    socketio.emit(
        "telemetry",
        robot_state
    )

    # =====================================================
    # VOICE
    # =====================================================

    threading.Thread(
        target=speak,
        args=(response,),
        daemon=True
    ).start()

# =========================================================
# START TELEMETRY
# =========================================================

threading.Thread(
    target=telemetry_loop,
    daemon=True
).start()

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("F.R.I.D.A.Y AI SYSTEM ONLINE")
    print("=" * 60)

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000
    )