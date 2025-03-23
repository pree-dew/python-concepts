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

class MyIterable:
    def __init__(self, sequence):
        self.sequence = sequence

    def __iter__(self):
        return MyIterator(self.sequence)


def main():
    iterable = MyIterable([1, 2, 3, 4, 5])
    print(iter(iterable))
    for i in iterable:
        print(i)

if __name__ == '__main__':
    main()
