from warehouse_generator.warehouse_generator import create_world

floor_size = [8,10] # width by height
shelf_size = [1,1,1]
number_of_racks = 2
line_distance_from_shelf = 0.1
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

create_world("WarehouseGenerator", floor_size, shelf_size, number_of_racks, line_distance_from_shelf, grid_array)
