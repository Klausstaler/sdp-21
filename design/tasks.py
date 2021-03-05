from celery.decorators import task
from celery.utils.log import get_task_logger
from .models import package,robot,shelf,hidden_package
from .models import task as tsk
from .models import node as nd
import asyncio
#from .pickup_test import main

logger = get_task_logger(__name__)

#divy node list
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
        
@task(name="send_robot")
def send_robot(ids):
    node_list = get_node_list()
    print(node_list)
    #get robots fields
    robots=[]
    for r in robot.objects.all():
        robots.append(r)
        ip = r.ip
        node = r.node_id
        status = r.status
        
    #Example task create
    for i in ids:
        p = hidden_package.objects.get(pk=i)
        tsk.objects.create(robot=robots[0],package=p,holding_package=0)

    #How to save to db
    #sh = shelf.objects.get(pk=1)
    #package.objects.create(id=18,shelf=sh,shelf_compartment=10)

    #asyncio.run(main())

       