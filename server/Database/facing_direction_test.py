from server.routing.Graph import __calc_lines_to_turn
from server.routing.containers import Connection, Node, Direction

#connections = [Connection(4, 1, 1, Direction.BIDIRECTIONAL), Connection(1, 1, 1, Direction.BIDIRECTIONAL), Connection(2, 1, 1, Direction.BIDIRECTIONAL),
#               Connection(3, 1, 1, Direction.BIDIRECTIONAL)]

connections = [None, Connection(1, 1, 1, Direction.BIDIRECTIONAL), Connection(2, 1, 1, Direction.BIDIRECTIONAL),
               Connection(3, 1, 1, Direction.BIDIRECTIONAL)]
nodes = [Node(1, []), Node(2, []), Node(3, []), Node(4, [])]
turn_node = Node(10, [])
turn_node.all_connections = connections
print(__calc_lines_to_turn(nodes[0], turn_node, nodes[1]))
print(__calc_lines_to_turn(nodes[0], turn_node, nodes[2]))
#print(__calc_lines_to_turn(nodes[0], turn_node, nodes[3]))
print(__calc_lines_to_turn(nodes[0], turn_node, nodes[0]))
print()

print(__calc_lines_to_turn(nodes[1], turn_node, nodes[1]))
print(__calc_lines_to_turn(nodes[1], turn_node, nodes[2]))
#print(__calc_lines_to_turn(nodes[1], turn_node, nodes[3]))
print(__calc_lines_to_turn(nodes[1], turn_node, nodes[0]))
print()

print(__calc_lines_to_turn(nodes[2], turn_node, nodes[1]))
print(__calc_lines_to_turn(nodes[2], turn_node, nodes[2]))
#print(__calc_lines_to_turn(nodes[2], turn_node, nodes[3]))
print(__calc_lines_to_turn(nodes[2], turn_node, nodes[0]))
print()

print(__calc_lines_to_turn(nodes[3], turn_node, nodes[1]))
print(__calc_lines_to_turn(nodes[3], turn_node, nodes[2]))
#print(__calc_lines_to_turn(nodes[3], turn_node, nodes[3]))
print(__calc_lines_to_turn(nodes[3], turn_node, nodes[0]))
print()