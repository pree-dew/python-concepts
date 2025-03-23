class MyIterable:
    def __init__(self):
        self._items = []

    def add(self, item):
        self._items.append(item)

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)


def main():
    iterable = MyIterable()
    iterable.add(1)
    iterable.add(2)
    iterable.add(3)
    iterable.add(4)

    print("iterator", iter(iterable))
    for item in iterable:
        print(item)


if __name__ == "__main__":
    main()
