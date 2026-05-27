# =========================
# esp32_controller.py
# =========================

from sensors import SensorSystem

from comms import (
    esp_send,
    esp_receive,
    create_sensor_packet
)

from robot_core import (
    execute_command,
    update_sensors
)

from state import robot_state

sensors = SensorSystem()

# =========================
# MAIN LOOP
# =========================
def run_esp32_cycle(battery):

    # ---------------------
    # SENSOR UPDATE
    # ---------------------

    sensors.update()

    distance = sensors.get_distance()

    temperature, humidity = (
        sensors.get_environment()
    )

    # ---------------------
    # UPDATE CENTRAL STATE
    # ---------------------

    update_sensors(
        distance,
        distance,
        distance
    )

    robot_state["sensors"]["temperature"] = temperature

    robot_state["sensors"]["humidity"] = humidity

    # ---------------------
    # CREATE SENSOR PACKET
    # ---------------------

    packet = create_sensor_packet(

        distance,
        temperature,
        humidity,

        battery,

        robot_state["position"]["x"],
        robot_state["position"]["y"],
        robot_state["position"]["direction"]
    )

    esp_send(packet)

    # ---------------------
    # RECEIVE COMMAND
    # ---------------------

    command_packet = esp_receive()

    if command_packet:

        command = (
            command_packet["data"]["command"]
        )

        execute_command(command)

    else:

        execute_command("STOP")

    # ---------------------
    # RETURN DATA
    # ---------------------

    return {

        "distance": distance,

        "temperature": temperature,

        "humidity": humidity,

        "x": robot_state["position"]["x"],

        "y": robot_state["position"]["y"],

        "direction": robot_state["position"]["direction"],

        "action": robot_state["movement"]["current_command"]
    }