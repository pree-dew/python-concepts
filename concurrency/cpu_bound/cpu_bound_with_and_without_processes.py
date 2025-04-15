import time
from multiprocessing import Process

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Execution time of {func.__name__} is {time.time() - start}")
        return result

    return wrapper

def average(n):
    total = 0
    for i in range(n):
        total += i
    return total / n

@measure_time
def without_processes():
    average(100000000)
    average(100000000)

@measure_time
def with_processes():
    p1 = Process(target=average, args=(100000000,))
    p2 = Process(target=average, args=(100000000,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

def main():
    without_processes()
    with_processes()

if __name__ == "__main__":
    main()


