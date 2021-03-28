from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.contrib import messages
from design.models import node,task,robot,shelf
from .forms import jsonForm
import json

from warehouse.server_setup import *

def getDirection(dir):
    if dir == 'from':
        direction = Direction.INCOMING
    elif dir == 'to':
        direction = Direction.OUTGOING
    elif dir == 'bi':
        direction = Direction.BIDIRECTIONAL
    return direction

def get_node_dict():
    nodes = {}
    for n in node.objects.all():
        data = []
        if n.right_node:
            direction = getDirection(n.right_node_direction)
            data.append(Connection(n.right_node.id,n.right_node_distance,n.right_node_priority,direction))
        else:
            data.append(None)
        if n.down_node:
            direction = getDirection(n.down_node_direction)
            data.append(Connection(n.down_node.id,n.down_node_distance,n.down_node_priority,direction))
        else:
            data.append(None)
        if n.left_node:
            direction = getDirection(n.left_node_direction)
            data.append(Connection(n.left_node.id,n.left_node_distance,n.left_node_priority,direction))
        else:
            data.append(None)
        if n.up_node:
            direction = getDirection(n.up_node_direction)
            data.append(Connection(n.up_node.id,n.up_node_distance,n.up_node_priority,direction))
        else:
            data.append(None)
        nodes[n.id] = data
    return nodes

def importJSON(text):
    node.objects.all().delete()
    robot.objects.all().delete()
    text = text.replace(" ","")
    try:
        dic = json.loads(text)
        print(dic.keys())
    except:
        return False
    nodes = {}
    for key in dic:
        nodes[key] = node.objects.create(id=key)
    for key in dic:
        item = dic.get(key)
        obj = nodes.get(key)
        nb = item.get('neighbours')
        directions = nb.keys()
        if 'up' in directions:
            obj.first_node = nodes.get(str(nb.get('up')[0]))
            obj.first_node_distance = nb.get('up')[1]
            if 'right' in directions:
                obj.second_node = nodes.get(str(nb.get('right')[0]))
                obj.second_node_distance = nb.get('right')[1]
                if 'down' in directions:
                    obj.third_node = nodes.get(str(nb.get('down')[0]))
                    obj.third_node_distance = nb.get('down')[1]
                    if 'left' in directions:
                        obj.fourth_node = nodes.get(str(nb.get('left')[0]))
                        obj.fourth_node_distance = nb.get('left')[1]
                else:
                    if 'left' in directions:
                        obj.third_node = nodes.get(str(nb.get('left')[0]))
                        obj.third_node_distance = nb.get('left')[1]
            elif 'down' in directions:
                obj.second_node = nodes.get(str(nb.get('down')[0]))
                obj.second_node_distance = nb.get('down')[1]
                if 'left' in directions:
                    obj.third_node = nodes.get(str(nb.get('left')[0]))
                    obj.third_node_distance = nb.get('left')[1]
            else:
                obj.second_node = nodes.get(str(nb.get('left')[0]))
                obj.second_node_distance = nb.get('left')[1]
        elif 'right' in directions:
            obj.first_node = nodes.get(str(nb.get('right')[0]))
            obj.first_node_distance = nb.get('right')[1]
            if 'down' in directions:
                obj.second_node = nodes.get(str(nb.get('down')[0]))
                obj.second_node_distance = nb.get('down')[1]
                if 'left' in directions:
                    obj.third_node = nodes.get(str(nb.get('left')[0]))
                    obj.third_node_distance = nb.get('left')[1]
            else:
                if 'left' in directions:
                    obj.second_node = nodes.get(str(nb.get('left')[0]))
                    obj.second_node_distance = nb.get('left')[1]
        elif 'down' in directions:
            obj.first_node = nodes.get(str(nb.get('down')[0]))
            obj.first_node_distance = nb.get('down')[1]
            if 'left' in directions:
                obj.second_node = nodes.get(str(nb.get('left')[0]))
                obj.second_node_distance = nb.get('left')[1]
        elif 'left' in directions:
            obj.first_node = nodes.get(str(nb.get('left')[0]))
            obj.first_node_distance = nb.get('left')[1]

        obj.save()

        sched.graph = Graph(get_node_dict())

        #if item.get('type') == 'Robot':
        #    robot.objects.create(ip=ip,node=obj)
        if item.get('type') == 'Shelf':
            shelf.objects.create(node=obj,compartment_size=1,number_of_compartments=1)

    return True



# Create your views here.
def home_view(request):
    tasks = task.objects.all()
    free_robots = len(robot.objects.filter(status = True))
    busy_robots = len(robot.objects.filter(status = False))

    if tasks:
        empty = False
    else:
        empty = True
    context={
        'tasks':tasks,
        'empty':empty,
        'free_robots':free_robots,
        'busy_robots': busy_robots
    }  
    return render(request, 'home.html', context)