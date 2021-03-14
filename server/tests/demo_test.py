import asyncio

from server.CentralServer import CentralServer
from server.Robot import Robot, Size
from server.Scheduler import Scheduler
from networking.NetworkInterface import NetworkInterface
from server.Parcel import Parcel
from server.Shelf import Shelf, ShelfInfo
from server.routing.Graph import Graph, Connection, Direction, path_to_commands

db_output = {
    0: [Connection(4, 3, 5, Direction.INCOMING), None, None, Connection(1, 3, 5, Direction.OUTGOING)],
    1: [Connection(0, 3, 5, Direction.INCOMING), None, Connection(2, 3, 5, Direction.OUTGOING),
        Connection(7, 1, 1, Direction.OUTGOING)],
    2: [Connection(1, 3, 5, Direction.INCOMING), None, Connection(3, 3, 5, Direction.OUTGOING),
        Connection(10, 1, 1, Direction.OUTGOING)],
    3: [Connection(2, 3, 5, Direction.INCOMING), None, None, Connection(13, 1, 1, Direction.OUTGOING)],
    4: [Connection(14, 1, 5, Direction.INCOMING), None, Connection(0, 1, 5, Direction.OUTGOING), Connection(5, 1, 5, Direction.BIDIRECTIONAL)],
    5: [Connection(4, 1, 5, Direction.BIDIRECTIONAL), None, None, None],
    6: [Connection(7, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    7: [Connection(1, 1, 1, Direction.INCOMING), Connection(8, 1, 1, Direction.BIDIRECTIONAL), Connection(17, 1, 1, Direction.OUTGOING), Connection(6, 1, 1, Direction.BIDIRECTIONAL)],
    8: [Connection(7, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    9:  [Connection(10, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    10: [Connection(9, 1, 1, Direction.BIDIRECTIONAL), Connection(2, 1, 1, Direction.INCOMING), Connection(11, 1, 1, Direction.BIDIRECTIONAL), Connection(20, 1, 1, Direction.OUTGOING)],
    11: [Connection(10, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    12: [Connection(13, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    13: [Connection(12, 1, 1, Direction.BIDIRECTIONAL), Connection(3, 1, 5, Direction.INCOMING), None, Connection(23, 1, 5, Direction.OUTGOING)],
    14: [Connection(24, 1, 5, Direction.INCOMING), None, Connection(4, 1, 5, Direction.OUTGOING), Connection(15, 1, 5, Direction.BIDIRECTIONAL)],
    15: [Connection(14, 1, 5, Direction.BIDIRECTIONAL), None, None, None],
    16: [Connection(17, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    17: [Connection(27, 1, 1, Direction.OUTGOING), Connection(16, 1, 1, Direction.BIDIRECTIONAL), Connection(7, 1, 1, Direction.INCOMING), Connection(18, 1, 1, Direction.BIDIRECTIONAL)],
    18: [Connection(17, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    19: [Connection(20, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    20: [Connection(19, 1, 1, Direction.BIDIRECTIONAL), Connection(10, 1, 1, Direction.INCOMING), Connection(21, 1, 1, Direction.BIDIRECTIONAL), Connection(30, 1, 1, Direction.OUTGOING)],
    21: [Connection(20, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    22: [Connection(23, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    23: [Connection(22, 1, 1, Direction.BIDIRECTIONAL), Connection(13, 1, 5, Direction.INCOMING), None, Connection(33, 1, 5, Direction.OUTGOING)],
    24: [Connection(34, 1, 5, Direction.INCOMING), None, Connection(14, 1, 5, Direction.OUTGOING), Connection(25, 1, 5, Direction.BIDIRECTIONAL)],
    25: [Connection(24, 1, 5, Direction.BIDIRECTIONAL), None, None, None],
    26: [Connection(27, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    27: [Connection(37, 1, 1, Direction.OUTGOING), Connection(26, 1, 1, Direction.BIDIRECTIONAL), Connection(17, 1, 1, Direction.INCOMING), Connection(28, 1, 1, Direction.BIDIRECTIONAL)],
    28: [Connection(27, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    29: [Connection(30, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    30: [Connection(29, 1, 1, Direction.BIDIRECTIONAL), Connection(20, 1, 1, Direction.INCOMING), Connection(31, 1, 1, Direction.BIDIRECTIONAL), Connection(40, 1, 1, Direction.OUTGOING)],
    31: [Connection(30, 1, 1, Direction.BIDIRECTIONAL), None, None , None],
    32: [Connection(33, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    33: [Connection(32, 1, 1, Direction.BIDIRECTIONAL), Connection(23, 1, 5, Direction.INCOMING), None, Connection(43, 1, 5, Direction.OUTGOING)],
    34: [Connection(24, 1, 5, Direction.OUTGOING), Connection(35, 1, 5, Direction.BIDIRECTIONAL), Connection(44, 1, 5, Direction.INCOMING), None],
    35: [Connection(34, 1, 5, Direction.BIDIRECTIONAL), None, None, None],
    36: [Connection(37, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    37: [Connection(47, 1, 1, Direction.OUTGOING), Connection(36, 1, 1, Direction.BIDIRECTIONAL), Connection(27, 1, 1, Direction.INCOMING), Connection(38, 1, 1, Direction.BIDIRECTIONAL)],
    38: [Connection(37, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    39: [Connection(40, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    40: [Connection(39, 1, 1, Direction.BIDIRECTIONAL), Connection(30, 1, 1, Direction.INCOMING), Connection(41, 1, 1, Direction.BIDIRECTIONAL), Connection(50, 1, 1, Direction.OUTGOING)],
    41: [Connection(40, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    42: [Connection(43, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    43: [Connection(42, 1, 1, Direction.BIDIRECTIONAL), Connection(33, 1, 1, Direction.INCOMING), None, Connection(53, 1, 5, Direction.OUTGOING)],
    44: [Connection(34, 1, 5, Direction.OUTGOING), Connection(45, 1, 5, Direction.BIDIRECTIONAL), Connection(54, 1, 1, Direction.INCOMING), None],
    45: [Connection(44, 1, 5, Direction.BIDIRECTIONAL), None, None, None],
    46: [Connection(47, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    47: [Connection(55, 1, 5, Direction.OUTGOING), Connection(46, 1, 1, Direction.BIDIRECTIONAL), Connection(37, 1, 1, Direction.INCOMING), Connection(48, 1, 1, Direction.BIDIRECTIONAL)],
    48: [Connection(47, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    49: [Connection(50, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    50: [Connection(49, 1, 1, Direction.BIDIRECTIONAL), Connection(40, 1, 1, Direction.INCOMING), Connection(51, 1, 1, Direction.BIDIRECTIONAL), Connection(56, 1, 5, Direction.OUTGOING)],
    51: [Connection(50, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    52: [Connection(53, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    53: [Connection(52, 1, 1, Direction.BIDIRECTIONAL), Connection(43, 1, 5, Direction.INCOMING), None, Connection(57, 1, 5, Direction.OUTGOING)],
    54: [Connection(44, 1, 5, Direction.OUTGOING), Connection(55, 3, 5, Direction.INCOMING), None, None],
    55: [Connection(54, 3, 5, Direction.OUTGOING), Connection(47, 1, 1, Direction.INCOMING), Connection(56, 3, 5, Direction.INCOMING), Connection(59, 1, 2, Direction.INCOMING)],
    56: [Connection(55, 3, 5, Direction.OUTGOING), Connection(50, 1, 5, Direction.INCOMING), Connection(57, 3, 5, Direction.INCOMING), None],
    57: [Connection(56, 3, 5, Direction.OUTGOING), Connection(53, 1, 5, Direction.INCOMING), None, None],
    58: [Connection(59, 1, 1, Direction.BIDIRECTIONAL)],
    59: [Connection(62, 1, 2, Direction.INCOMING), Connection(58, 1, 2, Direction.BIDIRECTIONAL), Connection(55, 1, 5, Direction.OUTGOING), Connection(60, 1, 2, Direction.BIDIRECTIONAL)],
    60: [Connection(59, 1, 1, Direction.BIDIRECTIONAL)],
    61: [Connection(62, 1, 1, Direction.BIDIRECTIONAL)],
    62: [None, Connection(61, 1, 1, Direction.BIDIRECTIONAL), Connection(59, 1, 5, Direction.OUTGOING), Connection(63, 1, 1, Direction.BIDIRECTIONAL)],
    63: [Connection(62, 1, 1, Direction.BIDIRECTIONAL)]
}


async def parcel_pickup():
    sched = Scheduler(Graph(db_output))
    my_shelf = Shelf(1, 2, 16)
    shelf_info = ShelfInfo(my_shelf, 1)
    parcel = Parcel(12., Size(.35, .35, .35), 16, shelf_info)
    robot_size = Size(height=.25, length=.75, width=.7)
    sched.add_free_robot(Robot("2", robot_size, 56))
    sched.add_free_robot(Robot("1", robot_size, 37))
    #sched.add_free_robot(Robot("3", robot_size, 62))
    interface = NetworkInterface()
    server = CentralServer(sched, interface)
    task1 = asyncio.create_task(server.move_parcel(parcel, None))
    # await asyncio.gather(task1)

    my_shelf = Shelf(1, 2, 28)
    shelf_info = ShelfInfo(my_shelf, 1)
    parcel = Parcel(12., Size(.35, .35, .35), 28, shelf_info)
    task2 = asyncio.create_task(server.move_parcel(parcel, None))
    #task3 = asyncio.create_task(server.move_parcel(parcel, None))
    #await asyncio.gather(task1, task2)
    await asyncio.gather(task1, task2)

async def robo_move():
    sched = Scheduler(Graph(db_output))

    robot_size = Size(height=.25, length=.75, width=.7)
    robo_1, robo_2 = Robot("1", robot_size, 37), Robot("2", robot_size, 56),
    sched.add_free_robot(robo_2)
    sched.add_free_robot(robo_1)
    interface = NetworkInterface()
    server = CentralServer(sched, interface)
    sched.add_tasks(robo_1, sched.graph.get_commands(robo_1.pos_id, 53))
    sched.add_tasks(robo_1, sched.graph.get_commands(53, 50))
    sched.add_tasks(robo_2, sched.graph.get_commands(robo_2.pos_id, 50))
    sched.add_tasks(robo_2, sched.graph.get_commands(50, 57))
    t1, t2 = asyncio.create_task(server.do_tasks(robo_2)), asyncio.create_task(server.do_tasks(robo_1))
    await asyncio.gather(t1, t2)
asyncio.run(robo_move())
