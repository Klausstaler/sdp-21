from warehouse_generator import create_world

#test data which won't be here in final version
floor_size = [9,5]
shelf_size = [1,1,1]
number_of_racks = 3
line_distance_from_shelf = 0.2
grid_array = [
    [12,9,4,11,5,12,4,4,11],
    [5,5,0,5,5,5,3,1,5],
    [5,3,1,8,6,7,3,1,5],
    [5,5,2,5,5,5,3,1,5],
    [13,10,4,14,5,13,4,4,14]
    ]

create_world("warehouse.wbt", floor_size, shelf_size, number_of_racks, line_distance_from_shelf, grid_array)
