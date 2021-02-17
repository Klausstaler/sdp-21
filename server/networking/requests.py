
def handle(request):
    length, location, id, function, arguements = request.split(":") #eg 00021:manager:collect_item:apple,unit_22,shelve_2x1
    length = int(length)
    response = ""
    if location == "manager":
        response = process_manager(function, arguements)
    elif location == "robot":
        response = process_robot(function, arguements)
    return response

def process_manager(id, function, arguements):
    pass

def process_robot(id, function, arguements):
    pass