# =========================
# visual_sim.py (STANDALONE CLEAN)
# =========================

import pygame
import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from voice.voice import listen_command, map_command
from voice.tars_voice import speak, tars_response

pygame.init()

# =========================
# STARTUP
# =========================
speak("Hello boss. Systems online.")

# =========================
# WINDOW
# =========================
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TARS // SIMULATION")

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 18)

# =========================
# COLORS
# =========================
BG = (5, 10, 20)
GRID = (20, 60, 100)
NEON = (0, 200, 255)
LIGHT = (180, 240, 255)
WARN = (255, 200, 0)
DANGER = (255, 60, 60)

# =========================
# ROBOT STATE
# =========================
x, y = WIDTH // 2, HEIGHT // 2
angle = 0
speed = 3

turning = False
target_angle = 0
forward_timer = 0

mode = "ACTIVE"
decision_text = "Manual control ready"

trail = []
battery = 100
idle_cooldown = 0

# =========================
# OBSTACLES
# =========================
obstacles = [
    pygame.Rect(200, 150, 120, 80),
    pygame.Rect(600, 300, 120, 80),
    pygame.Rect(400, 500, 150, 60)
]

# =========================
# SENSOR
# =========================
def cast_ray(offset=0):
    direction = pygame.math.Vector2(1, 0).rotate(-(angle + offset))

    for d in range(0, 250, 5):
        rx = x + direction.x * d
        ry = y + direction.y * d

        if rx <= 15 or rx >= WIDTH - 15 or ry <= 15 or ry >= HEIGHT - 15:
            return d

        point = pygame.Rect(rx, ry, 2, 2)

        for obs in obstacles:
            if obs.colliderect(point):
                return d

    return 250

# =========================
# TURN SYSTEM
# =========================
def update_turn():
    global angle, turning

    diff = (target_angle - angle + 180) % 360 - 180

    if abs(diff) < 3:
        angle = target_angle
        turning = False
    else:
        angle += 4 if diff > 0 else -4

# =========================
# GRID
# =========================
def draw_grid():
    for i in range(0, WIDTH, 40):
        pygame.draw.line(screen, GRID, (i, 0), (i, HEIGHT))
    for j in range(0, HEIGHT, 40):
        pygame.draw.line(screen, GRID, (0, j), (WIDTH, j))

# =========================
# MAIN LOOP
# =========================
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # =========================
    # VOICE INPUT
    # =========================
    if pygame.time.get_ticks() % 1400 < 50:
        text = listen_command()

        if text:
            text = text.lower()
            intents = map_command(text)

            # MODE SWITCH
            if "idle" in text:
                mode = "IDLE"
                speak("Autonomous mode activated.")
                decision_text = "AI control enabled"
                continue

            if "manual" in text:
                mode = "ACTIVE"
                speak("Manual control restored.")
                decision_text = "Manual control"
                continue

            # MANUAL COMMANDS
            if mode == "ACTIVE" and intents:
                cmd = intents[0]
                front = cast_ray(0)

                if cmd == "MOVE_FORWARD" and front < 60:
                    speak("That is a terrible idea.")
                    decision_text = "Blocked unsafe command"
                    continue

                speak(tars_response(cmd))
                decision_text = f"Manual → {cmd}"

                if cmd == "MOVE_FORWARD":
                    forward_timer = 20

                elif cmd == "TURN_LEFT":
                    turning = True
                    target_angle = (angle + 90) % 360

                elif cmd == "TURN_RIGHT":
                    turning = True
                    target_angle = (angle - 90) % 360

    # =========================
    # SENSOR
    # =========================
    front = cast_ray(0)
    left = cast_ray(35)
    right = cast_ray(-35)

    # =========================
    # AUTONOMOUS MODE
    # =========================
    if mode == "IDLE" and not turning and forward_timer <= 0:

        if idle_cooldown <= 0:

            if front < 60:
                turn_angle = random.randint(40, 140)

                if left > right:
                    target_angle = (angle + turn_angle) % 360
                    decision_text = f"AI → turning left {turn_angle}°"
                else:
                    target_angle = (angle - turn_angle) % 360
                    decision_text = f"AI → turning right {turn_angle}°"

                turning = True

            else:
                forward_timer = random.randint(25, 45)
                decision_text = "AI → advancing"

            idle_cooldown = random.randint(20, 40)

        else:
            idle_cooldown -= 1

    # =========================
    # MOVEMENT
    # =========================
    if turning:
        update_turn()

    elif forward_timer > 0:
        direction = pygame.math.Vector2(1, 0).rotate(-angle)

        next_x = x + direction.x * speed
        next_y = y + direction.y * speed

        # -----------------------------
        # COLLISION DETECTION
        # -----------------------------
        robot_rect = pygame.Rect(next_x - 15, next_y - 15, 30, 30)
        collided = False
        
        for obs in obstacles:
            if obs.colliderect(robot_rect):
                collided = True
                break
                
        if collided:
            forward_timer = 0
        else:
            x = next_x
            y = next_y

            x = max(20, min(WIDTH - 20, x))
            y = max(20, min(HEIGHT - 20, y))

            forward_timer -= 1

            trail.append((x, y))
            if len(trail) > 60:
                trail.pop(0)

    # =========================
    # BATTERY
    # =========================
    battery -= 0.02
    battery = max(battery, 0)

    # =========================
    # DRAW
    # =========================
    screen.fill(BG)
    draw_grid()

    for t in trail:
        pygame.draw.circle(screen, (0, 120, 255), (int(t[0]), int(t[1])), 2)

    for obs in obstacles:
        pygame.draw.rect(screen, (180, 40, 40), obs, border_radius=8)

    pygame.draw.circle(screen, NEON, (int(x), int(y)), 20)

    for ang, dist in [(0, front), (35, left), (-35, right)]:
        direction = pygame.math.Vector2(1, 0).rotate(-(angle + ang))
        ex = x + direction.x * dist
        ey = y + direction.y * dist

        color = NEON if dist > 60 else WARN if dist > 30 else DANGER
        pygame.draw.line(screen, color, (x, y), (ex, ey), 2)

    # UI PANEL
    pygame.draw.rect(screen, (10, 20, 40), (10, 10, 340, 180), border_radius=10)
    pygame.draw.rect(screen, NEON, (10, 10, 340, 180), 2, border_radius=10)

    info = [
        f"MODE: {mode}",
        f"DIST: {front}",
        f"BAT : {int(battery)}%",
        f"ANGLE: {int(angle)}"
    ]

    for i, t in enumerate(info):
        txt = font.render(t, True, LIGHT)
        screen.blit(txt, (20, 20 + i * 25))

    txt = font.render(f"AI: {decision_text}", True, NEON)
    screen.blit(txt, (20, 140))

    pygame.display.flip()
    clock.tick(60)