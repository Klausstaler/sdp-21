import asyncio

from server.CentralServer import CentralServer
from server.Robot import Robot
from server.Scheduler import Scheduler
from networking.NetworkInterface import NetworkInterface
from server.Location import Size, Location
from server.Parcel import Parcel
from server.Shelf import Shelf, ShelfInfo

async def main():
    sched = Scheduler()
    robot_size = Size(height=.25, length=.75, width=.7)
    my_shelf = Shelf(1, 2, Location(0, 0))
    shelf_info = ShelfInfo(my_shelf, 1)
    parcel = Parcel(12, Size(.35, .35, .35), Location(0, 0), shelf_info)
    sched.add_free_robot(Robot(1, robot_size))
    interface = NetworkInterface()
    server = CentralServer(sched, interface)
    await server.move_parcel(parcel, None)
    #task = asyncio.create_task(server.move_parcel(parcel, None))
    #await task

asyncio.run(main())