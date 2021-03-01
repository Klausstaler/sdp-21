from warehouse_generator import create_world
import json_parser as js

#test data which won't be here in final version
floor_size = [4,4]
shelf_size = [1,1,1]
number_of_racks = 3
line_distance_from_shelf = 0.2
grid_array = [
    [2,2,2,5],
    [5,5,5,5],
    [5,6,6,5],
    [6,6,6,6],
    ]

floor_size = js.grid[1] # gets values from json.txt
grid_array = js.grid[0]
print(grid_array)
create_world("warehouse.wbt", floor_size, shelf_size, number_of_racks, line_distance_from_shelf, grid_array)
