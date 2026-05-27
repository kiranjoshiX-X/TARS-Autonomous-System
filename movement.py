# =========================
# movement.py
# CENTRALIZED MOVEMENT SYSTEM
# =========================

import random

class MovementSystem:

    def __init__(self):

        self.current_action = "STOP"

        self.x = 0
        self.y = 0

        self.direction = "N"

        self.distance = 999

    # =========================
    # AUTONOMOUS UPDATE
    # =========================
    def update(self, robot_state, battery_level, distance):

        self.distance = distance

        if robot_state == "ERROR":

            self.current_action = "STOP"

        elif robot_state == "IDLE":

            self.current_action = "STOP"

        elif robot_state == "LOW_POWER":

            if random.random() < 0.3:

                self.current_action = random.choice([
                    "MOVE_FORWARD",
                    "TURN_LEFT",
                    "TURN_RIGHT"
                ])

            else:

                self.current_action = "STOP"

        elif robot_state == "ACTIVE":

            if self.distance < 10:

                self.current_action = "STOP"

            else:

                self.current_action = "MOVE_FORWARD"

        else:

            self.current_action = "STOP"

    # =========================
    # EXECUTE CURRENT ACTION
    # =========================
    def execute(self):

        self.execute_command(
            self.current_action
        )

    # =========================
    # CENTRAL COMMAND EXECUTOR
    # =========================
    def execute_command(self, command):

        self.current_action = command

        # ---------------------
        # MOVE FORWARD
        # ---------------------
        if command == "MOVE_FORWARD":

            if self.direction == "N":
                self.y += 1

            elif self.direction == "S":
                self.y -= 1

            elif self.direction == "E":
                self.x += 1

            elif self.direction == "W":
                self.x -= 1

        # ---------------------
        # MOVE BACKWARD
        # ---------------------
        elif command == "MOVE_BACKWARD":

            if self.direction == "N":
                self.y -= 1

            elif self.direction == "S":
                self.y += 1

            elif self.direction == "E":
                self.x -= 1

            elif self.direction == "W":
                self.x += 1

        # ---------------------
        # TURN LEFT
        # ---------------------
        elif command == "TURN_LEFT":

            self.direction = self._turn_left(
                self.direction
            )

        # ---------------------
        # TURN RIGHT
        # ---------------------
        elif command == "TURN_RIGHT":

            self.direction = self._turn_right(
                self.direction
            )

        # ---------------------
        # STOP
        # ---------------------
        elif command == "STOP":

            pass

    # =========================
    # TURN HELPERS
    # =========================
    def _turn_left(self, dir):

        return {
            "N": "W",
            "W": "S",
            "S": "E",
            "E": "N"
        }[dir]

    def _turn_right(self, dir):

        return {
            "N": "E",
            "E": "S",
            "S": "W",
            "W": "N"
        }[dir]