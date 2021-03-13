from collections import deque, defaultdict
from typing import List, Dict, Set, Union

from server.Robot import Robot
from server.Task import Task, TaskType
from server.routing.Graph import Graph
import asyncio


# from website.design.functions import get_node_dict

class Scheduler:
    def __init__(self, graph: Graph):
        self.free_robots: Set[Robot] = set()
        self.open_tasks: Dict[Robot, deque[Task]] = defaultdict(deque)
        self.graph = graph
        self.DIST_THRESHOLD = 2

    def add_free_robot(self, robot: Robot) -> None:
        self.graph.graph[robot.pos_id].occupying_robot = robot
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
            print(f"Sending task {next_task}")
            if next_task.task_type == TaskType.REACH_NODE:
                await self.check_collisions(robot, int(next_task.params["node"]))
            return next_task
        # no tasks open, add to free robots
        self.free_robots.add(robot)
        return None

    async def check_collisions(self, robot: Robot, node_id: int) -> None:
        robot_pos = robot.pos_id
        priority = self.graph.graph[robot_pos].incoming_connections[0].priority
        #for connection in self.graph.graph[robot_pos].outgoing_connections:
        #    if connection.node_id == node_id:
        #        priority = connection.priority
        #        break
        dist_closest = self.graph.dist_closest_robot(robot_pos, priority)
        if dist_closest <= self.DIST_THRESHOLD:
            print(f"Robot {robot.id} is too close to another robot! Stopping...")
            await asyncio.sleep(2)
            await self.check_collisions(robot, node_id)
        self.graph.graph[robot.pos_id].occupying_robot = None
        self.graph.graph[node_id].occupying_robot = robot
        robot.pos_id = node_id
