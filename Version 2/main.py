from machine import Pin, PWM, ADC
from time import sleep_us, ticks_us

trig = Pin(14, mode=Pin.OUT)
echo = Pin(15, mode=Pin.IN, pull=Pin.PULL_UP)

def read(trig_pin, echo_pin, simulation, simulation_value):
        if simulation == False:

            timepassed = 0
            signalon = 0
            signaloff = 0
            
            trig_pin.low()
            sleep_us(2)
            trig_pin.high()
            sleep_us(10)
            trig_pin.low()           
            while echo_pin.value() == 0:
                signaloff = ticks_us()
            while echo_pin.value() == 1:
                signalon = ticks_us()
            timepassed = signalon - signaloff

            distance_mm = (timepassed * 0.343) / 2
            distance_mm = round(distance_mm, 2)

            return distance_mm
                    
        else:
            return simulation_value


simulation = False
input_sim = False
output_sim = False

if simulation == True:
    input_sim = True
    output_sim = True

while True:
    ultra_reading = read(trig, echo, input_sim, 1000)
    print(ultra_reading)