import pickle
import socket
import struct
from datetime import datetime

import app as app
import cv2
from flask import Flask
from pyngrok import ngrok

is_stop = dict()

HOST = ''
PORT = 25565

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(1)


@app.route('/recode_start/<subject_name>')
def recode_start(subject_name):
    is_stop[subject_name] = False
    data = b''
    payload_size = struct.calcsize("L")
    conn, addr = s.accept()

    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    filename = datetime.today().strftime("%Y_%m_%d_%H") + "_" + subject_name + ".avi"
    out = cv2.VideoWriter("./video/" + filename, fourcc, 10, (640, 480))

    while not is_stop[subject_name]:
        while len(data) < payload_size:
            data += conn.recv(4096)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        while len(data) < msg_size:
            data += conn.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)

        out.write(frame)

    conn.close()
    cv2.destroyAllWindows()
    return "PBBS_RECODE_START/" + subject_name

@app.route('/recode_stop/<subject_name>')
def recode_stop(subject_name):
    is_stop[subject_name] = True
    return "PBBS_RECODE_STOP/" + + subject_name
