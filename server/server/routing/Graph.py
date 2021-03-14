from collections import defaultdict
from heapq import heappop, heappush, heapify
from typing import List, Dict

from server.Task import Task, TaskType
from server.routing.containers import Connection, Node, Direction


def path_to_commands(path: List[Node]) -> List[Task]:
    # oh no this is impossible
    prev_node, res = None, []
    for curr_node, next_node in zip(path[:-1], path[1:]):
        lines_to_turn = curr_node.calculate_lines_to_turn(prev_node.node_id,
                                                          next_node.node_id) if prev_node else 0  # what to do when we do not know the direction?
        if lines_to_turn > 0:
            res.append(Task(TaskType.TURN_UNTIL, {"n": lines_to_turn}))
        res.append(Task(TaskType.REACH_NODE, {"node": f"{next_node.node_id}"}))
        prev_node = curr_node
    return res


class Graph:
    def __init__(self, node_connections: Dict[int, List[Connection]]):
        self.graph: defaultdict[int, Node] = defaultdict(Node)
        self.shortest_paths: defaultdict[int, defaultdict[int, List[Node]]] = defaultdict(lambda: defaultdict(list))
        # Initializes graph datastructure
        for from_node_id in node_connections.keys():
            self.graph[from_node_id] = Node(from_node_id, [])
        for from_node_id, connections in node_connections.items():
            self.graph[from_node_id].all_connections = connections
            for connection in filter(lambda x: x is not None, connections):
                if connection.direction in [Direction.BIDIRECTIONAL, Direction.INCOMING]:
                    self.graph[from_node_id].incoming_connections.append(connection)
                if connection.direction in [Direction.BIDIRECTIONAL, Direction.OUTGOING]:
                    self.graph[from_node_id].outgoing_connections.append(connection)
            """
            for outgoing_connection in connections:
                to_id = outgoing_connection.node_id
                incoming_connection = Connection(from_node_id, outgoing_connection.distance,
                                                 outgoing_connection.priority)
                self.graph[to_id].incoming_connections.append(incoming_connection)
            """
        self.__compute_shortest_paths()

    def dist_closest_robot(self, node_id: int, priority: int) -> float:
        """
        Returns the distance to the closest robot which could follow the same path as a robot on the given node id.
        :param priority:
        :param node_id:
        :return:
        """
        distances = []
        for connection in filter(lambda conn: conn.priority > priority, self.graph[node_id].outgoing_connections):
            num_incoming_connections = len(self.graph[connection.node_id].incoming_connections)
            if num_incoming_connections > 1:  # only do check if we have a junction, otherwise it is not necessary
                distances.append((connection.distance, connection.node_id))
        # distances = [(0, node_id)]
        if distances:
            print(node_id, priority)
        heapify(distances)
        unvisited = set(self.graph.keys())
        reverse_search = False
        while unvisited and distances:
            dist, curr_node_id = heappop(distances)
            if curr_node_id not in unvisited:
                continue
            unvisited.remove(curr_node_id)
            if curr_node_id != node_id and self.graph[curr_node_id].occupying_robot:
                return dist
            curr_node = self.graph[curr_node_id]
            connections = curr_node.incoming_connections if reverse_search else curr_node.outgoing_connections
            for connection in connections:
                if connection.node_id in unvisited:
                    heappush(distances, (connection.distance + dist, connection.node_id))
                if connection.priority > priority:
                    reverse_search = True
        return float("inf")  # no robot found, all good to go yeet

    def get_commands(self, start_location: int, end_location: int) -> List[Task]:
        return path_to_commands(self.get_path(start_location, end_location))

    def get_path(self, start_location: int, end_location: int) -> List[Node]:
        return [self.graph[start_location]] + self.shortest_paths[start_location][end_location]

    def __compute_shortest_paths(self) -> None:
        """
        Floyd-Warshall algo to compute the shortest paths between all nodes.
        :return:
        """
        distances: defaultdict[int, defaultdict[int, float]] = defaultdict(lambda: defaultdict(lambda: float('inf')))
        for start_location, node in self.graph.items():
            for connection in node.outgoing_connections:
                distances[start_location][connection.node_id] = connection.distance
                self.shortest_paths[start_location][connection.node_id] = [self.graph[connection.node_id]]

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
