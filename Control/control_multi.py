"""This program was created to be in conjunction with Servo_receive.

Written by Noah Jackson, with help from the internet..."""

import json
import socket
import pygame.display
import asyncio
import pickle
import redis
import ast


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
    servo_send()
    ultrasonic_decoded = ultra_receive()
    ultrasonic = ast.literal_eval(ultrasonic_decoded)
    to_redis_servo(ultrasonic, 'ultrasonic')


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

    try:
        while True:
            control()

    except:
        print("EXITING NOW")
        conn.close()
        controller.quit()


