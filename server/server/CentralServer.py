from server.Parcel import Parcel
from server.Robot import Robot
from server.Scheduler import Scheduler
from server.Task import Task, TaskType
from networking.NetworkInterface import NetworkInterface


class CentralServer:
    def __init__(self, scheduler: Scheduler, network_interface: NetworkInterface):
        self.scheduler = scheduler
        self.network_interface = network_interface

    async def move_parcel(self, parcel: Parcel, final_location):
        robot = self.scheduler.get_free_robot()

        # we still need to figure out movement and other stuff

        compartment_num = parcel.shelf_info.compartment_number
        needed_height = parcel.shelf_info.assigned_shelf.get_compartment_height(compartment_num)
        # print(needed_height)
        tasks = [
            #Task(TaskType.RAISE_PLATFORM, {"height": robot.calculate_raise(needed_height)}),
            #Task(TaskType.PICKUP_PARCEL, {}),
            Task(TaskType.REACH_NODE, {"node": "6"}),
            Task(TaskType.TURN_UNTIL, {"n": 3}),
            Task(TaskType.REACH_NODE, {"node": "7"}),
            Task(TaskType.TURN_UNTIL, {"n": 3}),
            Task(TaskType.REACH_NODE, {"node": "9"}),
            ]
        self.scheduler.add_tasks(robot, tasks)
        print("Sending tasks....")
        while self.scheduler.has_tasks(robot):
            await self.network_interface.send_request(robot, self.scheduler.get_next_task(robot))
