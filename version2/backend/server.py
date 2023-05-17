import pickle
import socket
import struct
from datetime import datetime

import cv2
from flask import Flask

is_stop = dict()

HOST = ''
PORT = 7000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(1)

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/record_start/<week>/<time>/<subject_name>')
def record_start(week, time, subject_name):
    is_stop[week + "_" + time + "_" + subject_name] = False
    data = b''
    payload_size = struct.calcsize("L")
    conn, addr = s.accept()
    print("연결 성공")

    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    filename = datetime.today().strftime("%Y_%m_%d_%H") + "_" + week + "_" + time + "_" + subject_name + ".avi"
    out = cv2.VideoWriter("./video/" + filename, fourcc, 1, (1920, 1080))
    i = 0

    while not is_stop[week + "_" + time + "_" + subject_name]:
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
        i += 1
        print(i)
        out.write(frame)

    conn.close()
    cv2.destroyAllWindows()
    # return "PBBS_RECORD_START/" + week + "_" + time + "_" + subject_name
    return "START_RECORDING"

@app.route('/record_stop/<week>/<time>/<subject_name>')
def record_stop(week, time, subject_name):
    is_stop[week + "_" + time + "_" + subject_name] = True
    return "PBBS_RECORD_STOP/" + week + "_" + time + "_" + subject_name
