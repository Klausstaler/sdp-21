from warehouse_generator import create_world

#test data which won't be here in final version
floor_size = [8,8]
shelf_size = [2,2,2]
number_of_racks = 3
line_distance_from_shelf = 0.2
grid_array = [
    [12,9,4,11],
    [5 ,8,4,7],
    [5, 8,4,7],
    [13,10,4,14],
    ]

create_world("warehouse.wbt", floor_size, shelf_size, number_of_racks, line_distance_from_shelf, grid_array)
