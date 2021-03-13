from typing import Union, NamedTuple
from server.routing.containers import Node


class Shelf:
    def __init__(self, compartment_size: float, num_compartments, location_id: int):
        self.compartment_size = compartment_size
        self.num_compartments = num_compartments
        self.location_id = location_id

    def get_compartment_height(self, compartment_number: int):
        """
        :param compartment_number: Compartment number of shelf. Starts at 0 at the bottom
        :return:
        """
        assert compartment_number <= self.num_compartments
        return compartment_number * self.compartment_size  # for now we assume we can simply multiply compartment number with size


class ShelfInfo(NamedTuple):
    assigned_shelf: Union[None, Shelf]
    compartment_number: Union[None, int]
