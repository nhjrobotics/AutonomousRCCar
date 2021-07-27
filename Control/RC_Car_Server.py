"""Opens all the server programs so they are able to communicate with the client programs
and each other"""

import subprocess
from multiprocessing import Pool
import socket



def run_process(process):
    subprocess.call(['python', '{}'.format(process)], shell=True)


if __name__ == '__main__':
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print("Your Computer IP Address is: " + IPAddr)
    print("Use this IP to connect rc car")

    subprocess.call(['conda', 'activate', 'railway_bot'], shell=True)

    processes = ('C:/Users/Noah/PycharmProjects/rc_car/Control/Servo_control.py',
                 'C:/Users/Noah/PycharmProjects/rc_car/Control/webcam_server.py')

    pool = Pool(processes=2)
    pool.map(run_process, processes)
