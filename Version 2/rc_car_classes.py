try:
    from machine import Pin, PWM, ADC
    from time import sleep_us, ticks_us
except:
    print("Pico code invalid, must run in simulation mode")


class Servo:
    def __init__(self, pwm_pin, pwm_freq, E_stop_pin, E_stop_value, simulation, *args):
        self.pwm_pin = pwm_pin
        self.pwm_freq = pwm_freq
        self.E_stop_pin = E_stop_pin
        self.E_stop_value = E_stop_value
        self.throttle_args = args

        if len(self.throttle_args) == 6: ## forward, reverse, braking zone
            self.FRBZ = True
        elif len(self.throttle_args) == 4: ## forward, reverse
            self.forward_reverse = True
        elif len(self.throttle_args) == 2: ## forward only
            self.Forward_only = True
        else:
            print("Servo invalid, enter either 6, 4 or 2 arguments")

        if simulation == False:
            self.servo = PWM(Pin(self.pwm_pin))
            self.servo.freq(self.pwm_freq)
            self.E_stop = Pin(self.E_stop_pin, mode=Pin.IN, pull=Pin.PULL_UP)
    
    def E_stop_check(self, simulation, E_stop_true): # arg True
        if simulation == False:
            if self.E_stop.value() == 0:
                self.servo.duty_u16(self.E_stop_value)
                return True
            elif E_stop_true:
                self.servo.duty_u16(self.E_stop_value)
                return True
            else:
                return False
        else:
            if E_stop_true == True:
                    return True
            else:
                    return False
                
    def Drive(self, direction, throttle_input, throttle_min, throttle_max, simulation, E_stop_simulation):
        E_stop_return = self.E_stop_check(simulation, E_stop_simulation)
        if E_stop_return == True:
            return self.E_stop_value
        else:
            if throttle_input >= throttle_min and throttle_input <= throttle_max:
                throttle_input =  throttle_input
            elif throttle_input <= throttle_min:
                throttle_input = throttle_min
            else:
                throttle_input = throttle_max

            if direction == 'Forward':
                pwm_min = self.throttle_args[0]
                pwm_max = self.throttle_args[1]
            elif direction == 'Reverse':
                pwm_min = self.throttle_args[2]
                pwm_max = self.throttle_args[3]
            else:
                pwm_min = self.throttle_args[4]
                pwm_max = self.throttle_args[5]
            
            pwm_output = (throttle_input - throttle_min) * (pwm_max - pwm_min) // (throttle_max - throttle_min) + pwm_min
            if simulation == False:
                self.servo.duty_u16(pwm_output)
                return pwm_output
            else:
                return pwm_output
            
    def Stop(self, simulation, E_stop_simulation):
        E_stop_return = self.E_stop_check(simulation, E_stop_simulation)
        if E_stop_return == True:
            return self.E_stop_value
        else:
            if simulation == False:
                self.servo.duty_u16(self.E_stop_value)
                return self.E_stop_value
            else:
                return self.E_stop_value


class Led:
    def __init__(self, pwm_freq, simulation, *args): # up to 3 led_pins (Red, Green, Blue)
        self.led_pins = args
        self.pwm_freq = pwm_freq

        if simulation == False:
            if len(self.led_pins) == 1:
                self.led = PWM(Pin(self.led_pins[0]))
                self.led.freq(self.pwm_freq)

            elif len(self.led_pins) == 3:
                self.red_led = PWM(Pin(self.led_pins[0]))
                self.green_led = PWM(Pin(self.led_pins[1]))
                self.blue_led = PWM(Pin(self.led_pins[2]))

                self.red_led.freq(self.pwm_freq)
                self.green_led.freq(self.pwm_freq)
                self.blue_led.freq(self.pwm_freq)

            else:
                print("Led invalid, enter 1 or 3 arguments")

    def Set_colour(self, simulation, *args):
        if simulation == False:
            if len(args) == 1 and len(self.led_pins) == 1:
                self.led.duty_u16(args[0])
                return args
      
            elif len(args) == 3 and len(self.led_pins) == 3:
                self.red_led.duty_u16(args[0])
                self.green_led.duty_u16(args[1])
                self.blue_led.duty_u16(args[2])
                return args
            else:
                print("Led invalid, enter 1 or 3 arguments")
                return False
        else:
            return args


class Potentiometer:
    def __init__(self, pin, min, max, simulation):
        self.pin = pin
        self.min = min
        self.max = max

        if simulation == False:
            self.pot = ADC(pin)       
        
    def read(self, simulation, simulation_value):
        if simulation == False:
            pot_reading = self.pot.read_u16()

            if pot_reading >= self.min and pot_reading <= self.max:
                return pot_reading
            elif pot_reading <= self.min:
                pot_reading = self.min
                return pot_reading
            else:
                pot_reading = self.max
                return pot_reading
        else:
            return simulation_value


class Ultrasonic:
    def __init__(self, trig_pin, echo_pin, simulation):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin

        if simulation == False:
            self.trig = Pin(self.trig_pin, mode=Pin.OUT)
            self.echo = Pin(self.echo_pin, mode=Pin.IN)

    def read(self, simulation, simulation_value):
        if simulation == False:

            timepassed = 0
            signalon = 0
            signaloff = 0
            
            self.trig.low()
            sleep_us(2)
            self.trig.high()
            sleep_us(10)
            self.trig.low()           
            while self.echo.value() == 0:
                signaloff = ticks_us()
            while self.echo.value() == 1:
                signalon = ticks_us()
            timepassed = signalon - signaloff

            distance_mm = (timepassed * 0.343) / 2
            distance_mm = round(distance_mm, 2)

            return distance_mm
                    
        else:
            return simulation_value