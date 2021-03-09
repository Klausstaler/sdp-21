from typing import List, Union, NamedTuple

class Connection(NamedTuple):
    node_idx: int
    distance: float
    priority: int


class Node:
    def __init__(self, node_id: int, outgoing_connections: List[Connection], occupying_robot=None):
        self.node_id = node_id
        self.outgoing_connections = outgoing_connections
        self.incoming_connections: List[Connection] = []
        self.occupying_robot = occupying_robot
