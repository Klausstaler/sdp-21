from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.contrib import messages
from design.models import node,task,robot,shelf
from .forms import jsonForm
import json


def parseJSONstring(text):
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

        #if item.get('type') == 'Robot':
        #    robot.objects.create(ip=ip,node=obj)
        if item.get('type') == 'Shelf':
            shelf.objects.create(node=obj,compartment_size=1,number_of_compartments=1)

    return True



# Create your views here.
def home_view(request, JSON = None):
    # form = jsonForm(request.POST or None)
    # if form.is_valid():
    #     node.objects.all().delete()
    #     robot.objects.all().delete()
    if JSON != None:
        if parseJSONstring(JSON):
            print("Successfully Parsed!")
            messages.success(request, 'JSON Loaded')
        else:
            messages.success(request, 'Wrong JSON Format')
        # return HttpResponseRedirect('/')
        tasks = task.objects.all()
        context={
            'tasks':tasks,
            # 'form':form,
        }
    
    return render(request, 'home.html', context = None)