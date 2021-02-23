from server.Parcel import Parcel
from server.Robot import Robot
from server.Scheduler import Scheduler
from server.Task import Task, TaskType
from networking.NetworkInterface import NetworkInterface


class CentralServer:
    def __init__(self, scheduler: Scheduler, network_interface: NetworkInterface):
        self.scheduler = scheduler
        self.network_interface = network_interface
        self.network_interface.register_server(self)

    async def move_parcel(self, parcel: Parcel, final_location):
        robot = self.scheduler.get_free_robot()

        # we still need to figure out movement and other stuff
        tasks = [
            # Task(TaskType.RAISE_PLATFORM, {"height": robot.calculate_raise(height)}),
            # Task(TaskType.PICKUP_PARCEL, {}),
            Task(TaskType.REACH_NODE, {})
            ]
        compartment_num = parcel.shelf_info.compartment_number
        needed_height = parcel.shelf_info.assigned_shelf.get_compartment_height(compartment_num)
        print(needed_height)
        tasks = [Task(TaskType.RAISE_PLATFORM, {"height": robot.calculate_raise(needed_height)}),
                 Task(TaskType.PICKUP_PARCEL, {})]
        self.scheduler.add_tasks(robot, tasks)
        print("Sending tasks....")
        await self.network_interface.send_request(robot, self.scheduler.get_next_task(robot))

    async def finished_task(self, robot: Robot):
        next_task = self.scheduler.get_next_task(robot)
        if next_task:
            await self.network_interface.send_request(robot, next_task)
