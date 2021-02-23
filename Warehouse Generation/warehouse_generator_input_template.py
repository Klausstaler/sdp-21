from warehouse_generator import create_world

#test data which won't be here in final version
floor_size = [12,6]
shelf_size = [1,1,1]
number_of_racks = 2
line_distance_from_shelf = 0
grid_array = [
    [12,4,9,4,11,2,2,2,2,12,3,20],
    [5,1,6,3,8,4,4,4,4,7,1,11],
    [5,1,6,3,5,0,0,0,0,5,3,5],
    [8,11,0,12,7,2,2,2,2,5,1,5],
    [0,5,2,8,10,4,4,4,4,6,4,7],
    [1,10,10,10,3,0,0,0,0,0,0,0]
    ]

create_world("warehouse_example.wbt", floor_size, shelf_size, number_of_racks, line_distance_from_shelf, grid_array)
