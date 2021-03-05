#SDP2021
#GROUP21
#CREATED BY: REECE WALKER
#PREVIOUS VERSION BY: *BLANK*
#CURRENT VERSION BY: REECE WALKER


#PROGRAM TO GENERATE A PATH OF NODES TO FOLLOW IN ORDER TO GET FROM CURRENT NODE
#TO SPECIFIED TARGET NODE

from math import sqrt

#NODE CLASS TO BE USED IN THE A STAR SEARCH
class Node():

    #CONSTRUCTOR FOR NODE CLASS
    def __init__(self, node_position, target_node_position,
    parent_node = None, distance_from_parent = 0):
        self.parent_node = parent_node
        self.node_position = node_position
        self.g = distance_from_parent
        if parent_node is not None:
            self.g = self.g + self.parent_node.g
        self.h = self.distance_from_node(target_node_position)
        self.f = self.g + self.h

    #ALLOWS '==' TO CHECK IF ANOTHER NODE IS EQUAL TO THIS NODE
    #
    #@PARAM:
    #   Other_node:
    #       The node being comared against this node
    #
    #@RETURNS:
    #   Type boolean stating if both nodes are equal
    def __eq__(self, other_node):
        return self.node_position == other_node.node_position


    #METHOD FOR FINDING EUCLIDIEN DISTANCE FROM IT'S SELF TO ANOTHER NODE
    #
    #@PARAM:
    #   other_node_postion:
    #       list of form '[x,y]' defining the 'x,y' coords of the
    #       other node used in the distance equation
    #
    #@RETURNS:
    #   Type Float of the euclidien distance between the two nodes
    def distance_from_node(self, other_node_postion):
        a = (self.node_position[0] - other_node_postion[0])**2
        b = (self.node_position[1] - other_node_postion[1])**2
        c = sqrt(a + b)
        return c


#USED TO GENERATE A LIST CONTAINING THE OPTIMAL PATH OF NODES TO BE FOLLOWED
#TO GET FROM NODE 'start_node_index' TO NODE 'end_node_index'
#
#@PARAM:
#   node_positions:
#       2D list of the form '[n][l]' where 'n' is the node index
#       and 'l' is a list of form '[x,y]' defining the 'x,y' coords of node 'n'
#
#   node_connections:
#       2D list of the form '[n][c]' where 'n' is the node index and 'c' is
#       a list of the form '[*]' that stores the indexes of each node connected
#       to node 'n'
#
#   start_node_index:
#       Int that states which node the search should start from
#
#   end_node_index:
#       Int that states the node that is to be pathed to
#
#@RETURNS:
#   List of Int containing the node indexs in the order they should be followed
#   List still contains the starting node and ending node and the start and end
#   of the returned list respectivly
def a_star_search(
node_positions, node_connections, start_node_index, end_node_index):

    #INITILISE open_nodes AND close_nodes LISTS
    open_nodes = []
    close_nodes = []

    #CREATES starting_node AND end_node PER FUNCTION INPUTS AND ADDS
    #starting_node TO THE LIST OF OPEN NODES
    starting_node = Node(
    node_positions[start_node_index], node_positions[end_node_index])
    end_node = Node(
    node_positions[end_node_index], node_positions[end_node_index])

    open_nodes.append(starting_node)

    #START OF THE SEARCHING PROCESS
    #
    #LOOPS UNTIL open_nodes IS EMPTY
    while open_nodes:

        #FINDS OPEN NODE WITH LOWEST Node.f VALUE TO CONSIDER NEXT
        current_node = open_nodes[0]
        open_nodes_index = 0
        for i, node in enumerate(open_nodes):
             if node.f < current_node.f:
                 current_node = node
                 open_nodes_index = i

        #CHECK TO SEE IF THE ENDING NODE HAS BEEN REACHED
        if current_node == end_node:
            #ENDING NODE FOUND SO TRACE BACK STARTS FROM current_node
            node_path = []
            trace_back = current_node

            #KEEPS APPENDING EACH PARENT NODE OF THE PREVIOUS NODES UNTIL
            #NODE WITH NO PARENT SIGNIFYING THE STARTING NODE IS REACHED
            while trace_back is not None:
                node_path.append(node_positions.index(trace_back.node_position))
                trace_back = trace_back.parent_node

            #REVERSES AND RETURNS node_path
            return node_path[::-1]

        #MOVES CURRENTLY CONSIDERED NODE FROM open_nodes TO close_nodes
        open_nodes.pop(open_nodes_index)
        close_nodes.append(current_node)

        #CREATES CHILDREN OF CURRENTLY CONSIDERED NODE
        children = create_child_nodes(
        node_positions, node_connections, current_node, end_node)

        #CHECK TO SEE IF child ALREADY EXISTS WITHN close_nodes
        for child in children:
            already_exists = False
            for closed_node in close_nodes:
                if child != closed_node:
                    continue
                #SETS VARIABLE TO TRUE IF child IS FOUND IN close_nodes LIST
                already_exists = True

            #IF child DOES NOT EXIST IN close_nodes CHILD IS ADDED TO open_nodes
            if not already_exists:
                open_nodes.append(child)


#ALLOWS '==' TO CHECK IF ANOTHER NODE IS EQUAL TO THIS NODE
#
#@PARAM:
#   node_positions:
#       2D list of the form '[n][l]' where 'n' is the node index
#       and 'l' is a list of form '[x,y]' defining the 'x,y' coords of node 'n'
#
#   node_connections:
#       2D list of the form '[n][c]' where 'n' is the node index and 'c' is
#       a list of the form '[*]' that stores the indexes of each node connected
#       to node 'n'
#
#   parent_node:
#       Node that the children nodes should be created from
#
#   target_node:
#       Node that is to be pathed to
#
#@RETURNS:
#   List of Node containing the nodes connected to the parent_node as children
#   of itself
#
def create_child_nodes(node_positions, node_connections, parent_node, target_node):

    #Gets the node index of the parent_node
    parent_node_index = node_positions.index(parent_node.node_position)
    child_nodes = []

    #Uses values in node_connections to create children of parent_node
    for child in node_connections[parent_node_index]:
        child_nodes.append(
        Node(node_positions[child], target_node.node_position, parent_node, 1))
        
    return child_nodes
