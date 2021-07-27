import multiprocessing
import time

def test_1():
    while True:
        start_time = time.time()
        print("test 1 start at", start_time)
        time.sleep(3)
        finish_time = time.time()
        print("test 1 finishes at", finish_time)


def test_2():
    while True:
        start_time = time.time()
        print("test 2 start at", start_time)
        time.sleep(3)
        finish_time = time.time()
        print("test 2 finishes at", finish_time)

def main():
    pool = multiprocessing.Pool()

    pool.apply_async(test_1)
    pool.apply_async(test_2)

    # wait for them to exit
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
