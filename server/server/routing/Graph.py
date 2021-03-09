from server.routing.containers import Connection, Node
from typing import List
from collections import defaultdict
from heapq import heappop, heappush, heapify


class Graph:
    def __init__(self, adjacency_list: List[List[Connection]]):
        self.graph: defaultdict[int, Node] = defaultdict(Node)
        for from_node_id in range(len(adjacency_list)):
            self.graph[from_node_id] = Node(from_node_id, [])
        for from_node_id, adjacent_nodes in enumerate(adjacency_list):
            self.graph[from_node_id].outgoing_connections = adjacent_nodes
            for outgoing_connection in adjacent_nodes:
                to_id = outgoing_connection.node_idx
                incoming_connection = Connection(from_node_id, outgoing_connection.distance,
                                                 outgoing_connection.priority)
                self.graph[to_id].incoming_connections.append(incoming_connection)

    def dist_closest_robot(self, node_id: int) -> float:
        """
        Returns the distance to the closest robot which could follow the same path as a robot on the given node id.
        :param node_id:
        :return:
        """
        distances = [(float("inf"), node_id) for node_id in self.graph.keys()]
        distances.append((0, node_id))
        heapify(distances)
        unvisited = set(self.graph.keys())
        reverse_search, start_priority = False, self.graph[node_id].outgoing_connections[0].priority
        while unvisited:
            dist, curr_node_id = heappop(distances)
            unvisited.remove(curr_node_id)
            if curr_node_id != node_id and self.graph[curr_node_id].occupying_robot:
                return dist
            curr_node = self.graph[curr_node_id]
            connections = curr_node.incoming_connections if reverse_search else curr_node.outgoing_connections
            for connection in connections:
                if connection.node_idx in unvisited:
                    heappush(distances, (connection.distance + dist, connection.node_idx))
                if connection.priority > start_priority:
                    reverse_search = True
        return float("inf") # no robot found, all good to go yeet