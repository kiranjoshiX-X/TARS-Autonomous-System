#control.py
import random

# Robot States
IDLE = "IDLE"
ACTIVE = "ACTIVE"
LOW_POWER = "LOW_POWER"
ERROR = "ERROR"


def decide_next_state(current_state, battery_level, fault):
    """
    Decision-making logic for robot state transitions
    """

    # Debug info (helps later when system grows)
    # print(f"[DEBUG] State: {current_state}, Battery: {battery_level}, Fault: {fault}")

    # 1. Fault has highest priority
    if fault:
        return ERROR

    # 2. Battery safety
    if battery_level < 20:
        return LOW_POWER

    # 3. State transitions
    if current_state == IDLE:
        # 70% chance to become active
        return ACTIVE if random.random() > 0.3 else IDLE

    elif current_state == ACTIVE:
        # Stay active unless randomly deciding to rest
        return ACTIVE if random.random() > 0.2 else IDLE

    elif current_state == LOW_POWER:
        # Recover only if battery improves
        return IDLE if battery_level > 30 else LOW_POWER

    elif current_state == ERROR:
        # Recover if fault disappears
        return IDLE if not fault else ERROR
    
    # Fallback safety
    return IDLE

    
    
# =========================
# New Adapter Function
# =========================

current_state = IDLE  # maintain global state

def update_state(sensor_data):
    """
    Adapter for new architecture (Pi controller)
    """

    global current_state

    battery = sensor_data["battery"]
    temperature = sensor_data["temperature"]
    humidity = sensor_data["humidity"]

    # ---- Fault Logic (from your existing system) ----
    fault = False

    if temperature > 50:
        fault = True

    # ---- Environmental Overrides ----
    if humidity > 80:
        current_state = LOW_POWER
        return current_state

    # ---- Use existing state machine ----
    current_state = decide_next_state(current_state, battery, fault)

    return current_state