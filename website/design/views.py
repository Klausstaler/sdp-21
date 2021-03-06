from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from .models import package,node,robot,shelf,hidden_package
from .forms import packageCreateForm,packagePickForm
from django.contrib import messages
from .functions import get_node_list
from .functions import package_request

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