import asyncio

from server.CentralServer import CentralServer
from server.Robot import Robot
from server.Scheduler import Scheduler
from server.networking.NetworkInterface import NetworkInterface


async def main():
    sched = Scheduler()
    sched.add_free_robot(Robot(10))
    sched.add_free_robot(Robot(15))
    interface = NetworkInterface()
    server = CentralServer(sched, interface)
    t1 = asyncio.create_task(server.move_parcel(None, None))
    t2 = asyncio.create_task(server.move_parcel(None, None))
    await t1
    await t2
    print(sched.free_robots, sched.open_tasks)

asyncio.run(main())