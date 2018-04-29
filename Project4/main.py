import serial
import queue
import threading
import socket
import motor
import numpy


max_value = 2100
min_value = 700
value = 950

receiver_vals = [1000, 1900]
esc_vals = [min_value, max_value]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr =("192.168.1.213", 6879)

ser = serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate = 9600

ctl_queue = queue.Queue()
nav_queue = queue.Queue()
udp_queue = queue.Queue()


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
    if value <= min_value:
        return min_value
    if value >= max_value:
        return max_value
    return value


'''
MAIN
'''

worker = threading.Thread(target=read_arduino, args=(ctl_queue, nav_queue, udp_queue))
worker.setDaemon(True)
worker.start()

worker1 = threading.Thread(target=send_message, args=(udp_queue, sock))
worker1.setDaemon(True)
worker1.start()

motor1 = motor.Motor(4, min_value, max_value)
motor2 = motor.Motor(14, min_value, max_value)
motor3 = motor.Motor(27, min_value, max_value)
motor4 = motor.Motor(21, min_value, max_value)

motor1.set_pwm(value)
motor2.set_pwm(value)
motor3.set_pwm(value)
motor4.set_pwm(value)

while True:
    ctl = ctl_queue.get()
    yaw = numpy.interp(regulate(ctl[0]), receiver_vals, esc_vals)
    print("YAW:",yaw, ctl[0])
    throttle = numpy.interp(regulate(ctl[1]), receiver_vals, esc_vals)
    print("THR:",throttle, ctl[1])
    pitch = numpy.interp(regulate(ctl[2]), receiver_vals, esc_vals)
    print("PITCH",pitch, ctl[2])
    roll = numpy.interp(regulate(ctl[3]), receiver_vals, esc_vals)
    print("ROLL:",roll, ctl[3])
    motor1.set_pwm(int(yaw))
    motor2.set_pwm(int(throttle))
    motor3.set_pwm(int(pitch))
    motor4.set_pwm(int(roll))
