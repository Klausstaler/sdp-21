from collections import namedtuple
from typing import List
from server.Task import Task, TaskType
Size = namedtuple("Size", ["length", "width", "height"])


class Robot:
    def __init__(self, robot_id: str, size: Size, pos_id: int):
        self.pos_id = pos_id
        self.id = robot_id
        self.size = size

    def calculate_raise(self, height: float) -> float:
        """
        Calculates how much the platform needs to be raised in order for it to be at a
        specified height
        :param height: Height of the robot
        :return: The height needed to raise the platform to the appropriate level
        """
        # EPSILON = 0.02 # we want to place the platform slightly below it!
        return height - self.size.height  # - EPSILON

    def do_pickup(self, height: float) -> List[Task]:
        return ([
            # Task(TaskType.MOVEMENT, {"func_name": "strafe", "total_time": 3, "speed": 5, "right": True}),
            # Task(TaskType.RAISE_PLATFORM, {"height": self.calculate_raise(height)}),
            # Task(TaskType.PICKUP_PARCEL, {}),
            # Task(TaskType.RAISE_PLATFORM, {"height": 0.05}),
            # Task(TaskType.MOVEMENT, {"func_name": "strafe", "total_time": 4, "speed": 5, "right": False}),
        ])

    def __repr__(self):
        return f"<Robot {self.id}>"
