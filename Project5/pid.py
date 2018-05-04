import time


class Control:
    def __init__(self, kP=0, kI=0, kD=0):
        # PID Values
        self.kP = kP
        self.kI = kI
        self.kD = kD
        # Bookkeeping values
        self.integral = 0
        self.previous_error = 0
        self.previous_time = 0

    def PID(self, ordered, actual):
        # Get the current time and compute the time change
        millis = int(round(time.time() * 1000))
        time_change = millis - self.previous_time
        # Get the error between ordered and actual
        error = ordered - actual
        # Compute the integral and derivative
        self.integral = self.integral + (error*time_change)
        derivative = (error - self.previous_error) / time_change
        # Book keeping
        self.previous_time = millis
        self.previous_error = error
        # Return the value
        return self.kP*error + self.kI*self.integral + self.kD*derivative
