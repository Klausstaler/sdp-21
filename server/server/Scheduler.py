from collections import deque, defaultdict
from typing import List, Dict, Set, Union
from datetime import datetime
from server.Robot import Robot, Size
from server.Task import Task, TaskType
from server.routing.Graph import Graph
import time

from design.models import robot as db_rob
from design.models import hidden_package as hp
from design.models import task
# from website.design.functions import get_node_dict

class Scheduler:
    def __init__(self, graph: Graph):
        self.open_tasks: Dict[Robot, deque[Task]] = defaultdict(deque)
        self.graph = graph
        self.DIST_THRESHOLD = 3

    def add_free_robot(self, robot: Robot) -> None:
        r = db_rob.objects.get(name=str(robot.id))
        r.status = False
        r.save()
        current_task = task.objects.get(robot=r)
        current_task.hidden_package.delete()

    def get_free_robot(self) -> Robot:
        robots = db_rob.objects.all()
        for r in robots:
            if not r.status:
                robot_size = Size(height=r.height, length=r.length, width=r.width)
                robot = Robot(r.name, robot_size, r.node_id.id)
                return robot
        raise Exception("No robot found")


    def reserve_robot(self, robot: Robot) -> None:
        r = db_rob.objects.get(name=str(robot.id))
        r.status = True
        r.save()


    def add_tasks(self, robot: Robot, tasks: List[Task], package_id) -> None:
        self.open_tasks[robot].extend(tasks)
        if tasks:
            self.reserve_robot(robot)
            r = db_rob.objects.get(name=str(robot.id))
            pack = hp.objects.get(pk=package_id)
            current_task = task.objects.create(robot=r, package=pack)
            current_task.save()

    def has_tasks(self, robot: Robot) -> bool:
        return len(self.open_tasks[robot]) > 0

    def get_next_task(self, robot: Robot) -> Union[None, Task]:
        if self.open_tasks[robot]:
            next_task = self.open_tasks[robot].popleft()
            #print(f"Sending task {next_task}")
            if next_task.task_type == TaskType.REACH_NODE:
                self.check_collisions(robot, int(next_task.params["node"]))
            return next_task
        # no tasks open, add to free robots
        self.add_free_robot(robot)
        return None

    def check_collisions(self, robot: Robot, node_id: int) -> None:
        robot_pos = robot.pos_id
        priority = self.graph.graph[robot_pos].incoming_connections[0].priority

        dist_closest = self.graph.dist_closest_robot(robot_pos, priority)
        graph = self.graph.graph
        last_time_accessed = (datetime.now() - graph[node_id].last_accessed).seconds
        #print(f"{robot}, {node_id}, {dist_closest}")
        if dist_closest <= self.DIST_THRESHOLD or (last_time_accessed < 3):
            print(f"Robot {robot.id} is too close to another robot! Stopping.", f"Other robot is {dist_closest}m away.")
            print(f"{print(graph[node_id])}")
            if last_time_accessed < 3:
                time.sleep(3 - last_time_accessed)
            else:
                time.sleep(2)
            self.check_collisions(robot, node_id)
        graph[robot.pos_id].occupying_robot = None
        graph[robot.pos_id].last_accessed = datetime.now()
        graph[node_id].occupying_robot = robot
        robot.pos_id = node_id
