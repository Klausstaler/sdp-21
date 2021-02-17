from collections import deque, defaultdict
from typing import List, Dict, Set, Union

from server.networking.server import Robot
from server.networking.server import Task


class Scheduler:
    def __init__(self):
        self.free_robots: Set[Robot] = set()
        self.open_tasks: Dict[Robot, deque] = defaultdict(deque)

    def add_free_robot(self, robot: Robot) -> None:
        self.free_robots.add(robot)

    def get_free_robot(self) -> Robot:
        return next(iter(self.free_robots))

    def add_tasks(self, robot: Robot, tasks: List[Task]) -> None:
        self.open_tasks[robot].extend(tasks)
        if tasks and robot in self.free_robots:
            self.free_robots.remove(robot)

    def get_next_task(self, robot: Robot) -> Union[None, Task]:
        if self.open_tasks[robot]:
            next_task = self.open_tasks[robot].popleft()
            return next_task
        # no tasks open, add to free robots
        self.free_robots.add(robot)
        return None
