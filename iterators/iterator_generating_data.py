class MyIterator():
    def __init__(self, last_index=15):
        self._last_index = last_index
        self._index = 0
        self._previous = 0
        self._current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= self._last_index:
            raise StopIteration
        self._index += 1
        return_value = self._previous
        self._previous, self._current = self._current, self._previous + self._current
        return return_value


def main():
    my_iterator = MyIterator()
    for value in my_iterator:
        print(value)


if __name__ == '__main__':
    main()
