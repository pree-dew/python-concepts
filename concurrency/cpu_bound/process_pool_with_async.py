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
        p1 = p.apply_async(sum, args=(50000000,))
        p2 = p.apply_async(sum, args=(100000000,))
        
        print("Sum of upto 50000000 = ", p1.get())
        print("Sum of upto 100000000 = ", p2.get())

    print("Time taken = {0:.5f}".format(time.time() - start))

if __name__ == '__main__':
    main()
