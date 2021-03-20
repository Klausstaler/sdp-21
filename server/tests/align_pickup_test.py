from datetime import datetime, timedelta
start = datetime.now()
print(datetime.now())
print((datetime.now() -  start).seconds, (datetime.now() -  start).seconds < 0.01)

"""from server.routing.containers import Node, Connection, Direction
from server.routing.Graph import align_for_pickup
connections = [Connection(55, 1, 1, Direction.BIDIRECTIONAL), Connection(46, 1, 1, Direction.BIDIRECTIONAL),
               Connection(37, 1, 1, Direction.BIDIRECTIONAL), Connection(48, 1, 1, Direction.BIDIRECTIONAL)]

turn_node = Node(47, [])
turn_node.all_connections = connections
nodes = [Node(55, []), Node(46, []), Node(37, []), Node(48, [])]
print(align_for_pickup(37, turn_node, 48))


connections = [Connection(53, 1, 1, Direction.BIDIRECTIONAL), Connection(42, 1, 1, Direction.BIDIRECTIONAL),
               Connection(33, 1, 1, Direction.BIDIRECTIONAL), None]

turn_node = Node(43, [])
turn_node.all_connections = connections
nodes = [Node(53, []), Node(42, []), Node(33, [])]
print(align_for_pickup(33, turn_node, 53))"""