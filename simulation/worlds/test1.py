from warehouse_generator.warehouse_generator import create_world

floor_size = [10, 9]
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
    [8,4,4,6,4,4,10,4,4,14],
    [-1, -1, 1, 5, 3, -1, -1, -1 -1, -1],
    [-1, -1, 1, 5, 3, -1, -1, -1 -1, -1]
    ]

create_world("demo_world", floor_size, shelf_size, number_of_racks, line_distance_from_shelf, grid_array)
