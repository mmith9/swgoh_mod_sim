# import multiprocessing

# def a_function(ret_value):
#     ret_value.value = 3.145678


# ret_value = multiprocessing.Value("d", 0.0, lock=False)

# if __name__ == '__main__':
    
#     reader_process = multiprocessing.Process(target=a_function, args=[ret_value])
#     reader_process.start()
#     reader_process.join()

# print(ret_value.value)

import random
import time
import multiprocessing


def worker(name, q):
    t = 0
    for i in range(10):
        print(name + " " + str(i))
        x = random.randint(1, 3)
        t += x
        time.sleep(x * 0.1)
    q.put(t)

if __name__ == '__main__':
    q = multiprocessing.Queue()
    jobs = []
    for i in range(10):
        p = multiprocessing.Process(target=worker, args=("process"+str(i), q))
        jobs.append(p)
        p.start()

    for p in jobs:
        p.join()

    results = [q.get() for j in jobs]
    print(results)
