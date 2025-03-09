
import threading
import time

def fibonacci_with_threading(n):
    if n <= 1:
        return n
    else:
        return fibonacci_with_threading(n-1) + fibonacci_with_threading(n-2)

n1 = 35
n2 = 36
start_time = time.time()
thread1 = threading.Thread(target=fibonacci_with_threading, args=(n1,))
thread2 = threading.Thread(target=fibonacci_with_threading, args=(n2,))
thread1.start()
thread2.start()
thread1.join()
thread2.join()

print(f'Time taken: {time.time() - start_time}')
