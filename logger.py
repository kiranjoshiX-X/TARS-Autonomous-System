# =========================
# logger.py (CLEAN LOG SYSTEM)
# =========================

import csv
import time
import os

FILE_NAME = "robot_log.csv"

def init_log():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Cycle",
                "Timestamp",
                "Mode",
                "Battery",
                "Fault",
                "X",
                "Y",
                "Direction",
                "Action",
                "Temperature",
                "Humidity"
            ])

def log_data(cycle, mode, battery, fault, x, y, direction, action, temp, humidity):
    timestamp = time.strftime("%H:%M:%S")

    with open(FILE_NAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            cycle,
            timestamp,
            mode,
            round(battery, 2),
            fault,
            x,
            y,
            direction,
            action,
            temp,
            humidity
        ])