
from server.Robot import Robot
from server.Task import Task, TaskType
from server.Scheduler import Scheduler
from server.networking.NetworkInterface import NetworkInterface


class CentralServer:
    def __init__(self, scheduler: Scheduler, network_interface: NetworkInterface):
        self.scheduler = scheduler
        self.network_interface = network_interface
        self.network_interface.register_server(self)

    async def move_parcel(self, parcel, final_location):
        robot = self.scheduler.get_free_robot()

        self.scheduler.add_tasks(robot, [Task(TaskType.MOVE_ARM, {"5": 10})])
        self.scheduler.add_tasks(robot, [Task(TaskType.MOVE_ARM, {"1": 3})])
        print("Sending tasks....")
        await self.network_interface.send_request(robot, self.scheduler.get_next_task(robot))

    async def finished_task(self, robot: Robot):
        next_task = self.scheduler.get_next_task(robot)
        if next_task:
            await self.network_interface.send_request(robot, next_task)
