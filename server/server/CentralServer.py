from networking.NetworkInterface import NetworkInterface
from server.Parcel import Parcel
from server.Scheduler import Scheduler
from server.Task import Task, TaskType


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
        tasks = self.scheduler.graph.get_commands(robot.curr_pos.node_id, parcel.location_id)
        tasks.extend([
            Task(TaskType.MOVEMENT, {"func_name": "strafe", "total_time": 3, "speed": 5, "right": True}),
            Task(TaskType.RAISE_PLATFORM, {"height": robot.calculate_raise(needed_height)}),
            Task(TaskType.PICKUP_PARCEL, {}),
            Task(TaskType.RAISE_PLATFORM, {"height": 0}),
            Task(TaskType.MOVEMENT, {"func_name": "strafe", "total_time": 4, "speed": 5, "right": False}),
        ])
        tasks.extend(self.scheduler.graph.get_commands(37, 56))
        """tasks = [
            Task(TaskType.REACH_NODE, {"node": "51"}),
            Task(TaskType.TURN_UNTIL, {"n": 3}),
            Task(TaskType.RAISE_PLATFORM, {"height": 0.01}),
            Task(TaskType.REACH_NODE, {"node": "50"}),    
            Task(TaskType.TURN_UNTIL, {"n": 2}),
            Task(TaskType.REACH_NODE, {"node": "43"}),
            Task(TaskType.REACH_NODE, {"node": "29"}),
            Task(TaskType.REACH_NODE, {"node": "15"}),
            Task(TaskType.TURN_UNTIL, {"n": 3}),
            Task(TaskType.REACH_NODE, {"node": "14"}),
            Task(TaskType.MOVEMENT, {"func_name": "strafe", "total_time": 3, "speed": 5, "right": True}),
            Task(TaskType.RAISE_PLATFORM, {"height": robot.calculate_raise(needed_height) + 0.03}),
            Task(TaskType.PICKUP_PARCEL, {}),
            Task(TaskType.RAISE_PLATFORM, {"height": 0}),

            Task(TaskType.MOVEMENT, {"func_name": "strafe", "total_time": 4, "speed": 5, "right": False}),
            Task(TaskType.REACH_NODE, {"node": "13"}),
            Task(TaskType.REACH_NODE, {"node": "12"}),
            Task(TaskType.TURN_UNTIL, {"n": 1}),
            Task(TaskType.REACH_NODE, {"node": "1"}),
            Task(TaskType.TURN_UNTIL, {"n": 3}),
            Task(TaskType.REACH_NODE, {"node": "0"}),
            Task(TaskType.MOVEMENT, {"func_name": "strafe", "total_time": 15, "speed": 7, "right": True}),
        ]"""
        self.scheduler.add_tasks(robot, tasks)
        print(f"Sending tasks to robot {robot.id}")
        while self.scheduler.has_tasks(robot):
            print(f"Robot currently at {robot.curr_pos.node_id}")
            await self.network_interface.send_request(robot, await self.scheduler.get_next_task(robot))

################# For line following demo world.
# Task(TaskType.REACH_NODE, {"node": "3"}),
# Task(TaskType.TURN_UNTIL, {"n": 2}),
# Task(TaskType.REACH_NODE, {"node": "4"}),
# Task(TaskType.TURN_UNTIL, {"n": 1}),
# Task(TaskType.REACH_NODE, {"node": "6"}),
# Task(TaskType.REACH_NODE, {"node": "9"})
################ For Basic Navigation demo world
# Task(TaskType.MOVEMENT, {"func_name":"move_forward","total_time":30, "speed":10}),
# Task(TaskType.MOVEMENT, {"func_name":"move_diagonal","total_time":35, "speed":15, "right":True}),
# Task(TaskType.MOVEMENT, {"func_name":"turn","total_time":24, "speed":12}),            
# Task(TaskType.MOVEMENT, {"func_name":"strafe","total_time":30, "speed":15}),
