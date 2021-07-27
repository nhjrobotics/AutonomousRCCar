import pygame.display
import redis


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
    print(angle_x, angle_y, angle_a, angle_b)

    return angle_x, angle_y, angle_a, angle_b


trim = 35
pygame.init()

controller = pygame.joystick.Joystick(0)
controller.init()

while True:
    axis_input()
