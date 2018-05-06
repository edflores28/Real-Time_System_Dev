import time


class Control:
    def __init__(self, kP=0, kI=0, kD=0):
        # PID Values
        self.kP = kP
        self.kI = kI
        self.kD = kD
        # Bookkeeping values
        self.integral = 0
        self.prev_error = 0
        self.curr_time = time.time()
        self.prev_time = self.curr_time

    def set_setpoint(self, setpoint):
        self.setpoint = float(setpoint)

    def PID(self, feedback):
        print(self.setpoint)
        # Find the error
        error = self.setpoint - float(feedback)
        # Get the current time and compute the time change
        self.curr_time = time.time()
        deltaT = self.curr_time - self.prev_time
        # Determine error change
        deltaE = error - self.prev_error
        # Determine the p term
        pTerm = self.kP * error
        # Determine the i term
        self.integral += error * deltaT
        # Determine the d term
        dTerm = 0
        if deltaT > 0:
            dTerm = deltaE / deltaT
        # Bookkeeping
        self.prev_time = self.curr_time
        self.prev_error = error
        # Return
        return pTerm + (self.kI * self.integral) + (self.kD * dTerm)
