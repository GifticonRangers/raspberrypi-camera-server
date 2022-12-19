import socket
import numpy
import cv2
from flask import Flask
from flask import Response
from flask import stream_with_context

UDP_IP = "127.0.0.1"
UDP_PORT = 9509

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

s = [b'\xff' * 46080 for x in range(20)]

app = Flask(__name__)
@app.route('/stream')
def stream():
    try:
        return Response(
            stream_with_context(stream_gen()),
            mimetype='multipart/x-mixed-replace; boundary=frame')

    except Exception as e:
        print('[Error] stream error: ' + str(e))

def stream_gen():
    while True:
        picture = b''
        data, addr = sock.recvfrom(46081)
        s[data[0]] = data[1:46081]

        if data[0] == 19:
            for i in range(20):
                picture += s[i]
            frame = numpy.fromstring(picture, dtype=numpy.uint8)
            frame = frame.reshape(480, 640, 3)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')