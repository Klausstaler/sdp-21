from server.routing.containers import Connection, Node
from typing import List
from collections import defaultdict
from heapq import heappop, heappush, heapify

class Graph:
    def __init__(self, adjacency_list: List[List[Connection]]):
        self.graph: defaultdict[int, Node] = defaultdict(Node)
        self.shortest_paths: defaultdict[int, defaultdict[int, List[Node]]] = defaultdict(lambda: defaultdict(list))
        # Initializes graph datastructure
        for from_node_id in range(len(adjacency_list)):
            self.graph[from_node_id] = Node(from_node_id, [])
        for from_node_id, adjacent_nodes in enumerate(adjacency_list):
            self.graph[from_node_id].outgoing_connections = adjacent_nodes
            for outgoing_connection in adjacent_nodes:
                to_id = outgoing_connection.node_idx
                incoming_connection = Connection(from_node_id, outgoing_connection.distance,
                                                 outgoing_connection.priority)
                self.graph[to_id].incoming_connections.append(incoming_connection)

        self.__compute_shortest_paths()

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

    def __compute_shortest_paths(self) -> None:
        """
        Floyd-Warshall algo to compute the shortest paths between all nodes.
        :return:
        """
        distances: defaultdict[int, defaultdict[int, float]] = defaultdict(lambda: defaultdict(lambda: float('inf')))
        for start_location, node in self.graph.items():
            for connection in node.outgoing_connections:
                distances[start_location][connection.node_idx] = connection.distance
                self.shortest_paths[start_location][connection.node_idx] = [self.graph[connection.node_idx]]

        for k in self.graph.keys():
            for i in self.graph.keys():
                for j in self.graph.keys():
                    curr_dist = distances[i][j]
                    new_dist = distances[i][k] + distances[k][j]
                    if new_dist < curr_dist:
                        first_path = self.shortest_paths[i][k]
                        second_path = self.shortest_paths[k][j]

                        self.shortest_paths[i][j] = first_path + second_path
                        distances[i][j] = new_dist

    def get_path(self, start_location: int, end_location: int) -> List[Node]:
        return self.shortest_paths[start_location][end_location]