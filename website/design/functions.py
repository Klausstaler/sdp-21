from .models import package,robot,shelf,hidden_package
from .models import task as tsk
from .models import node as nd
import asyncio

def sim_json(json):
    pass

def package_request(packs):
    for id in packs:
        pack = packs.get(id)
        print('Parcel:{}'.format(pack.old_id))
        print('Shelf:{}'.format(pack.shelf))
        print('Node:{}'.format(pack.shelf.node))


def get_node_list():
    nodes = []
    for n in nd.objects.all():
        n_of_nodes = 0
        if n.fifth_node:
            n_of_nodes+=1
        if n.fourth_node:
            n_of_nodes+=1
        if n.third_node:
            n_of_nodes+=1
        if n.second_node:
            n_of_nodes+=1
        if n.first_node:
            n_of_nodes+=1
        if n_of_nodes == 5:
            nod = [n.id,n.first_node.id,n.second_node.id,n.third_node.id,n.fourth_node.id,n.fifth_node.id]
        elif n_of_nodes == 4:
            nod = [n.id,n.first_node.id,n.second_node.id,n.third_node.id,n.fourth_node.id]
        elif n_of_nodes == 3:
            nod = [n.id,n.first_node.id,n.second_node.id,n.third_node.id]
        elif n_of_nodes == 2:
            nod = [n.id,n.first_node.id,n.second_node.id]
        elif n_of_nodes == 1:
            nod = [n.id,n.first_node.id]
        nodes.append(nod)
    return nodes

def get_node_dict():
    nodes = {}
    for n in nd.objects.all():
        n_of_nodes = 0
        if n.fifth_node:
            n_of_nodes+=1
        if n.fourth_node:
            n_of_nodes+=1
        if n.third_node:
            n_of_nodes+=1
        if n.second_node:
            n_of_nodes+=1
        if n.first_node:
            n_of_nodes+=1
        if n_of_nodes == 5:
            nod = [n.first_node.id,n.second_node.id,n.third_node.id,n.fourth_node.id,n.fifth_node.id]
        elif n_of_nodes == 4:
            nod = [n.first_node.id,n.second_node.id,n.third_node.id,n.fourth_node.id]
        elif n_of_nodes == 3:
            nod = [n.first_node.id,n.second_node.id,n.third_node.id]
        elif n_of_nodes == 2:
            nod = [n.first_node.id,n.second_node.id]
        elif n_of_nodes == 1:
            nod = [n.first_node.id]
        nodes[n.id] = nod
    return nodes

def get_connected_nodes(id):
    dictionary = get_node_dict()
    return dictionary.get(id)