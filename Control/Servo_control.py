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
async def scale_servo(x):
    # used to scale -1,1 to 0,179
    y = round((179/2)*(x+1))
    return y


async def angle_maxmin(angle_axis):
    if angle_axis <= 0:
        angle_axis = 0

    if angle_axis >= 180:
        angle_axis = 180

    return angle_axis


async def axis_input():
    angle_x = 180 - await scale_servo(controller.get_axis(0)) - trim
    angle_y = 180 - await scale_servo(controller.get_axis(1))
    angle_a = 180 - await scale_servo(controller.get_axis(2))
    angle_b = 180 - await scale_servo(controller.get_axis(3))

    angle_x = await angle_maxmin(angle_x)
    angle_y = await angle_maxmin(angle_y)
    angle_a = await angle_maxmin(angle_a)
    angle_b = await angle_maxmin(angle_b)

    return angle_x, angle_y, angle_a, angle_b


async def button_input():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.JOYBUTTONDOWN:
            if controller.get_button(0):
                print("Square Pressed")
                global trim
                trim = trim - 1
            elif controller.get_button(1):
                print("X Pressed")
            elif controller.get_button(2):
                print("Circle Pressed")
                trim = trim + 1
            elif controller.get_button(3):
                print("Triangle Pressed")
            elif controller.get_button(4):
                print("L1 Pressed")
            elif controller.get_button(5):
                print("R1 Pressed")
            elif controller.get_button(6):
                print("L2 Pressed")
            elif controller.get_button(7):
                print("R2 Pressed")
            elif controller.get_button(8):
                print("SHARE Pressed")
            elif controller.get_button(9):
                print("OPTIONS Pressed")
            elif controller.get_button(10):
                print("Left Analog Pressed")
            elif controller.get_button(11):
                print("Right Analog Pressed")
            elif controller.get_button(12):
                print("Power Button Pressed")
            elif controller.get_button(13):
                print("Pad")

        elif event.type == pygame.JOYBUTTONUP:
            print("Button Released")

        else:
            break


async def servo_send():
    steer_angle, drive_angle, a_angle, b_angle = await axis_input()
    rpi_send = {'steer_angle': steer_angle, 'drive_angle': drive_angle, 'a_angle': a_angle, 'b_angle': b_angle}
    rpi_send = json.dumps(rpi_send).encode()
    conn.send(rpi_send)
    data = conn.recv(BUFFER_SIZE)
    echo = data.decode()
    print("Servo echo:", echo)


async def ultra_receive():
    pc_receive = conn.recv(BUFFER_SIZE)
    ultrasonic_decoded = pc_receive.decode()
    print("Ultrasonic data:", ultrasonic_decoded)
    return ultrasonic_decoded


async def to_redis_servo(a, n):
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    p_a = pickle.dumps(a)
    r.set(n, p_a)


async def control():
    await button_input()
    await servo_send()
    ultrasonic_decoded = await ultra_receive()
    ultrasonic = ast.literal_eval(ultrasonic_decoded)
    await to_redis_servo(ultrasonic, 'ultrasonic')


async def main():
    await asyncio.gather(control())

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
            asyncio.run(main())

    except:
        print("EXITING NOW")
        conn.close()
        controller.quit()
