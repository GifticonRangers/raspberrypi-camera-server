import cv2
import numpy as np
import socket
import sys
import pickle
import struct

# 비디오 경로 읽어오기
cap = cv2.VideoCapture("")

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('192.168.0.16', 8089))

while True:
    ret, frame = cap.read()
    data = pickle.dumps(frame)
    message_size = struct.pack("L", len(data))
    clientsocket.sendall(message_size + data)
