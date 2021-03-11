from typing import List, NamedTuple
from enum import Enum


class Direction(Enum):
    BIDIRECTIONAL = "bidirectional"
    INCOMING = 'incoming'
    OUTGOING = 'outgoing'


class Connection(NamedTuple):
    node_idx: int
    distance: float
    priority: int
    direction: Direction


class Node:
    def __init__(self, node_id: int, outgoing_connections: List[Connection], occupying_robot=None):
        self.node_id = node_id
        self.all_connections = []
        self.outgoing_connections = outgoing_connections
        self.incoming_connections: List[Connection] = []
        self.occupying_robot = occupying_robot

    def __repr__(self):
        return f"<Node {self.node_id}, Occupying robot: {self.occupying_robot}>"
