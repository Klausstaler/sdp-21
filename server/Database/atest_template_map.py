from server.routing.containers import Connection, Node
from server.routing.Graph import Graph
adjacency_list = [[Connection(1, 3, 5)], [Connection(2, 3, 5), Connection(7, 1, 1)],
                  [Connection(3, 3, 5), Connection(10, 1, 1)], [Connection(13, 1, 1)],
                  [Connection(0, 1, 5), Connection(5, 1, 5)], [Connection(4, 1, 5)], [Connection(7, 1, 1)],
                  [Connection(17, 1, 1), Connection(6, 1, 1), Connection(8, 1, 1)], [Connection(7, 1, 1)],
                  [Connection(10, 1, 1)], [Connection(9, 1, 1), Connection(20, 1, 1), Connection(11, 1, 1)],
                  [Connection(10, 1, 1)], [Connection(13, 1, 1)], [Connection(12, 1, 1), Connection(23, 1, 5)],

                  [Connection(4, 1, 5), Connection(15, 1, 5)], [Connection(14, 1, 5)], [Connection(17, 1, 1)],
                  [Connection(27, 1, 1), Connection(16, 1, 1), Connection(18, 1, 1)], [Connection(17, 1, 1)],
                  [Connection(20, 1, 1)], [Connection(19, 1, 1), Connection(30, 1, 1), Connection(21, 1, 1)],
                  [Connection(20, 1, 1)], [Connection(23, 1, 1)], [Connection(22, 1, 1), Connection(33, 1, 5)],

                  [Connection(14, 1, 5), Connection(25, 1, 5)], [Connection(24, 1, 5)], [Connection(27, 1, 1)],
                  [Connection(37, 1, 1), Connection(26, 1, 1), Connection(28, 1, 1)], [Connection(27, 1, 1)],
                  [Connection(30, 1, 1)], [Connection(29, 1, 1), Connection(40, 1, 1), Connection(31, 1, 1)],
                  [Connection(30, 1, 1)], [Connection(33, 1, 1)], [Connection(32, 1, 1), Connection(43, 1, 5)],

                  [Connection(24, 1, 5), Connection(35, 1, 5)], [Connection(34, 1, 5)], [Connection(37, 1, 1)],
                  [Connection(47, 1, 1), Connection(36, 1, 1), Connection(38, 1, 1)], [Connection(37, 1, 1)],
                  [Connection(40, 1, 1)], [Connection(39, 1, 1), Connection(50, 1, 1), Connection(41, 1, 1)],
                  [Connection(40, 1, 1)], [Connection(43, 1, 1)], [Connection(42, 1, 1), Connection(53, 1, 5)],

                  [Connection(34, 1, 5), Connection(45, 1, 5)], [Connection(44, 1, 5)], [Connection(47, 1, 1)],
                  [Connection(55, 1, 5), Connection(46, 1, 1), Connection(48, 1, 1)], [Connection(47, 1, 1)],
                  [Connection(50, 1, 1)], [Connection(49, 1, 1), Connection(56, 1, 5), Connection(51, 1, 1)],
                  [Connection(50, 1, 1)], [Connection(53, 1, 1)], [Connection(52, 1, 1), Connection(57, 1, 5)],

                  [Connection(44, 1, 5)], [Connection(54, 3, 5)], [Connection(55, 3, 5)], [Connection(56, 3, 5)]]

graph = Graph(adjacency_list)
print(graph.graph[0].incoming_connections, graph.graph[0].outgoing_connections)
graph.graph[43].occupying_robot = True
print(graph.dist_closest_robot(50))
print(len(graph.graph))