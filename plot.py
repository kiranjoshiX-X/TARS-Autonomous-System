# =========================
# plot.py
# CINEMATIC TELEMETRY SYSTEM
# =========================

import csv
import matplotlib.pyplot as plt

# =========================
# DATA
# =========================

cycles = []
battery = []
x_pos = []
y_pos = []
actions = []

# =========================
# READ LOG
# =========================

with open("robot_log.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        try:

            cycles.append(int(row["Cycle"]))

            battery.append(float(row["Battery"]))

            x_pos.append(int(row["X"]))

            y_pos.append(int(row["Y"]))

            actions.append(row["Action"])

        except:
            continue

# =========================
# GLOBAL STYLE
# =========================

plt.style.use("dark_background")

# =====================================================
# BATTERY GRAPH
# =====================================================

fig1 = plt.figure(figsize=(10, 5))

plt.plot(
    cycles,
    battery,
    linewidth=3,
    marker='o',
    markersize=5
)

plt.xlabel("Cycle", fontsize=12)
plt.ylabel("Battery (%)", fontsize=12)

plt.title(
    "TARS POWER SYSTEM TELEMETRY",
    fontsize=16,
    fontweight='bold'
)

plt.grid(alpha=0.3)

# =====================================================
# PATH VISUALIZATION
# =====================================================

fig2 = plt.figure(figsize=(8, 8))

for i in range(len(x_pos) - 1):

    dx = x_pos[i+1] - x_pos[i]

    dy = y_pos[i+1] - y_pos[i]

    action = actions[i]

    # ---------------------------------------------
    # COLOR SYSTEM
    # ---------------------------------------------

    if action == "STOP":

        color = "red"

    elif "TURN" in action:

        color = "orange"

    elif "MOVE" in action:

        color = "lime"

    else:

        color = "gray"

    # ---------------------------------------------
    # DRAW PATH
    # ---------------------------------------------

    plt.arrow(

        x_pos[i],
        y_pos[i],

        dx,
        dy,

        head_width=0.15,

        length_includes_head=True,

        linewidth=2,

        color=color,

        alpha=0.9
    )

# =====================================================
# POINTS
# =====================================================

plt.scatter(

    x_pos,
    y_pos,

    s=80
)

# =====================================================
# START / END
# =====================================================

plt.text(

    x_pos[0],
    y_pos[0],

    "START",

    fontsize=12,
    fontweight='bold'
)

plt.text(

    x_pos[-1],
    y_pos[-1],

    "END",

    fontsize=12,
    fontweight='bold'
)

# =====================================================
# LABELS
# =====================================================

plt.xlabel("X Position", fontsize=12)

plt.ylabel("Y Position", fontsize=12)

plt.title(

    "TARS MOVEMENT TRAJECTORY",

    fontsize=16,

    fontweight='bold'
)

plt.grid(alpha=0.3)

plt.axis('equal')

# =====================================================
# SHOW
# =====================================================

plt.show()