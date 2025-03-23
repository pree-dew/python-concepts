class MyIterator():
    def __init__(self, sequence):
        self._sequence = sequence
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._sequence):
            raise StopIteration
        value = f"Hello {self._sequence[self._index]}"
        self._index += 1
        return value


def main():
    my_iterator = MyIterator(["sam", "riya", "james", "john", "mike", "sara"])
    for value in my_iterator:
        print(value)


if __name__ == '__main__':
    main()
