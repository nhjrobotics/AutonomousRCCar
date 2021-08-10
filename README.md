# Introduction

The ultimate goal of this project is to explore the ways that autonomous vehicles can traverse rough terrain, requiring extra computation to work out the most appropriate path to take. To do this, I will create a fully autonomous rc car using a Raspberry Pi linked to a PC based computer vision algorithm. I believe that this is the best solution becuase it allows the immense processing power required by AI systems to be offloaded onto a more powerful PC, while the Raspberry Pi can focus on real time awareness and crash prevention using more primative sensors such as ultrasonic sensors and potentially GPS.

Currently this project is still in the early stages. I took an old radio controlled car from my childhood, and fitted it out with a Raspberry Pi, power systems, ultrasonic sensors, and a camera system with pan and tilt control. Then I used python to implement remote control of the vehicle over wifi, using a Playstation controller as the input device. I also got the video signal from the pi to be streamed back to the host PC, so I am able to drive the car out of my line of sight. 

I plan to keep working on this project once I finish yr12, hopefully implementing automation sometime in the future. 

# Timeline

I started out by investigating potential solutions using LEGO technic. I decided to use this because I have a lot of experience in creating LEGO structures, and because it allows for rapid prototyping without the use of specialised equipment such as a 3D printer. I used LEGO Mindstorms and an Arduino to build in some primitive automation. I struggled to get the LEGO motors to work properly due to the proprietary design of the system.

![alt text](https://github.com/Rewind2B4/raspberry_pi_rc_car/blob/master/Photos/Lego/IMG_3541.JPG "LEGO technic")
![alt text](https://github.com/Rewind2B4/raspberry_pi_rc_car/blob/master/Photos/Lego/60915021328__D29A656D-DBFE-4A1C-A47E-D4608F7D8852.JPG "LEGO Mindstorms + Arduino")

While this did end up working. It was an incredibly tedious process to get working, and the automation options were limited. The next phase of the project involved using an RC car that I had lying around as the basis for an autonomous car platform. I experimented with using an Arduino to provide the correct PWM output to the ESC that powers the motor driving the wheels, and the servo controlling the steering. The problem with the use of an arduino is that it has very limited processing power, especially for the types of operations that it would need to perform. Due to this limitation, I moved onto using a Raspberry Pi to control the vehicle. 

![alt text](https://github.com/Rewind2B4/raspberry_pi_rc_car/blob/master/Photos/Motor%20testing/IMG_4055.JPG "RC Car + Raspberry Pi")

Also included in the design was a PWM control PiHat. This is a baord which is used to control up to 16 PWM outputs from the Raspberry Pi, which only natively supports 2, and even then requires lots of configuring that I wasn't able to do at the time. With some trial and error with the programming, I was able to get the Raspberry Pi to control the motors. 

The next stage of the project was to implement a control system that could operate the car in real time and provide video feedback so I could control the car from any location. I used PyGame to access the control surfaces of a PS4 controller so I was able to use that to drive the car. To do this, I used a network connection with the Pi and the python library socket to send signals to the car wirelessly from the PS4 controller. This was quite complex, and involved having to pair the two devices together every time I wanted to start the program. Hopefully in the future I can get this process to work a bit better. 

![alt text](https://github.com/Rewind2B4/raspberry_pi_rc_car/blob/78aebbf07dedb1c6a64e2b46f53298a3acfa05a6/Photos/Driving/IMG_4061.JPG "RC Car driving")

While all this was happening, I worked on installing ultrasonic sensors on the vehicle. These, like with parking sensors in real cars, act to protect the vehicle from accidently running into objects. This is especially important for autonomous vehicles as it gives them a second set of "eyes" that are able to view the world around the car. This, in combination with an advanced computer vision system, allows the RC car to be able to drive it self around and work out where to go. To get the 5V ultasonic sensors to work with the 3.3V Raspberry Pi GPIO I had to incorporate a voltage divider circuit into the leads that are run to the front and back of the vehicle to power the sensors. 

![alt text](https://github.com/Rewind2B4/raspberry_pi_rc_car/blob/master/Photos/Sensor%20testing/62520187954__BD491C7E-84AC-4A95-9669-4C41C5F97B2F.JPG "Breadboard testing")

The other part of the sensor suite, the camera mast, then had to be built so the Raspberry Pi camera is able to pan and tilt so that the operator (and later the AI) can see what is happening around the vehicle. I found a 3D printed mount for small hobby servos that could hold the Raspberry Pi camera, and then mounted this system on the back of the RC car. This was controlled by the PS4 controller.

![alt text](https://github.com/Rewind2B4/raspberry_pi_rc_car/blob/master/Photos/Camera%20mast/IMG_4192.JPG "Camera Mast")

Putting all of this together, currently the vehicle can drive around being controlled by a laptop with a PS4 controller. If the car is less than 300mm from an object, and travelling towards the object, the car will stop and won't let the user crash it. The user can also currently use the camera mast to gain a sense of the car's surroundings and can control it accordingly.

I haven't yet started working on the autonomous side of the system, but I should be able to get to work on it after I have completed yr12. 

There were many issues that I encountered when building the vehicle, battery life being a big one. At the time of writing I have bought the parts to build a voltmeter which will be able to measure the battery life of the car. This will allow the vehicle to shut off when it runs out of power, preventing the Lipo batteries from being damaged due to overdischarging the vehicle. 

**Noah Jackson 10/08/21**

![alt text](https://github.com/Rewind2B4/raspberry_pi_rc_car/blob/master/Photos/Driving/P8100011.JPG "RC Car")
