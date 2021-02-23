from server.Location import Location


class Shelf:
    def __init__(self, compartment_size: float, num_compartments, location: Location):
        self.compartment_size = compartment_size
        self.num_compartments = num_compartments
        self.location = location
        self.compartments = [None for _ in range(num_compartments)]

    def get_compartment_height(self, compartment_number: int):
        """
        :param compartment_number: Compartment number of shelf. Starts at 0 at the bottom
        :return:
        """
        return compartment_number*self.compartment_size # for now we assume we can simply multiply compartment number with size