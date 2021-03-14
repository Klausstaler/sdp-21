from networking.NetworkInterface import NetworkInterface
from server.Parcel import Parcel
from server.Scheduler import Scheduler
from server.Task import Task, TaskType
from server.routing.Graph import Graph, path_to_commands


class CentralServer:
    def __init__(self, scheduler: Scheduler, network_interface: NetworkInterface):
        self.scheduler = scheduler
        self.network_interface = network_interface

    async def move_parcel(self, parcel: Parcel, final_location):
        robot = self.scheduler.get_free_robot()

        tasks = []
        # this is really shitty encapsulation, but I do not have time to fix it ahhhh
        graph = self.scheduler.graph
        # Shelves are only assigned to one node. We grab the node id of that node and route our robot to there
        attached_node = graph.graph[parcel.location_id].all_connections[0].node_id
        path = graph.get_path(robot.pos_id, attached_node)
        tasks.extend(path_to_commands(path))

        # now figure out by how much we have to turn the robot to pick up the parcel from the shelf.
        prev_node, curr_node = path[-2], path[-1]
        lines_to_turn = curr_node.align_for_pickup(prev_node.node_id, parcel.location_id)
        if lines_to_turn > 0:
            tasks.append(
                Task(TaskType.TURN_UNTIL, {"n": lines_to_turn}))
        # Cool shit, now we have to pick up the parcel.
        compartment_num = parcel.shelf_info.compartment_number
        needed_height = parcel.shelf_info.assigned_shelf.get_compartment_height(compartment_num)
        tasks.extend(robot.do_pickup(needed_height))
        # Now turn back to original position
        if lines_to_turn > 0:
            prev_facing = curr_node.get_facing_node_id(prev_node.node_id)
            lines_to_turn = curr_node.calculate_lines_to_turn(prev_facing, prev_facing)
            tasks.append(
                Task(TaskType.TURN_UNTIL, {"n": lines_to_turn})
            )
        tasks.extend(self.scheduler.graph.get_commands(attached_node, 0)) # move back to some position
        self.scheduler.add_tasks(robot, tasks)
        print(f"Sending tasks to robot {robot.id}")
        while self.scheduler.has_tasks(robot):
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
