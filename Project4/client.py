import socket

'''
This package is run on a computer to see what the values
from the receiver and IMU from the arduino
'''

UDP_IP = ''
UDP_PORT = 6879

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    decoded = data.decode().rstrip().split(',')

    if decoded[0] == "'CTL":
        decoded[4] = decoded[4][:-5]
        print("Ordered - Yaw:", decoded[1], "Pitch:", decoded[3], "Roll", decoded[4], "Throttle:", decoded[2])
    if decoded[0] == "'NAV":
        decoded[3] = decoded[3][:-5]
        print("Actual - Yaw:", decoded[1], "Pitch:", decoded[2], "Roll", decoded[3],)
sock.close()
