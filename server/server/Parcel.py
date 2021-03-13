from server.Location import Location
from server.Robot import Size
from server.Shelf import ShelfInfo


class Parcel:
    def __init__(self, weight: float, size: Size, location: Location, shelf_info: ShelfInfo):
        self.location, self.weight, self.size = location, weight, size
        self.shelf_info = shelf_info
