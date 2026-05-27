# =========================
# tars_personality (FUN + HUMAN MODE)
# =========================

import random

def tars_response(command):

    responses = {
        "MOVE_FORWARD": [
            "Alright, moving forward. Hope you know where we are going.",
            "Advancing. Confidence level: suspicious.",
            "Forward it is. What could possibly go wrong?",
        ],
        "MOVE_BACKWARD": [
            "Going back. Like your life decisions.",
            "Reversing. Strategic retreat… I hope.",
        ],
        "TURN_LEFT": [
            "Turning left. Bold move.",
            "Left turn. I will pretend that was intentional.",
        ],
        "TURN_RIGHT": [
            "Turning right. Interesting choice.",
            "Right turn. Let us see where this leads.",
        ],
        "STOP": [
            "Stopping. Crisis avoided.",
            "System halted. Finally, peace.",
        ],
        "WAKE": [
            "Ah, you're back. Let us lower expectations together.",
            "Systems awake. Chaos loading...",
        ],
        "GO_IDLE": [
            "Taking control. This might end badly.",
            "Autonomous mode activated. Good luck to us.",
        ]
    }

    if command in responses:
        return random.choice(responses[command])

    return "I have no idea what you just told me to do."