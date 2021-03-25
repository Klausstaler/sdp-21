from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from .models import package,node,robot,shelf,hidden_package
from .forms import packageCreateForm,packagePickForm
from django.contrib import messages
from .functions import package_request,sim_json
from home.views import home_view
import json

from server.routing.Graph import Graph
from server.routing.containers import Connection, Direction
from warehouse.server_setup import *
from server.Scheduler import Scheduler

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
    #robot.objects.all().delete()
    text = text.replace(" ","")
    try:
        dic = json.loads(text)
    except:
        return False
    grid_dimensions = dic.get('dimensions')
    dic = dic.get('nodes')
    nodes = {}
    for key in dic:
        nodes[key] = node.objects.create(id=key)
    for key in dic:
        item = dic.get(key)
        obj = nodes.get(key)
        nb = item.get('neighbours')
        directions = nb.keys()
        if 'up' in directions:
            obj.up_node = nodes.get(str(nb.get('up')[0]))
            obj.up_node_distance = nb.get('up')[1]
            obj.up_node_direction = nb.get('up')[2]
            obj.up_node_priority = nb.get('up')[3]
        if 'right' in directions:
            obj.right_node = nodes.get(str(nb.get('right')[0]))
            obj.right_node_distance = nb.get('right')[1]
            obj.right_node_direction = nb.get('right')[2]
            obj.right_node_priority = nb.get('right')[3]
        if 'down' in directions:
            obj.down_node = nodes.get(str(nb.get('down')[0]))
            obj.down_node_distance = nb.get('down')[1]
            obj.down_node_direction = nb.get('down')[2]
            obj.down_node_priority = nb.get('down')[3]
        if 'left' in directions:
            obj.left_node = nodes.get(str(nb.get('left')[0]))
            obj.left_node_distance = nb.get('left')[1]
            obj.left_node_direction = nb.get('left')[2]
            obj.left_node_priority = nb.get('left')[3]

        obj.save()

        if item.get('type') == 'shelf':
            shelf.objects.create(node=obj,compartment_size=1,number_of_compartments=3)
    sched = Scheduler(Graph(get_node_dict()))
    return True

# Create your views here.

def packages_view(request):
    packages = package.objects.all()
    context={
        'packages' : packages,
    }
    return render(request,'packages/packages.html',context)

def package_view(request,id):
    package_object = get_object_or_404(package, id=id)
    form = packageCreateForm(request.POST or None,instance=package_object)
    if form.is_valid():
        form.save()
        messages.success(request, 'Package Successfully Changed')
        return HttpResponseRedirect('/packages')
    context={
        'form' : form,
        'package' : package_object,
    }

    return render(request,'packages/package.html',context)

def create_view(request):
    form = packageCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Package Successfully Created')
        return HttpResponseRedirect('/packages')
    context={
        'form' : form
    }

    return render(request,'packages/create.html',context)


def map_gen_view(request):
    if request.POST:
        JSON = request.POST.get("data")
        jsons = JSON.split('||')
        try:
            simjson = jsons[1]
            dbjson = jsons[0]
        except:
            pass
        else:
            #print(dbjson)
            if importJSON(dbjson):
                print("Successfully Parsed!")
                messages.success(request, 'JSON Loaded')
            else:
                print('Parsing Failed!')
                messages.success(request, 'Wrong JSON Format')
            #sim_json(simjson)
    return render(request, "map_gen.html")

def map_view(request):
    packages = package.objects.all()
    nodes = node.objects.all()
    shelves = shelf.objects.all()
    robots = robot.objects.all()
    context={
        'nodes' : nodes,
        'robots' : robots,
        'shelves' : shelves,
        'packages' : packages,
    }
    return render(request,'map.html',context)

def package_request_view(request):
    form = packagePickForm(request.POST or None)
    if form.is_valid():
        data = form.data.getlist('package')
        packs = {}
        for id in data:
            pack = package.objects.get(pk=id)
            shelf = pack.shelf
            compartment = pack.shelf_compartment
            p=hidden_package.objects.create(old_id=pack.id,shelf=pack.shelf,shelf_compartment=pack.shelf_compartment,weight=pack.weight,length=pack.length,width=pack.width,height=pack.height,details=pack.details)
            packs[p.id] = p
            pack.delete()
        package_request(packs)
        messages.success(request, 'Packages Are On Their Way!')
        return HttpResponseRedirect('/get')
    context={
        'form' : form,

    }
    return render(request,'package_pick.html',context)