import time
from concurrent.futures import ProcessPoolExecutor

def sum(n):
    output = 1
    for i in range(1, n + 1):
        output += i
    return n, output

def main():
    start = time.time()
    with ProcessPoolExecutor() as executor:
        numbers = [100000000, 50000000]
        for n, result in executor.map(sum, numbers):
            print("Result for {0} = {1}".format(n, result))


    print("Time taken = {0:.5f}".format(time.time() - start))

if __name__ == '__main__':
    main()
