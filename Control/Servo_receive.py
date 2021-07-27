"""This program was created to be in conjunction with Servo_control_multi.

Written by Noah Jackson, with help from the internet..."""

import RPi.GPIO as GPIO
import time
import socket
import ast
import json
from adafruit_servokit import ServoKit
import argparse

# -------------------------------GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
steer = 14
drive = 15
gimbal_a = 7
gimbal_b = 11

TRIG = 6

ECHO = 13
TRIG_2 = 26
ECHO_2 = 19

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(TRIG_2, GPIO.OUT)
GPIO.setup(ECHO_2, GPIO.IN)

kit = ServoKit(channels=16)
kit.servo[steer].actuation_range = 180
kit.servo[drive].actuation_range = 180
kit.servo[gimbal_a].actuation_range = 180
kit.servo[gimbal_b].actuation_range = 180

# -----------------------------Functions


def set_servo_angle(servo, angle):
    kit.servo[servo].angle = angle


def ultrasonic_distance(trig, echo):
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    while GPIO.input(echo) == 0:
        pulse_start = time.time()
    while GPIO.input(echo) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    dist = pulse_duration * 171500
    dist = round(dist, 2)
    return dist


# -------------parses the arguments from the terminal. Used to obtain IP address
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ipaddress", required=True, help="IP Address")
args = vars(ap.parse_args())

# --------------------------------------------Control Socket Setup
TCP_IP = args['ipaddress']
TCP_PORT = 5005
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

# ------------------------------Servo Initialisation
set_servo_angle(steer, 90)
set_servo_angle(drive, 90)
time.sleep(1)

# -----------------------------------------------While loop

while True:
    try:

        # receiving servo angles from control
        data = s.recv(BUFFER_SIZE)
        if data:
            s.send(data)
            decoded = data.decode()
            print("Servo data:", decoded)
            RPI_decode = ast.literal_eval(decoded)
            steer_angle = int(RPI_decode["steer_angle"])
            drive_angle = int(RPI_decode["drive_angle"])
            gimbal_a_angle = int(RPI_decode["a_angle"])
            gimbal_b_angle = int(RPI_decode["b_angle"])
            print(drive_angle, steer_angle, gimbal_a_angle, gimbal_b_angle)

        # reading ultrasonic sensors
        front_dist = ultrasonic_distance(TRIG, ECHO)
        back_dist = ultrasonic_distance(TRIG_2, ECHO_2)

        # Check to make sure car isn't going to crash
        if front_dist <= 300 and drive_angle >= 90:
            drive_angle = 90

        if back_dist <= 300 and drive_angle <= 90:
            drive_angle = 90

        # transmitting ultrasonic data to control
        print("distance: ", front_dist, "mm & ", back_dist, "mm")
        PC_send = {'front_dist': front_dist, 'back_dist': back_dist}
        PC_send = json.dumps(PC_send).encode()
        s.send(PC_send)

        # Servo angles sent to Adafruit board
        set_servo_angle(steer, steer_angle)
        set_servo_angle(drive, drive_angle)
        set_servo_angle(gimbal_a, gimbal_a_angle)
        set_servo_angle(gimbal_b, gimbal_b_angle)


# ------------------------------------------Error handling
    except ConnectionResetError:
        print("Connection closed: Goodbye")
        break

    except Exception:
        print("error")
        set_servo_angle(steer, 55)
        set_servo_angle(drive, 90)
        break
s.close()
