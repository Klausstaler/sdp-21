from server.Robot import Robot
from server.Task import Task
from typing import Union
import server.CentralServer
import asyncio


class NetworkInterface:
    """
    Class representing the network itnerface. Dummy class for now!
    """

    def __init__(self):
        self.central_server: Union[None, server.CentralServer.CentralServer] = None

    def register_server(self, central_server):
        self.central_server = central_server

    async def send_request(self, robot: Robot, task: Task):
        await asyncio.sleep(1)
        print("Finished task", task.task_type)
        await self.central_server.finished_task(robot)
