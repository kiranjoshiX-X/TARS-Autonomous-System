# =========================
# state.py
# CENTRALIZED ROBOT STATE
# =========================

robot_state = {

    # =====================
    # SYSTEM
    # =====================

    "mode": "IDLE",
    "status": "ONLINE",

    # =====================
    # POWER
    # =====================

    "battery": 100,

    # =====================
    # POSITION
    # =====================

    "position": {
        "x": 0,
        "y": 0,
        "direction": "N"
    },

    # =====================
    # MOVEMENT
    # =====================

    "movement": {
        "current_command": "STOP",
        "last_command": None
    },

    # =====================
    # SENSOR DATA
    # =====================

    "sensors": {
        "front": 0,
        "left": 0,
        "right": 0,
        "temperature": 0,
        "humidity": 0
    },

    # =====================
    # AI
    # =====================

    "ai": {
        "last_response": ""
    },

    # =====================
    # TELEMETRY
    # =====================

    "telemetry": {
        "cycle": 0,
        "uptime": 0
    },

    # =====================
    # LOGS
    # =====================

    "log": []
}