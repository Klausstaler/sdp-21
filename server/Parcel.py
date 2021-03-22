from server.Robot import Size
from server.Shelf import ShelfInfo


class Parcel:
    def __init__(self, weight: float, size: Size, location_id: int, shelf_info: ShelfInfo):
        self.location_id, self.weight, self.size = location_id, weight, size
        self.shelf_info = shelf_info
