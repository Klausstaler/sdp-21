from line_grid_generator import LineGridGenerator
import math
from PIL import Image



#Function to create webot world acording to the passed arguments
def create_world(world_name, room_size, shelf_size, placement_grid):

    #Defines the start of the world file as this won't change between maps
    wbt_file_start = (
"#VRML_SIM R2021a utf8\n\
WorldInfo {\n\
  coordinateSystem \"NUE\"\n\
}\n\
Viewpoint {\n\
  orientation -1 0 0 1\n\
  position 0 4 3\n\
}\n\
TexturedBackground {\n\
}\n")


    #Defines the floor size and creates walls of the arena based on arguments
    wbt_file_floor = (
"RectangleArena {\n\
  floorSize " + str(room_size[0]) + " " + str(room_size[1]) + "\n\
  floorTileSize " + str(room_size[0]) + " " + str(room_size[1]) + "\n\
  floorAppearance PBRAppearance {\n\
    baseColorMap ImageTexture {\n\
      url [\n\
        \"set_to_url_of_line_path\"\n\
      ]\n\
      repeatS FALSE\n\
      repeatT FALSE\n\
    }\n\
  }\n\
  wallThickness " + str(0.2) + "\n\
  wallHeight " + str(1) + "\n\
}\n")

    #Defines a geometry for the shape node (This deffinition will need to change
    #slightly to work with the shelf proto node)
    box_geom_def = (
"    DEF BOX_GEOMETRY Shape {\n\
      appearance PBRAppearance {\n\
      }\n\
      geometry Box {\n\
        size " + str(1.0*shelf_size[0]) + " " + str(1.0*shelf_size[1]) + " " + str(1.0*shelf_size[2]) + "\n\
      }\n\
    }\n")

    #Appends both strings together into the string that will be outputted
    #as the world file
    full_file_string = wbt_file_start + wbt_file_floor


    #Section of code to create objects of shelfs and append these to the output
    #string when created
    shelf_num = 0
    #Used to convert the i,j values into x,y values for webots as the middle
    #point of map will be at 0,0 meaning negative values exist
    j_conversion_x = math.floor((floor_size[0]/shelf_size[0])/2)
    i_conversion_z = math.floor((floor_size[1]/shelf_size[2])/2)

    #nested loop to intterate through the 2D list
    for i in range(len(placement_grid)):
        for j in range(len(placement_grid[i])):
            #Checks if current index is a shelf (will need to add checks once
            #orientation is added for other kinds of shelfs)
            if placement_grid[i][j] == 0:
                #Checks if this is the first shelf to be defined if so
                #uses 'box_geom_def' to define the gemoetry used by each later
                #shelf
                if not shelf_num:
                    obj = create_box(
                    [
                    (j-j_conversion_x)*shelf_size[0],
                    0.5*shelf_size[1],
                    (i-i_conversion_z)*shelf_size[2]
                    ],

                    [0.0,0.0,0.0,0.0],
                    shelf_size,
                    box_geom_def,
                    "USE BOX_GEOMETRY",
                    "solid(" + str(shelf_num) + ")")
                #Means that this is not the first shelf and can use the gemoetry
                #defined earlier
                else:
                    obj = create_box(
                    [
                    (j-j_conversion_x)*shelf_size[0],
                    0.5*shelf_size[1],
                    (i-i_conversion_z)*shelf_size[2]
                    ],

                    [0.0,0.0,0.0,0.0],
                    shelf_size,
                    "    USE BOX_GEOMETRY\n",
                    "USE BOX_GEOMETRY",
                    "solid(" + str(shelf_num) + ")")

                #Appends the created shelf code to the output string
                full_file_string += obj
                #Adds 1 to shelf_num to keep track of current shelf number
                shelf_num += 1

    #Writer to write the output string file to a file denoted by 'world_name'
    #in the format needed for webots map files
    #If file called the same as 'world_name' already exists it will overright it
    #if not a new file will be created
    writer = open(world_name, "wb")
    writer.write(full_file_string.encode('utf-8'))
    writer.close()


#Method used to create an instance of a box, will need to be changed later
#to implement the shelf node when that is created
def create_box(translation, rotation, scale, children, boundingObject, name):
    obj = (
"Solid {\n\
  translation " + str(translation[0]) + " " + str(translation[1]) + " " + str(translation[2]) + "\n\
  rotation " + str(rotation[0]) + " " + str(rotation[1]) + " " + str(rotation[2]) + " " + str(rotation[3]) + "\n"\
  #scale " + str(scale[0]) + " " + str(scale[1]) + " " + str(scale[2]) + "\n\
  + "scale 1 1 1\n\
  children [\n"\
+ children + "\
  ]\n\
  name \"" + name + "\"\n\
  boundingObject " + boundingObject + "\n\
  physics Physics {\n\
    mass 1\n\
  }\n\
  linearVelocity 0.0 0.0 0.0\n\
  angularVelocity 0.0 0.0 0.0\n\
}\n")

    return obj


#test data which won't be here in final version
floor_size = [9,5]
shelf_size = [1,1,1]
grid_array = [
    [12,9,4,11,5,12,4,4,11],
    [5,5,0,5,5,5,0,0,5],
    [5,0,0,8,6,7,0,0,5],
    [5,5,0,5,5,5,0,0,5],
    [13,10,4,14,5,13,4,4,14]
    ]

line_gen = LineGridGenerator()
line_grid_image = line_gen.create_line_grid([int(shelf_size[0]*64),int(shelf_size[2]*64)], grid_array)
line_grid_image.save("warehouse_floor_grid.jpg")

create_world("withboxes.wbt", floor_size, shelf_size, grid_array)
