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
        value = self.max_value if value > self.max_value else value
        value = self.min_value if value < self.min_value else value
        self.pi.set_servo_pulsewidth(self.pin, value)

    def stop(self):
        self.pi.set_servo_pulsewidth(self.pin, 0)

    def stopAll(self):
        self.stop()
        self.pi.stop()


class Flight:
    def __init__(self, motor1, motor2, motor3, motor4, debug):
        self.motor1 = motor1
        self.motor2 = motor2
        self.motor3 = motor3
        self.motor4 = motor4
        self.debug = debug
		
    def set_throttle(self, value):
        self.m1 = value
        self.m2 = value
        self.m3 = value
        self.m4 = value

    def set_axis(self, yaw, roll, pitch):
        # DEBUG
        if self.debug:
            print("PID outputs")
            print("Yaw:", yaw, "Roll", roll, "Pitch", pitch)
            print("Throttle:", self.m1)
        # Apply pitch
        self.m1 += pitch if pitch > 0.0 else 0.0
        self.m2 += pitch if pitch > 0.0 else 0.0
        self.m3 -= pitch if pitch < 0.0 else 0.0
        self.m4 -= pitch if pitch < 0.0 else 0.0
        # Apply roll
        self.m1 -= roll if roll < 0.0 else 0.0
        self.m2 += roll if roll > 0.0 else 0.0
        self.m3 -= roll if roll < 0.0 else 0.0
        self.m4 += roll if roll > 0.0 else 0.0		
        # DEBUG
        if self.debug:
            print("PWM Values")
            print("M1:", self.m1, "M2:", self.m2, "M3:", self.m3, "M4:", self.m4)
        # Update PWM
        self.motor1.set_pwm(self.m1)
        self.motor2.set_pwm(self.m2)
        self.motor3.set_pwm(self.m3)
        self.motor4.set_pwm(self.m4)
