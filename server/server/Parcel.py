from typing import Tuple

from server.Location import Location, Size


class Parcel:
    def __init__(self, weight: float, size: Size, location: Location):
        self.location, self.weight, self.size = location, weight, size