import serial
import queue
import threading
import socket
import motor
import numpy
import pid

# Constants
ESC_MAX = 2000
ESC_MIN = 800
RC_MIN = 1000
RC_MAX = 1900
DEGREES_MIN = -20
DEGREES_MAX = 20

receiver_vals = [RC_MIN, RC_MAX]
esc_vals = [ESC_MIN, ESC_MAX]
degree_vals = [DEGREES_MIN, DEGREES_MAX]

DEBUG = True

def read_arduino(rc, imu, udp):
    while True:
        value = ser.readline().decode()
        udp.put(''.join(value))

        decoded = value.rstrip().split(',')
        if decoded[0] == "CTL":
            rc.put(decoded[1:])
        if decoded[0] == "NAV":
            imu.put(decoded[1:])


def send_message(udp, sock):
    while True:
        temp = repr(udp.get())
        b = bytearray()
        b.extend(temp.encode())
        sock.sendto(b, (addr))


def regulate(value):
    value = int(value)
    if value <= ESC_MIN:
        return ESC_MIN
    if value >= ESC_MAX:
        return ESC_MAX
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
yaw_pid = pid.Control(kP=1)
roll_pid = pid.Control(1, 0.05, 0)
pitch_pid = pid.Control(1, 0.05, 0)

flight = motor.Flight(motor1, motor2, motor3, motor4, True)
print("Done initializing starting forever loop")
while True:
    # Read the queue for the RC receiver values.
    ctl = ctl_queue.get()
    # Read the queue to get the IMU values
    nav = nav_queue.get()
    # Interpolate the commanded yaw to degrees
    yaw = numpy.interp(regulate(ctl[0]), receiver_vals, degree_vals)
    # Interpolate the commanded yaw to degrees
    pitch = numpy.interp(regulate(ctl[2]), receiver_vals, degree_vals)
    # Interpolate the commanded yaw to degrees
    roll = numpy.interp(regulate(ctl[3]), receiver_vals, degree_vals)
    # Interpolate the throttle to PWM values
    throttle = numpy.interp(regulate(ctl[1]), receiver_vals, esc_vals)
    if DEBUG:
        print("IMU Values")
        print("Yaw:", nav[0], "Pitch:", nav[1], "Roll:", nav[2])
    # Get the values from the PID
    # Yaw
    yaw_pid.set_setpoint(yaw)	
    c_yaw = yaw_pid.PID(nav[0])
    # Pitch
    pitch_pid.set_setpoint(pitch)
    c_pitch = pitch_pid.PID(nav[1])
    # Roll
    roll_pid.set_setpoint(roll)
    c_roll = roll_pid.PID(nav[2])
    # Update flight parameters
    flight.set_throttle(throttle)
    flight.set_axis(c_yaw, c_roll, c_pitch)
