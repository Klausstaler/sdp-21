from warehouse_generator import create_world

#test data which won't be here in final version
floor_size = [8,10]
shelf_size = [1,1,1]
number_of_racks = 2
line_distance_from_shelf = 0.2
grid_array = [
    [ 5,-1,-1,-1,-1,-1,-1,-1],
    [ 8, 4, 9, 4, 4, 9, 4,11],
    [5 , 3, 5, 2, 2, 5, 1, 5],
    [5 , 3, 8, 4, 4, 7, 1, 5],
    [5 , 3, 5, 2, 2, 5, 1, 5],
    [5 , 3, 8, 4, 4, 7, 1, 5],
    [5 , 3, 5, 2, 2, 5, 1, 5],
    [5 , 3, 8, 6, 6, 7, 1, 5],
    [13, 4,10,10,10,10, 4, 7],
    [-1,-1,-1,-1,-1,-1,-1, 5],
    ]

create_world("warehouse.wbt", floor_size, shelf_size, number_of_racks, line_distance_from_shelf, grid_array)
