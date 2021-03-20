import asyncio
from asyncio import StreamReader, StreamWriter
from typing import Dict, NamedTuple

from networking.utils import encode, decode
from server.Robot import Robot
from server.Task import Task


class Connection(NamedTuple):
    reader: StreamReader
    writer: StreamWriter


def format_task(robot_id, task: Task) -> str:
    res = [robot_id, task.task_type.value]
    for key, val in task.params.items():
        res.append(",".join(map(str, [key, val])))
    # if no parameters are present, we insert the empty string at the end to present having no params
    if len(task.params) == 0:
        res.append("")
    return ":".join(map(str, res))


async def send_task(connection: Connection, robot_id, task: Task):
    cmd = encode(format_task(robot_id, task))
    # data received from client
    connection.writer.write(cmd)
    await connection.writer.drain()
    response = (await connection.reader.readline()).decode()
    print(decode(response))


class NetworkInterface:
    """
    Class representing the network interface. Dummy class for now!
    """

    def __init__(self):
        self.port, self.host = 12345, ""
        self.open_connections: Dict[str, Connection] = dict()
        print("Setting up asyncio")
        loop = asyncio.get_event_loop()
        loop.create_task(asyncio.start_server(self.receive_new_connection, self.host, self.port))
        print("Asyncio set up!")

    async def receive_new_connection(self, reader: StreamReader, writer: StreamWriter):
        connection = Connection(reader, writer)
        robot_id = decode((await reader.readline()).decode())
        self.open_connections[robot_id] = connection
        print(f"Robot ID {robot_id}")

    async def send_request(self, robot: Robot, task: Task):
        connection = await self.resolve_connection(robot.id)
        await send_task(connection, robot.id, task)
        print("Robot", robot.id, "finished task", task.task_type)

    async def resolve_connection(self, robot_id) -> Connection:
        if robot_id in self.open_connections:
            return self.open_connections[robot_id]
        else:
            await asyncio.sleep(2)
            #print(f"No connection with ID {robot_id} found! Sleeping 2 secs..")
            return await self.resolve_connection(robot_id)
