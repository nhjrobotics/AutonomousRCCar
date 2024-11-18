from machine import Pin, PWM, ADC
from time import sleep, sleep_us, ticks_us
from sys import exit

sensor_simulation = True
actuator_simulation = True

Steer_pot = ADC(26)
Drive_pot = ADC(27)
pwm_drive = PWM(Pin(0))
pwm_steer = PWM(Pin(3))
E_Stop = Pin(4, mode=Pin.IN, pull=Pin.PULL_UP) 
Reverse = Pin(5, mode=Pin.IN, pull=Pin.PULL_UP)


red_led = Pin(8, mode=Pin.OUT)
green_led = Pin(7, mode=Pin.OUT)
blue_led = Pin(6, mode=Pin.OUT) 


trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)  

pwm_drive.freq(100)
pwm_steer.freq(50)

def convert(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

while True:
    Steer_Alog = Steer_pot.read_u16()
    Drive_Alog = Drive_pot.read_u16()  
    #ultra_dist = ultra()
    print("Steer: ",Steer_Alog, " Drive: ",Drive_Alog) 

    if Reverse.value() == 0:
            reverse_drive = True
    else:
        reverse_drive = False    

    if Steer_Alog >= 300 and Steer_Alog <= 65500 :
        steer_throttle = convert(Steer_Alog, 300, 65500, 2700, 5100)
    elif Steer_Alog <= 300:
        steer_throttle = 2700
    else:
        steer_throttle = 5100
    
    if Drive_Alog >= 2000 and Drive_Alog <= 65500 :
        if reverse_drive == True:
            drive_throttle = convert(Drive_Alog, 2000, 65500, 9540, 4000)
        else:
            drive_throttle = convert(Drive_Alog, 2000, 65500, 10363, 16174)

            
    else:
        drive_throttle = 0
        

    if reverse_drive == True:
        red_led.value(0)
        green_led.value(0)
        blue_led.value(1)
    else:
        red_led.value(0)
        green_led.value(1)
        blue_led.value(0)


    if E_Stop.value() == 0:
        pwm_steer.duty_u16(3900)
        pwm_drive.duty_u16(0)
        red_led.value(1)
        green_led.value(0)
        blue_led.value(0)
        exit()
    else:
        pwm_steer.duty_u16(steer_throttle)
        pwm_drive.duty_u16(drive_throttle)

    sleep(0.001)
