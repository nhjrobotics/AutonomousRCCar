import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)
kit.servo[14].actuation_range = 180
kit.servo[15].actuation_range = 180

while True:
    kit.servo[15].angle = 110
    kit.servo[14].angle = 180
    time.sleep(1)
    kit.servo[15].angle = 0
    kit.servo[14].angle = 0
    time.sleep(1)