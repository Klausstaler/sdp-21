from collections import namedtuple

Size = namedtuple("Size", ["length", "width", "height"])


class Location:
    def __init__(self, x, y):
        self.x, self.y = x, y  # there are probably better representations
