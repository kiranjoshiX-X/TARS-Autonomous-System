# test_core.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.robot_core import execute_command
from core.state import robot_state

commands = [

    "MOVE_FORWARD",
    "TURN_RIGHT",
    "MOVE_FORWARD",
    "TURN_LEFT",
    "MOVE_BACKWARD"
]

for cmd in commands:

    execute_command(cmd)

    print("\nCOMMAND:", cmd)

    print(robot_state["position"])