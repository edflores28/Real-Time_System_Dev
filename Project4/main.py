import serial
import queue
import threading
import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr =("192.168.1.213",6879)

ser = serial.Serial("/dev/ttyACM0",9600)
ser.baudrate=9600

ctl_queue = queue.Queue()
nav_queue = queue.Queue()
udp_queue = queue.Queue()

def read_arduino(rc, imu, udp):
    while True:
        value = ser.readline().decode()
        print(value) 
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
        print(sock.sendto(b, (addr)))

worker = threading.Thread(target=read_arduino,args=(ctl_queue, nav_queue, udp_queue))
worker.setDaemon(True)
worker.start()

worker1 = threading.Thread(target=send_message,args=(udp_queue,sock))
worker1.setDaemon(True)
worker1.start()

while True:
    print(ctl_queue.get())
    print(nav_queue.get())

