import asyncio
import time

from server.CentralServer import CentralServer
from server.Robot import Robot
from server.Scheduler import Scheduler
from server.networking.NetworkInterface import NetworkInterface

sched = Scheduler()
sched.add_free_robot(Robot(10))
interface = NetworkInterface()
server = CentralServer(sched, interface)
asyncio.run(server.move_parcel(None, None))