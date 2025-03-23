def sequence_generator(sequence):
    for i in sequence:
        yield i

def main():
    sequence = [1, 2, 3, 4, 5]
    print("generator object: ", sequence_generator(sequence))
    for i in sequence_generator(sequence):
        print(i)

if __name__ == '__main__':
    main()
