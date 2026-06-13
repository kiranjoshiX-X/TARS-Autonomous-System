# =========================
# robot_core.py
# CENTRAL ROBOT CORE
# =========================

from core.state import robot_state
from core.movement import MovementSystem

movement = MovementSystem()

# =========================
# EXECUTE COMMAND
# =========================

def execute_command(command):

    # ---------------------
    # MOVEMENT EXECUTION
    # ---------------------

    movement.execute_command(command)

    # ---------------------
    # UPDATE ROBOT STATE
    # ---------------------

    robot_state["movement"]["current_command"] = command

    robot_state["position"]["x"] = movement.x

    robot_state["position"]["y"] = movement.y

    robot_state["position"]["direction"] = movement.direction

# =========================
# BATTERY SYSTEM
# =========================

def update_battery(value):

    robot_state["battery"] = max(
        0,
        min(100, value)
    )

# =========================
# MODE SYSTEM
# =========================

def set_mode(mode):

    robot_state["mode"] = mode

# =========================
# SENSOR UPDATE
# =========================

def update_sensors(front, left, right):

    robot_state["sensors"]["front"] = front

    robot_state["sensors"]["left"] = left

    robot_state["sensors"]["right"] = right

# =========================
# GET CURRENT STATE
# =========================

def get_robot_state():

    return robot_state