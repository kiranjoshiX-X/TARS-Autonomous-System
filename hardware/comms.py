# comms.py

from queue import Queue, Empty
from core.command_bus import send_command
import time
import random
import time

# =========================
# Communication Channels
# =========================

esp_to_pi = Queue()
pi_to_esp = Queue()

# =========================
# Packet Helpers
# =========================

def create_sensor_packet(distance, temperature, humidity, battery, x, y, direction):
    return {
        "type": "SENSOR_DATA",
        "timestamp": time.time(),
        "data": {
            "distance": distance,
            "temperature": temperature,
            "humidity": humidity,
            "battery": battery,
            "x": x,
            "y": y,
            "direction": direction
        }
    }
    
def create_command_packet(command):
    return {
        "type": "COMMAND",
        "timestamp": time.time(),
        "data": {
            "command": command
        }
    }

# =========================
# ESP32 Interface
# =========================

def esp_send(packet):
    """Send data from ESP32 → Pi with delay + packet loss"""

    # 🔥 Simulate packet loss (10%)
    if random.random() < 0.1:
        return  # packet dropped

    # 🔥 Simulate delay
    time.sleep(random.uniform(0.01, 0.1))

    esp_to_pi.put(packet)


def esp_receive():
    """Receive command from Pi → ESP32 (non-blocking)"""
    try:
        return pi_to_esp.get_nowait()
    except Empty:
        return None

# =========================
# Raspberry Pi Interface
# =========================

def pi_send(packet):
    """Send command from Pi → ESP32 with delay + packet loss"""

    if random.random() < 0.1:
        return

    time.sleep(random.uniform(0.01, 0.1))

    pi_to_esp.put(packet)


def pi_receive():
    """Receive sensor data from ESP32 → Pi (non-blocking)"""
    try:
        return esp_to_pi.get_nowait()
    except Empty:
        return None

# =========================
# Debug / Monitoring
# =========================

def get_queue_sizes():
    return {
        "esp_to_pi": esp_to_pi.qsize(),
        "pi_to_esp": pi_to_esp.qsize()
    }
    
# =========================
# COMMAND BRIDGE
# =========================

def relay_pi_command(command):

    send_command(
        source="VOICE",
        command=command
    )