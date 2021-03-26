from enum import Enum
from typing import List, NamedTuple, Union
from datetime import datetime


class Direction(Enum):
    BIDIRECTIONAL = "bidirectional"
    INCOMING = 'incoming'
    OUTGOING = 'outgoing'


class Connection(NamedTuple):
    node_id: int
    distance: float
    priority: int
    direction: Direction


class Node:
    def __init__(self, node_id: int, outgoing_connections: List[Connection], occupying_robot=None):
        self.node_id = node_id
        self.all_connections: List[Union[None, Connection]] = []
        self.outgoing_connections = outgoing_connections
        self.incoming_connections: List[Connection] = []
        self.occupying_robot = occupying_robot
        self.last_accessed = datetime.now()

    def calculate_lines_to_turn(self, prev_node_id: int, next_node_id: int) -> int:
        assert (len(self.all_connections) == 4)
        prev_idx, next_idx = 0, 0
        for i, connection in enumerate(self.all_connections):
            if connection and connection.node_id == prev_node_id:
                prev_idx = i
            if connection and connection.node_id == next_node_id:
                next_idx = i
        facing_direction = (prev_idx + 2) % len(self.all_connections)
        if facing_direction == next_idx:
            return 0
        lines_to_turn = 1
        while facing_direction != next_idx:
            if self.all_connections[facing_direction]:
                lines_to_turn += 1
            facing_direction = (facing_direction + 1) % len(self.all_connections)
        return lines_to_turn

    def align_for_pickup(self, prev_node_id: int, target_node_id: int) -> int:
        """
        Returns number of lines you have to turn in order to align the robot for pickup.
        """
        target_idx = self.get_idx(target_node_id)
        conn_to_face = (target_idx + len(self.all_connections) - 1) % len(self.all_connections)
        return self.calculate_lines_to_turn(prev_node_id, self.all_connections[conn_to_face].node_id)

    def get_idx(self, node_id: int) -> int:
        for i, connection in enumerate(self.all_connections):
            if connection and connection.node_id == node_id:
                return i

    def get_facing_node_id(self, prev_node_id: int) -> int:
        length = len(self.all_connections)
        return self.all_connections[((self.get_idx(prev_node_id) + length // 2) % length)].node_id

    def __repr__(self):
        return f"<Node {self.node_id}, Occupying robot: {self.occupying_robot}, All Connections: {self.all_connections}>"
