import serial
import queue
import threading
import socket
import motor
import numpy
import pid
import time
from pid_controller.pid import PID


# Constants
ESC_MAX = 2000
ESC_MIN = 800
RC_MIN = 1000
RC_MAX = 1900

DEGREES_MIN = -20
DEGREES_MAX = 20

throttle_rc_vals = [997, 1976]
RC_MIN = throttle_rc_vals[0]
RC_MAX = throttle_rc_vals[1]
roll_rc_vals = [989, 1969]
pitch_rc_vals = throttle_rc_vals
yaw_rc_vals = [988, 1973]

esc_vals = [ESC_MIN, ESC_MAX]
degree_vals = [DEGREES_MIN, DEGREES_MAX]

DEBUG = True

kp = 2.5
ki = 0.25
kd = 0

def read_arduino(rc, imu, udp):
    while True:
        value = ser.readline().decode()
        udp.put(''.join(value))

        decoded = value.rstrip().split(',')
        if decoded[0] == "CTL":
            rc.put([float(i) for i in decoded[1:]])
        if decoded[0] == "NAV":
            imu.put([float(i) for i in decoded[1:]])


def send_message(udp, sock):
    while True:
        temp = repr(udp.get())
        b = bytearray()
        b.extend(temp.encode())
        sock.sendto(b, (addr))


def regulate(value, minmax):
    value = int(value)
    if value <= minmax[0]:
        return minmax[0]
    if value >= minmax[1]:
        return minmax[1]
    return value

'''
MAIN
'''
# Create the socket for UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ("192.168.1.213", 6879)

# Open the serial device
ser = serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate = 9600

# Create a queue for each functionality
ctl_queue = queue.Queue()
nav_queue = queue.Queue()
udp_queue = queue.Queue()

# Create and launch the reading arduino thread
worker = threading.Thread(target=read_arduino, args=(ctl_queue, nav_queue, udp_queue))
worker.setDaemon(True)
worker.start()

# Create and launch the UDP thread
worker1 = threading.Thread(target=send_message, args=(udp_queue, sock))
worker1.setDaemon(True)
worker1.start()

# Initialize the motors
motor1 = motor.Motor(4, ESC_MIN, ESC_MAX)
motor2 = motor.Motor(14, ESC_MIN, ESC_MAX)
motor3 = motor.Motor(27, ESC_MIN, ESC_MAX)
motor4 = motor.Motor(21, ESC_MIN, ESC_MAX)

# Initialize the PIDs
rpid = PID(p=kp, i=ki, d=kd)
ppid = PID(p=kp, i=ki, d=kd)
ypid = PID(p=3, i=0.02, d=0)

flight = motor.Flight(motor1, motor2, motor3, motor4, DEBUG)

print("Done initializing starting forever loop")
while True:
    time.sleep(0.005)
    # Read the queue for the RC receiver values.
    ctl = ctl_queue.get()
    # Read the queue to get the IMU values
    nav = nav_queue.get()
    # Interpolate the commanded yaw to degrees
    yaw = numpy.interp(regulate(ctl[0], yaw_rc_vals), yaw_rc_vals, degree_vals)
    # Interpolate the commanded yaw to degrees
    pitch = numpy.interp(regulate(ctl[2], pitch_rc_vals), pitch_rc_vals, degree_vals)
    # Interpolate the commanded yaw to degrees
    roll = numpy.interp(regulate(ctl[3], roll_rc_vals), roll_rc_vals, degree_vals)
    # Interpolate the throttle to PWM values
    throttle = numpy.interp(regulate(ctl[1], throttle_rc_vals), throttle_rc_vals, esc_vals)
    # Print
    if DEBUG:
        print("IMU Values")
        print("Yaw:", nav[0], "Pitch:", nav[1], "Roll:", nav[2],"\n")
        print("CTL Values")
        print("Yaw:", yaw, "Pitch:", pitch, "Roll:", roll, "Throttle: ", ctl[1], "\n")
	# Set the target value
    rpid.target = roll
    ppid.target = pitch
    ypid.target = yaw
    # Update flight parameters
    flight.set_throttle(ctl[1])
    rollp = rpid(nav[2])
    pitchp = ppid(nav[1])
    yawp = ypid(nav[0])
	# Send the ESC
    flight.set_axis(yawp, rollp, pitchp)
