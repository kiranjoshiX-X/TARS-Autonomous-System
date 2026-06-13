#sensors.py
import random

class SensorSystem:
    def __init__(self):
        self.distance = 100
        self.temperature = 25
        self.humidity = 50

    def update(self):
        # Distance (cm)
        self.distance = random.randint(5, 40)

        # Temperature (°C)
        self.temperature = random.randint(20, 50)

        # Humidity (%)
        self.humidity = random.randint(30, 90)

    def get_distance(self):
        return self.distance

    def is_obstacle_close(self, threshold=20):
        return self.distance <= threshold

    def get_environment(self):
        return self.temperature, self.humidity