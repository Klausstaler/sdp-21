from server.Location import Size


class Robot:
    def __init__(self, robot_id, size: Size):
        self.id = robot_id
        self.size = size

    def calculate_raise(self, height: float) -> float:
        """
        Calculates how much the platform needs to be raised in order for it to be at a
        specified height
        :param height: Height of the robot
        :return: The height needed to raise the platform to the appropriate level
        """
        return height - self.size.height
