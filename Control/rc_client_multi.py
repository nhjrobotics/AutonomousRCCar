"""This program was created to be in conjunction with Servo_control_multi.

Written by Rewind2b4, with help from the internet..."""

import RPi.GPIO as GPIO
import ast
import json
from adafruit_servokit import ServoKit
import io
import socket
import struct
import time
import picamera
import multiprocessing


# -----------------------------Functions


def set_servo_angle(servo, angle):
    kit.servo[servo].angle = angle


class Ultrasonic:
    def __init__(self, trig, echo):
        self.trig = trig
        self.echo = echo

    def read(self):
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        while GPIO.input(self.echo) == 0:
            pulse_start = time.time()
        while GPIO.input(self.echo) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        dist = pulse_duration * 171500
        dist = round(dist, 2)

        if dist >= 4000:
            dist = 4000

        return dist


class SplitFrames(object):
    def __init__(self, connection):
        self.connection = connection
        self.stream = io.BytesIO()
        self.count = 0

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # Start of new frame; send the old one's length
            # then the data
            size = self.stream.tell()
            if size > 0:
                self.connection.write(struct.pack('<L', size))
                self.connection.flush()
                self.stream.seek(0)
                self.connection.write(self.stream.read(size))
                self.count += 1
                self.stream.seek(0)
        self.stream.write(buf)


def control_client():
    front_ultra = Ultrasonic(TRIG, ECHO)
    back_ultra = Ultrasonic(TRIG_2, ECHO_2)
    while True:
        try:
            # receiving servo angles from control
            data = s.recv(BUFFER_SIZE)
            if data:
                s.send(data)
                decoded = data.decode()
                print("Servo data:", decoded)
                rpi_decode = ast.literal_eval(decoded)
                steer_angle = int(rpi_decode["steer_angle"])
                drive_angle = int(rpi_decode["drive_angle"])
                gimbal_a_angle = int(rpi_decode["a_angle"])
                gimbal_b_angle = int(rpi_decode["b_angle"])
                print(drive_angle, steer_angle, gimbal_a_angle, gimbal_b_angle)

            # reading ultrasonic sensors

            front_dist = front_ultra.read()
            back_dist = back_ultra.read()

            # Check to make sure car isn't going to crash
            if front_dist <= 300 and drive_angle >= 90:
                drive_angle = 90

            if back_dist <= 300 and drive_angle <= 90:
                drive_angle = 90

            # transmitting ultrasonic data to control
            print("distance: ", front_dist, "mm & ", back_dist, "mm")
            pc_send = {'front_dist': front_dist, 'back_dist': back_dist}
            pc_send = json.dumps(pc_send).encode()
            s.send(pc_send)

            # Servo angles sent to Adafruit board
            set_servo_angle(steer, steer_angle)
            set_servo_angle(drive, drive_angle)
            set_servo_angle(gimbal_a, gimbal_a_angle)
            set_servo_angle(gimbal_b, gimbal_b_angle)

        # ------------------------------------------Error handling
        except ConnectionResetError:
            print("Connection closed: Goodbye")
            break

    s.close()


def webcam_client():
    try:
        output = SplitFrames(connection)
        with picamera.PiCamera(resolution='VGA', framerate=30) as camera:
            time.sleep(2)
            start = time.time()
            camera.start_recording(output, format='mjpeg')
            camera.wait_recording(1000000)
            camera.stop_recording()
            # Write the terminating 0-length to the connection to let the
            # server know we're done
            connection.write(struct.pack('<L', 0))
    finally:
        connection.close()
        client_socket.close()
        finish = time.time()
    print('Sent %d images in %d seconds at %.2ffps' % (
        output.count, finish-start, output.count / (finish-start)))


def main():
    pool = multiprocessing.Pool()

    pool.apply_async(webcam_client)
    pool.apply_async(control_client)

    # wait for them to exit
    pool.close()
    pool.join()


if __name__ == '__main__':
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

    # -------------Arguments from the terminal. Used to obtain IP address
    IP = str(input("IP Address: "))

    # -------------------------------------------Control Socket Setup
    TCP_PORT = 5005
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, TCP_PORT))

    # --------------------------------------------Webcam Socket
    client_socket = socket.socket()
    client_socket.connect((IP, 8485))
    connection = client_socket.makefile('wb')

    # ------------------------------Servo Initialisation
    set_servo_angle(steer, 90)
    set_servo_angle(drive, 90)
    time.sleep(1)

    main()
