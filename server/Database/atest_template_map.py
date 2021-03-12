from server.routing.Graph import Graph
from server.routing.containers import Connection, Direction

# if this is wrong I will have to cry myself to sleep tonight
db_output = {
    0: [Connection(4, 3, 5, Direction.INCOMING), None, None, Connection(1, 3, 5, Direction.OUTGOING)],
    1: [Connection(0, 3, 5, Direction.INCOMING), None, Connection(2, 3, 5, Direction.OUTGOING),
        Connection(7, 1, 1, Direction.OUTGOING)],
    2: [Connection(1, 3, 5, Direction.INCOMING), None, Connection(3, 3, 5, Direction.OUTGOING),
        Connection(10, 1, 1, Direction.OUTGOING)],
    3: [Connection(2, 3, 5, Direction.INCOMING), None, None, Connection(13, 1, 1, Direction.OUTGOING)],
    4: [Connection(14, 1, 5, Direction.INCOMING), None, Connection(0, 1, 5, Direction.OUTGOING), Connection(5, 1, 5, Direction.BIDIRECTIONAL)],
    5: [Connection(4, 1, 5, Direction.BIDIRECTIONAL), None, None, None],
    6: [Connection(7, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    7: [Connection(1, 1, 1, Direction.INCOMING), Connection(8, 1, 1, Direction.BIDIRECTIONAL), Connection(17, 1, 1, Direction.OUTGOING), Connection(6, 1, 1, Direction.BIDIRECTIONAL)],
    8: [Connection(7, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    9:  [Connection(10, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    10: [Connection(9, 1, 1, Direction.BIDIRECTIONAL), Connection(2, 1, 1, Direction.INCOMING), Connection(11, 1, 1, Direction.BIDIRECTIONAL), Connection(20, 1, 1, Direction.OUTGOING)],
    11: [Connection(10, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    12: [Connection(13, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    13: [Connection(12, 1, 1, Direction.BIDIRECTIONAL), Connection(3, 1, 5, Direction.INCOMING), None, Connection(23, 1, 5, Direction.OUTGOING)],
    14: [Connection(24, 1, 5, Direction.INCOMING), None, Connection(4, 1, 5, Direction.OUTGOING), Connection(15, 1, 5, Direction.BIDIRECTIONAL)],
    15: [Connection(14, 1, 5, Direction.BIDIRECTIONAL), None, None, None],
    16: [Connection(17, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    17: [Connection(27, 1, 1, Direction.OUTGOING), Connection(16, 1, 1, Direction.BIDIRECTIONAL), Connection(7, 1, 1, Direction.INCOMING), Connection(18, 1, 1, Direction.BIDIRECTIONAL)],
    18: [Connection(17, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    19: [Connection(20, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    20: [Connection(19, 1, 1, Direction.BIDIRECTIONAL), Connection(10, 1, 1, Direction.INCOMING), Connection(21, 1, 1, Direction.BIDIRECTIONAL), Connection(30, 1, 1, Direction.OUTGOING)],
    21: [Connection(20, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    22: [Connection(23, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    23: [Connection(22, 1, 1, Direction.BIDIRECTIONAL), Connection(13, 1, 5, Direction.INCOMING), None, Connection(33, 1, 5, Direction.OUTGOING)],
    24: [Connection(34, 1, 5, Direction.INCOMING), None, Connection(14, 1, 5, Direction.OUTGOING), Connection(25, 1, 5, Direction.BIDIRECTIONAL)],
    25: [Connection(24, 1, 5, Direction.BIDIRECTIONAL), None, None, None],
    26: [Connection(27, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    27: [Connection(37, 1, 1, Direction.OUTGOING), Connection(26, 1, 1, Direction.BIDIRECTIONAL), Connection(17, 1, 1, Direction.INCOMING), Connection(28, 1, 1, Direction.BIDIRECTIONAL)],
    28: [Connection(27, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    29: [Connection(30, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    30: [Connection(29, 1, 1, Direction.BIDIRECTIONAL), Connection(20, 1, 1, Direction.INCOMING), Connection(31, 1, 1, Direction.BIDIRECTIONAL), Connection(40, 1, 1, Direction.OUTGOING)],
    31: [Connection(30, 1, 1, Direction.BIDIRECTIONAL), None, None , None],
    32: [Connection(33, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    33: [Connection(32, 1, 1, Direction.BIDIRECTIONAL), Connection(23, 1, 5, Direction.INCOMING), None, Connection(43, 1, 5, Direction.OUTGOING)],
    34: [Connection(24, 1, 5, Direction.OUTGOING), Connection(35, 1, 5, Direction.BIDIRECTIONAL), Connection(44, 1, 5, Direction.INCOMING), None],
    35: [Connection(34, 1, 5, Direction.BIDIRECTIONAL), None, None, None],
    36: [Connection(37, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    37: [Connection(47, 1, 1, Direction.OUTGOING), Connection(36, 1, 1, Direction.BIDIRECTIONAL), Connection(27, 1, 1, Direction.INCOMING), Connection(38, 1, 1, Direction.BIDIRECTIONAL)],
    38: [Connection(37, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    39: [Connection(40, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    40: [Connection(39, 1, 1, Direction.BIDIRECTIONAL), Connection(30, 1, 1, Direction.INCOMING), Connection(41, 1, 1, Direction.BIDIRECTIONAL), Connection(50, 1, 1, Direction.OUTGOING)],
    41: [Connection(40, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    42: [Connection(43, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    43: [Connection(42, 1, 1, Direction.BIDIRECTIONAL), Connection(33, 1, 1, Direction.INCOMING), None, Connection(53, 1, 5, Direction.OUTGOING)],
    44: [Connection(34, 1, 5, Direction.OUTGOING), Connection(45, 1, 5, Direction.BIDIRECTIONAL), Connection(54, 1, 1, Direction.INCOMING), None],
    45: [Connection(44, 1, 5, Direction.BIDIRECTIONAL), None, None, None],
    46: [Connection(47, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    47: [Connection(55, 1, 5, Direction.OUTGOING), Connection(46, 1, 1, Direction.BIDIRECTIONAL), Connection(37, 1, 1, Direction.INCOMING), Connection(48, 1, 1, Direction.BIDIRECTIONAL)],
    48: [Connection(47, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    49: [Connection(50, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    50: [Connection(49, 1, 1, Direction.BIDIRECTIONAL), Connection(40, 1, 1, Direction.INCOMING), Connection(51, 1, 1, Direction.BIDIRECTIONAL), Connection(56, 1, 5, Direction.OUTGOING)],
    51: [Connection(50, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    52: [Connection(53, 1, 1, Direction.BIDIRECTIONAL), None, None, None],
    53: [Connection(52, 1, 1, Direction.BIDIRECTIONAL), Connection(43, 1, 5, Direction.INCOMING), None, Connection(57, 1, 5, Direction.OUTGOING)],
    54: [Connection(44, 1, 5, Direction.OUTGOING), Connection(55, 3, 5, Direction.INCOMING), None, None],
    55: [Connection(54, 3, 5, Direction.OUTGOING), Connection(47, 1, 5, Direction.INCOMING), Connection(56, 3, 5, Direction.INCOMING), None],
    56: [Connection(55, 3, 5, Direction.OUTGOING), Connection(50, 1, 5, Direction.INCOMING), Connection(57, 3, 5, Direction.INCOMING), None],
    57: [Connection(56, 3, 5, Direction.OUTGOING), Connection(53, 1, 5, Direction.INCOMING), None, None]
}

graph = Graph(db_output)
print(graph.graph[0].incoming_connections, graph.graph[0].outgoing_connections)
graph.graph[43].occupying_robot = True
print(graph.dist_closest_robot(50))
print(len(graph.graph))
"""
print(graph.get_path(0, 3))
print(graph.get_commands(0, 3))
print(graph.get_path(0, 21))
print(graph.get_commands(0, 21))"""
#print(graph.get_path(50, 2))
#print(graph.get_commands(50, 2))
print(graph.get_commands(1, 14))