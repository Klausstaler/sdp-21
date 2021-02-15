from warehouse_generator import create_world

#test data which won't be here in final version
floor_size = [9,6]
shelf_size = [1,1,1.2]
grid_array = [
    [12,9,4,11,5,12,4,4,11],
    [5,5,0,5,5,5,0,0,5],
    [5,0,0,8,6,7,0,0,5],
    [5,5,0,5,5,5,0,0,5],
    [13,10,4,14,5,13,4,4,14]
    ]

create_world("withboxes.wbt", floor_size, shelf_size, grid_array)
