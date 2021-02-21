from typing import Tuple

from server.Location import Location


class Parcel:
    def __init__(self, weight: float, size: Tuple[float, float, float], location:Location):
        self.location, self.weight, self.size = location, weight, size