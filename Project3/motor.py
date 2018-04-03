import time
import pigpio


class Motor:

    def __init__(self, pin, min_value, max_value):
        # Variables
        self.pin = pin
        self.pi = pigpio.pi()
        self.max_value = max_value
        self.min_value = min_value
        # Arming sequence
        self.pi.set_servo_pulsewidth(pin, max_value)
        time.sleep(1)
        self.pi.set_servo_pulsewidth(pin, min_value)
        time.sleep(1)
        # Start in an "off" state
        self.stop()

    def set_pwn(self, value):
        self.pi.set_servo_pulsewidth(self.pin, value)

    def stop(self):
        self.pi.set_servo_pulsewidth(self.pin, 0)
