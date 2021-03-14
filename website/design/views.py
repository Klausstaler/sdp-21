from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from .models import package,node,robot,shelf,hidden_package
from .forms import packageCreateForm,packagePickForm
from django.contrib import messages
from .functions import get_node_list
from .functions import package_request,sim_json
from home.views import home_view
import json


def importJSON(text):
    node.objects.all().delete()
    robot.objects.all().delete()
    text = text.replace(" ","")
    try:
        dic = json.loads(text)
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

        #if item.get('type') == 'Robot':
        #    robot.objects.create(ip=ip,node=obj)
        if item.get('type') == 'Shelf':
            shelf.objects.create(node=obj,compartment_size=1,number_of_compartments=1)

    return True

# Create your views here.

def packages_view(request):
    packages = package.objects.all()
    context={
        'packages' : packages,
    }
    return render(request,'packages/packages.html',context)

def package_view(request,code):
    package_object = get_object_or_404(package, code=code)
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
        print(len(jsons))
        if importJSON(jsons[0]):
            print("Successfully Parsed!")
            messages.success(request, 'JSON Loaded')
        else:
            messages.success(request, 'Wrong JSON Format')
        simjson = jsons[1]
        sim_json(simjson)
        return HttpResponseRedirect('/generator')
        # print(JSON)
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
            p=hidden_package.objects.create(old_id=pack.id,shelf=pack.shelf,shelf_compartment=pack.shelf_compartment,weight=pack.weight,length=pack.length,width=pack.width,heigth=pack.heigth,details=pack.details)
            packs[p.id] = p
            pack.delete()
        package_request(packs)
        messages.success(request, 'Packages Are On Their Way!')
        return HttpResponseRedirect('/get')
    context={
        'form' : form,

    }
    return render(request,'package_pick.html',context)