from collections import deque, defaultdict
from typing import List, Dict, Set, Union

from server.Robot import Robot
from server.Task import Task, TaskType
from server.routing.containers import Node


# from website.design.functions import get_node_dict

class Scheduler:
    def __init__(self):
        self.free_robots: Set[Robot] = set()
        self.open_tasks: Dict[Robot, deque[Task]] = defaultdict(deque)
        self.graph: defaultdict[int, Node] = defaultdict(Node)
        """
        node_dict = get_node_dict()
        for from_node_id, adjacent_nodes in node_dict.items():
            self.graph[from_node_id] = Node(from_node_id, [])
            for node_id in adjacent_nodes:
                self.graph[from_node_id].connections.append(Connection(node_id, 1.))  # currently no distance support
        """

    def add_free_robot(self, robot: Robot) -> None:
        self.free_robots.add(robot)

    def get_free_robot(self) -> Robot:
        return next(iter(self.free_robots))

    def add_tasks(self, robot: Robot, tasks: List[Task]) -> None:
        self.open_tasks[robot].extend(tasks)
        if tasks and robot in self.free_robots:
            self.free_robots.remove(robot)

    def has_tasks(self, robot: Robot) -> bool:
        return len(self.open_tasks[robot]) > 0

    async def get_next_task(self, robot: Robot) -> Union[None, Task]:
        if self.open_tasks[robot]:

            next_task = self.open_tasks[robot].popleft()
            if next_task.task_type == TaskType.REACH_NODE:
                await self.check_collisions(robot, int(next_task.params["node"]))
            return next_task
        # no tasks open, add to free robots
        self.free_robots.add(robot)
        return None

    async def check_collisions(self, robot: Robot, node_id: int) -> None:
        pass
        # if self.graph[node_id].occupying_robot:
        #    await asyncio.sleep(2)
        #    await self.check_collisions(robot, node_id)
        # self.graph[robot.curr_pos.node_id].occupying_robot = None
        # self.graph[node_id].occupying_robot = robot
        # robot.curr_pos = self.graph[node_id]
