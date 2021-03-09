from server.Location import Size
from server.routing.containers import Node

class Robot:
    def __init__(self, robot_id: str, size: Size, curr_pos: Node):
        self.curr_pos = curr_pos
        self.id = robot_id
        self.size = size

    def calculate_raise(self, height: float) -> float:
        """
        Calculates how much the platform needs to be raised in order for it to be at a
        specified height
        :param height: Height of the robot
        :return: The height needed to raise the platform to the appropriate level
        """
        #EPSILON = 0.02 # we want to place the platform slightly below it!
        return height - self.size.height #- EPSILON
