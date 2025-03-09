import time

def fibonacci_without_threading(n):
    if n <= 1:
        return n
    else:
        return fibonacci_without_threading(n-1) + fibonacci_without_threading(n-2)

n1 = 35
n2 = 36

start_time = time.time()
fibonacci_without_threading(n1)
fibonacci_without_threading(n2)
print(f'Time taken: {time.time() - start_time}')

