from warehouse_generator import create_world

#test data which won't be here in final version
floor_size = [9,4]
shelf_size = [1,1,1]
number_of_racks = 3
line_distance_from_shelf = 0.2
grid_array = [
    [12,4,9,4,4,4,4,11,3],
    [5,1,5,2,2,2,2,5,3],
    [5,3,13,4,4,4,4,14,3],
    [0,20,20,0,0,0,0,0,20],
    ]

create_world("warehouse.wbt", floor_size, shelf_size, number_of_racks, line_distance_from_shelf, grid_array)
