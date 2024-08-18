"""This program was created to be in conjunction with Servo_receive.

Written by Rewind2b4, with help from the internet..."""

import json
import pygame.display
import pickle
import ast
import multiprocessing
import io
import socket
import struct
from PIL import Image
import redis
import cv2
import numpy

# ----------------------------------------Functions
def scale_servo(x):
    # used to scale -1,1 to 0,179
    y = round((179/2)*(x+1))
    return y


def angle_maxmin(angle_axis):
    if angle_axis <= 0:
        angle_axis = 0

    if angle_axis >= 180:
        angle_axis = 180

    return angle_axis


def axis_input():
    angle_x = 180 - scale_servo(controller.get_axis(0)) - trim
    angle_y = 180 - scale_servo(controller.get_axis(1))
    angle_a = 180 - scale_servo(controller.get_axis(2))
    angle_b = 180 - scale_servo(controller.get_axis(3))

    angle_x = angle_maxmin(angle_x)
    angle_y = angle_maxmin(angle_y)
    angle_a = angle_maxmin(angle_a)
    angle_b = angle_maxmin(angle_b)

    return angle_x, angle_y, angle_a, angle_b


def servo_send():
    steer_angle, drive_angle, a_angle, b_angle = axis_input()
    rpi_send = {'steer_angle': steer_angle, 'drive_angle': drive_angle, 'a_angle': a_angle, 'b_angle': b_angle}
    rpi_send = json.dumps(rpi_send).encode()
    conn.send(rpi_send)
    data = conn.recv(BUFFER_SIZE)
    echo = data.decode()
    print("Servo echo:", echo)


def ultra_receive():
    pc_receive = conn.recv(BUFFER_SIZE)
    ultrasonic_decoded = pc_receive.decode()
    print("Ultrasonic data:", ultrasonic_decoded)
    return ultrasonic_decoded


def to_redis_servo(a, n):
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    p_a = pickle.dumps(a)
    r.set(n, p_a)


def control():
    while True:
        servo_send()
        ultrasonic_decoded = ultra_receive()
        ultrasonic = ast.literal_eval(ultrasonic_decoded)
        to_redis_servo(ultrasonic, 'ultrasonic')


def webcam_server():
    try:
        while True:
            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            # Construct a stream to hold the image data and read the image
            # data from the connection
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            # Rewind the stream, open it as an image with PIL and do some
            # processing on it
            image_stream.seek(0)
            image = Image.open(image_stream)
            print('Image is %dx%d' % image.size)
            image.verify()
            print('Image is verified')
            image = Image.open(image_stream)
            frame_bgr = numpy.array(image)
            frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            # Send to cache
            toRedis_webcam(frame, 'webcam')

    finally:
        connection.close()
        server_socket.close()


def toRedis_webcam(a, n):
    """Store given Numpy array 'a' in Redis under key 'n'"""
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    h, w = a.shape[:2]
    shape = struct.pack('>II',h,w)
    encoded = shape + a.tobytes()

    # Store encoded data in Redis
    r.set(n,encoded)
    return


def main():
    pool = multiprocessing.Pool()

    pool.apply_async(control)
    pool.apply_async(webcam_server)

    # wait for them to exit
    pool.close()
    pool.join()


if __name__ == "__main__":

    pygame.init()

    # Socket Setup / RC Car Connection
    trim = 35
    TCP_IP = ''
    TCP_PORT = 5005
    BUFFER_SIZE = 100 # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, address = s.accept()

    print('Connection address:', address)

    controller = pygame.joystick.Joystick(0)
    controller.init()

    # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
    # all interfaces)
    server_socket = socket.socket()
    server_socket.bind(('', 8485))
    server_socket.listen(0)

    # Accept a single connection and make a file-like object out of it
    connection = server_socket.accept()[0].makefile('rb')

    try:
        main()

    except:
        print("EXITING NOW")
        conn.close()
        controller.quit()
