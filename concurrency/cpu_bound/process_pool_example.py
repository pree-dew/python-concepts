import time
from multiprocessing import Pool

def sum(n):
    output = 1
    for i in range(1, n + 1):
        output += i
    return output

def main():
    start = time.time()
    with Pool() as p:
        sum_5 = p.apply(sum, args=(50000000,))
        print("Sum upto 5 is: ", sum_5)

        sum_10 = p.apply(sum, args=(100000000,))
        print("Sum upto 10 is: ", sum_10)

    print("Time taken = {0:.5f}".format(time.time() - start))

if __name__ == '__main__':
    main()
