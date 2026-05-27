# =========================
# pi_controller.py
# =========================

from comms import (
    pi_receive,
    pi_send,
    create_command_packet
)

from control import update_state

import random

from robot_core import execute_command

last_command = None

turn_cooldown = 0

# =========================
# DECISION ENGINE
# =========================
def decide_command(state, sensor_data):

    global last_command
    global turn_cooldown

    distance = sensor_data["distance"]

    if state in [
        "ERROR",
        "LOW_POWER",
        "IDLE"
    ]:
        return "STOP"

    if state == "ACTIVE":

        # -----------------
        # OBSTACLE
        # -----------------

        if distance < 10:

            turn_cooldown = 3

            cmd = random.choice([
                "TURN_LEFT",
                "TURN_RIGHT"
            ])

            last_command = cmd

            return cmd

        # -----------------
        # POST TURN
        # -----------------

        if turn_cooldown > 0:

            turn_cooldown -= 1

            last_command = "MOVE_FORWARD"

            return "MOVE_FORWARD"

        # -----------------
        # DEFAULT
        # -----------------

        action = "MOVE_FORWARD"

        last_command = action

        return action

    return "STOP"

# =========================
# MAIN PI LOOP
# =========================
def run_pi_cycle():

    packet = pi_receive()

    if not packet:
        return None

    sensor_data = packet["data"]

    state = update_state(sensor_data)

    command = decide_command(
        state,
        sensor_data
    )

    # ---------------------
    # EXECUTE
    # ---------------------

    execute_command(command)

    # ---------------------
    # SEND
    # ---------------------

    command_packet = create_command_packet(
        command
    )

    pi_send(command_packet)

    return {

        "state": state,

        "command": command,

        "sensor_data": sensor_data
    }