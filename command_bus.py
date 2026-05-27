# =========================
# command_bus.py
# CENTRAL COMMAND HIGHWAY
# =========================

from queue import PriorityQueue
import time

# =========================
# PRIORITY LEVELS
# LOWER NUMBER = HIGHER PRIORITY
# =========================

PRIORITY = {
    "EMERGENCY": 0,
    "VOICE": 1,
    "AI": 2,
    "AUTONOMOUS": 3
}

# =========================
# CENTRAL COMMAND QUEUE
# =========================

command_queue = PriorityQueue()

# =========================
# SEND COMMAND
# =========================

def send_command(source, command):

    priority = PRIORITY.get(source, 5)

    packet = {
        "source": source,
        "command": command,
        "timestamp": time.time()
    }

    # Queue format:
    # (priority, timestamp, data)

    command_queue.put((
        priority,
        time.time(),
        packet
    ))

# =========================
# RECEIVE NEXT COMMAND
# =========================

def get_next_command():

    if command_queue.empty():
        return None

    _, _, packet = command_queue.get()

    return packet

# =========================
# QUEUE STATUS
# =========================

def pending_commands():

    return command_queue.qsize()