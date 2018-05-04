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
        self.stop()
        time.sleep(1)
        self.pi.set_servo_pulsewidth(pin, max_value)
        time.sleep(1)
        self.pi.set_servo_pulsewidth(pin, min_value)
        time.sleep(2)
        # Start in an "off" state
        self.stop()

    def set_pwm(self, value):
        self.pi.set_servo_pulsewidth(self.pin, value)

    def stop(self):
        self.pi.set_servo_pulsewidth(self.pin, 0)

    def stopAll(self):
        self.stop()
        self.pi.stop()


class Flight:
    def __init__(self, motor1, motor2, motor3, motor4):
        self.motor1 = motor1
        self.motor2 = motor2
        self.motor3 = motor3
        self.motor4 = motor4

    def set_throttle(self, value):
        self.throttle = value

    def set_axis(self, yaw, roll, pitch):
        m1 = self.throttle + pitch + yaw
        m2 = self.throttle + roll - yaw
        m3 = self.throttle - pitch + yaw
        m4 = self.throttle - roll - yaw
        self.motor1.set_pwm(m1)
        self.motor2.set_pwm(m2)
        self.motor3.set_pwm(m3)
        self.motor4.set_pwm(m4)
