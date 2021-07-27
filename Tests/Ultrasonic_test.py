import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

TRIG = 6
ECHO = 13
TRIG_2 = 26
ECHO_2 = 19

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(TRIG_2, GPIO.OUT)
GPIO.setup(ECHO_2,GPIO.IN)



GPIO.output(TRIG, False)
GPIO.output(TRIG_2, False)

while True:

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 171500
    distance = round(distance, 2 )

    GPIO.output(TRIG_2, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_2, False)

    while GPIO.input(ECHO_2)==0:
        pulse_start_2 = time.time()
    while GPIO.input(ECHO_2)==1:
        pulse_end_2 = time.time()

    pulse_duration_2 = pulse_end_2 - pulse_start_2

    distance_2 = pulse_duration_2 * 171500
    distance_2 = round(distance_2, 2 )

    print("distance: ", distance, "mm & ", distance_2, "mm")

    time.sleep(0.1)


