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

Also included in the design was a PWM control PiHat. This is a baord which is used to control up to 16 PWM outputs from the Raspberry Pi, which only natively supports 2, and even then requires lots of configuring that I wasn't able to do at the time. 
