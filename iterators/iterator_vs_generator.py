import sys
import tracemalloc
import time

# Task: Find all squares of numbers from 1 to n that are divisible by 3

# Approach 1: Traditional Iterator with intermediate lists
class SquareProcessor:
    def __init__(self, n):
        self.n = n
        self.index = 0
        self.filtered_squares = [i**2 for i in range(1, n + 1)]
        
    def __iter__(self):
        return self
        
    def __next__(self):
        if self.index >= len(self.filtered_squares):
            raise StopIteration
        if self.filtered_squares[self.index] % 3 == 0:
            result = self.filtered_squares[self.index]
            self.index += 1
            return result

        self.index += 1
        return self.__next__()

def square_generator(n):
    for num in range(1, n + 1):
        s = num**2
        if s % 3 == 0:
            yield s

# Memory measurement
def measure_memory_and_time(func, n):
    tracemalloc.start()
    start_time = time.time()
    
    # Process numbers
    count = 0
    for item in func(n):
        count += 1
        # Just iterate through the values
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Found {count:,} filtered squares divided by 3.")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    print(f"Peak memory usage: {peak / 1024:.2f} KB")
    tracemalloc.stop()

# Run the comparison with a moderately large number
n = 1_000_000

print("\nTRADITIONAL ITERATOR APPROACH:")
measure_memory_and_time(SquareProcessor, n)

print("\nGENERATOR APPROACH:")
measure_memory_and_time(square_generator, n)
