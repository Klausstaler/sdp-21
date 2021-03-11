from warehouse_generator import create_world

#test data which won't be here in final version
floor_size = [10,7]
shelf_size = [1,1,1]
number_of_racks = 2
line_distance_from_shelf = 0.2
grid_array = [
    [12,4,4,9,4,4,9,4,4,11],
    [5,3,1,5,3,1,5,3,1,5],
    [5,3,1,5,3,1,5,3,1,5],
    [5,3,1,5,3,1,5,3,1,5],
    [5,3,1,5,3,1,5,3,1,5],
    [5,3,1,5,3,1,5,3,1,5],
    [13,4,4,10,4,4,10,4,4,14]
    ]

create_world("warehouse.wbt", floor_size, shelf_size, number_of_racks, line_distance_from_shelf, grid_array)
