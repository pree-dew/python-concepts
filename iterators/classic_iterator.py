import dis

class MyIterator():
    def __init__(self, sequence):
        self._sequence = sequence
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._sequence):
            raise StopIteration
        value = self._sequence[self._index]
        self._index += 1
        return value


def main():
    my_iterator = MyIterator([1, 2, 3, 4, 5])
    for value in my_iterator:
        print(value)


if __name__ == '__main__':
    dis.dis(main)
    main()
