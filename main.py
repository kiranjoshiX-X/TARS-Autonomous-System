# =========================
# main.py
# CLEAN CENTRAL ORCHESTRATOR
# =========================

from voice.voice import (
    listen_command,
    map_command
)

from voice.tars_voice import (
    speak,
    tars_response
)

from telemetry.logger import (
    init_log,
    log_data
)

from core.robot_core import (
    execute_command,
    update_battery,
    set_mode
)

from core.command_bus import (
    send_command,
    get_next_command,
    pending_commands
)

from core.robot_core import (
    execute_command,
    update_battery,
    set_mode
)

from core.state import robot_state

import time
import random
import datetime
import os

# =====================================================
# INIT
# =====================================================

init_log()

# =====================================================
# TERMINAL UI
# =====================================================

def clear():

    os.system("cls" if os.name == "nt" else "clear")

def banner():

    clear()

    print("\n")

    print("╔" + "═" * 58 + "╗")
    print("║{:^58}║".format("TARS CENTRAL ORCHESTRATOR"))
    print("╚" + "═" * 58 + "╝")

def status_panel():

    pos = robot_state["position"]

    print("\n┌" + "─" * 58 + "┐")

    print(
        "│ MODE      : {:<45}│".format(
            robot_state["mode"]
        )
    )

    print(
        "│ POSITION  : ({:<2}, {:<2}) {:<36}│".format(
            pos["x"],
            pos["y"],
            pos["direction"]
        )
    )

    print(
        "│ BATTERY   : {:>6.2f}% {:<38}│".format(
            robot_state["battery"],
            ""
        )
    )

    print(
        "│ FRONT     : {:>3} cm {:<38}│".format(
            robot_state["sensors"]["front"],
            ""
        )
    )

    print(
        "│ LEFT      : {:>3} cm {:<38}│".format(
            robot_state["sensors"]["left"],
            ""
        )
    )

    print(
        "│ RIGHT     : {:>3} cm {:<38}│".format(
            robot_state["sensors"]["right"],
            ""
        )
    )

    print("└" + "─" * 58 + "┘")

def divider():

    print("\n" + "═" * 60)

# =====================================================
# GREETING
# =====================================================

def get_greeting():

    hour = datetime.datetime.now().hour

    if hour < 12:
        return "Good morning."

    elif hour < 18:
        return "Good afternoon."

    return "Good evening."

# =====================================================
# STARTUP
# =====================================================

banner()

speak(
    get_greeting() +
    " Systems online. Waiting for command."
)

set_mode("WAITING")

last_command_time = time.time()

cycle = 0

# =====================================================
# MAIN LOOP
# =====================================================

while True:

    cycle += 1

    mode = robot_state["mode"]

    text = None

    # =================================================
    # WAIT MODE
    # =================================================

    if mode != "IDLE":

        divider()

        print("🎤 WAITING FOR COMMAND...\n")

        while text is None:

            text = listen_command()

            time.sleep(0.1)

        print(f"👂 INPUT DETECTED  →  {text}")

        last_command_time = time.time()

    # =================================================
    # IDLE MODE
    # =================================================

    else:

        text = listen_command()

        if text:

            print(f"\n👂 INPUT DETECTED  →  {text}")

            last_command_time = time.time()

    # =================================================
    # INTENTS
    # =================================================

    intents = map_command(text) if text else []

    action_taken = "NONE"

    # =================================================
    # COMMAND HANDLER
    # =================================================

    if intents:

        print(f"🎯 INTENTS         →  {intents}")

        for cmd in intents:

            robot_state["movement"]["last_command"] = cmd

            # -----------------------------------------
            # WAKE
            # -----------------------------------------

            if cmd == "WAKE":

                set_mode("ACTIVE")

                speak("I'm listening.")

                print("🟢 SYSTEM STATE    →  ACTIVE")

                action_taken = "WAKE"

                continue

            # -----------------------------------------
            # IDLE
            # -----------------------------------------

            elif cmd == "IDLE":

                set_mode("IDLE")

                speak(
                    "Switching to autonomous mode."
                )

                print("🟡 SYSTEM STATE    →  AUTONOMOUS")

                action_taken = "IDLE"

                continue

            # -----------------------------------------
            # NORMAL COMMANDS
            # -----------------------------------------

            print(f"📨 BUS REQUEST     →  {cmd}")

            send_command(
                source="VOICE",
                command=cmd
            )

            response = tars_response(cmd)

            print(f"🤖 TARS            →  {response}")

            speak(response)

            action_taken = cmd

    # =================================================
    # AUTO IDLE
    # =================================================

    if (
        time.time() - last_command_time > 15
        and robot_state["mode"] != "IDLE"
    ):

        set_mode("IDLE")

        print("\n😴 AUTO-IDLE ACTIVATED")

        speak(
            "No input detected. "
            "Going autonomous."
        )

    # =================================================
    # AUTONOMOUS SYSTEM
    # =================================================

    if robot_state["mode"] == "IDLE":

        cmd = random.choice([

            "MOVE_FORWARD",

            "TURN_LEFT",

            "TURN_RIGHT",

            "STOP"
        ])

        send_command(
            source="AUTONOMOUS",
            command=cmd
        )

        action_taken = cmd

        if cmd != "STOP":

            print(f"\n🤖 AUTONOMOUS      →  {cmd}")

    # =================================================
    # COMMAND BUS EXECUTION LAYER
    # =================================================

    packet = get_next_command()

    if packet:

        bus_command = packet["command"]

        bus_source = packet["source"]

        print(
            f"\n📦 COMMAND BUS     →  "
            f"{bus_command} [{bus_source}]"
        )

        execute_command(bus_command)

        action_taken = bus_command
    
    # =================================================
    # BATTERY
    # =================================================

    battery = (
        robot_state["battery"]
        - random.uniform(0.15, 0.45)
    )

    update_battery(battery)

    # =================================================
    # SENSOR SIMULATION
    # =================================================

    robot_state["sensors"]["front"] = random.randint(10, 120)

    robot_state["sensors"]["left"] = random.randint(10, 120)

    robot_state["sensors"]["right"] = random.randint(10, 120)

    robot_state["sensors"]["temperature"] = random.randint(20, 50)

    robot_state["sensors"]["humidity"] = random.randint(30, 90)

    # =================================================
    # SMART LOGGING
    # =================================================

    should_log = True

    if (
        robot_state["mode"] == "IDLE"
        and action_taken == "STOP"
    ):
        should_log = False

    if should_log:

        pos = robot_state["position"]

        log_data(

            cycle,

            robot_state["mode"],

            robot_state["battery"],

            False,

            pos["x"],

            pos["y"],

            pos["direction"],

            action_taken,

            robot_state["sensors"]["temperature"],

            robot_state["sensors"]["humidity"]
        )

    # =================================================
    # STATUS PANEL
    # =================================================

    status_panel()

    # =================================================
    # LOOP SPEED
    # =================================================

    if robot_state["mode"] == "IDLE":

        time.sleep(3)