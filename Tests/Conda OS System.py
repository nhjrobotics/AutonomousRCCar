import os
from multiprocessing import Pool


def run_process(process):
    os.system('python {}'.format(process))


if __name__ == '__main__':
    os.system('conda activate railway_bot')

    processes = ('C:/Users/Noah/PycharmProjects/rc_car/Control/Servo_control.py',
                 'C:/Users/Noah/PycharmProjects/rc_car/Control/webcam_server.py')

    pool = Pool(processes=2)
    pool.map(run_process, processes)
