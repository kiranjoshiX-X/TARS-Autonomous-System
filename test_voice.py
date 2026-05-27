# test_core.py

from robot_core import execute_command
from state import robot_state

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