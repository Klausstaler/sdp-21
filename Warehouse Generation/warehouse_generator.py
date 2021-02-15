#SDP2021
#GROUP21
#CREATED BY: REECE WALKER
#PREVIOUS VERSION BY: REECE WALKER
#CURRENT VERSION BY: REECE WALKER 15/02/2021


#PROGRAM TO GENERATE A WEBOTS MAP FILE GIVIN ARGUMENTS PASSED TO IT

from line_grid_generator import LineGridGenerator
import math
from PIL import Image



#METHOD TO GENERATE WEBOTS WORLD FILE ACRODING TO INPUT
#
#@PARAM:
#   world_name:
#       String containing name of file to be created
#
#   room_size:
#       The length and breadth of the room (x,z)
#
#   shelf_size:
#       The length, breadth and height of the shelf units (x,y,z)
#
#   placement_grid:
#       2D List where 'placement_grid[i][j]' refairs to node x=i, z=j
#       Contains values from 0-14 detailing what is in that node position
#           0) Shelf with open side facing north
#           1) Shelf with open side facing east
#           2) Shelf with open side facing south
#           3) Shelf with open side facing west
#           4) Horizontal floor line
#           5) Vertical floor line
#           6) 4 way (+) floor junction
#           7) T junction (3 exits) with exits to the north, south and west
#           8) T junction (3 exits) with exits to the north, south and east
#           9) T junction (3 exits) with exits to the east, west and south
#          10) T junction (3 exits) with exits to the east, west and north
#          11) Right angle turn with exits south and west
#          12) Right angle turn with exits south and east
#          13) Right angle turn with exits north and east
#          14) Right angle turn with exits north and west


def create_world(world_name, room_size, shelf_size, placement_grid):
    #CREATES FLOOR LINE IMAGE USING 'line_grid_generator.py'
    line_gen = LineGridGenerator()
    line_grid_image = line_gen.create_line_grid(
    [int(shelf_size[0]*64),int(shelf_size[2]*64)], placement_grid)
    line_grid_image.save("warehouse_floor_grid.jpg")

    #DEFINES START OF WORLD FILE AS STRING AS THIS WON'T CHANGE BETWEEN WORLDS
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


    #DEFINES ARENA FOR THE WAREHOUSE FLOOR FROM ARGUMENTS GIVEN
    wbt_file_floor = (
"RectangleArena {\n\
  floorSize " + str(room_size[0]) + " " + str(room_size[1]) + "\n\
  floorTileSize " + str(room_size[0]) + " " + str(room_size[1]) + "\n\
  floorAppearance PBRAppearance {\n\
    baseColorMap ImageTexture {\n" +
    #URL WILL NEED TO BE CHANGED TO MATCH WHERE THE USER SAVES THE FILE OR
    #CHANGED TO THE LOCATION OF IMAGE WHEN MAP IS LOADED IN WEBOTS
      "url [\n\
        \"C:/Users/Reece/Documents/Uni Year 3/Semester 2/SDP/code/WarehouseGenCode/warehouse_floor_grid.jpg\"\n\
      ]\n\
      repeatS FALSE\n\
      repeatT FALSE\n\
    }\n\
  }\n\
  wallThickness " + str(0.2) + "\n\
  wallHeight " + str(1) + "\n\
}\n")


    #DEFINES THE GEOMETRY FOR THE SHELFS (CURRENTLY USES SHAPE NODE WILL NEED
    #TO CHANGE THIS SLIGHTLY ACORDING TO THE SHELF PROTONODE WHEN ITS DONE)
    box_geom_def = (
"    DEF BOX_GEOMETRY Shape {\n\
      appearance PBRAppearance {\n\
      }\n\
      geometry Box {\n\
        size " + str(1.0*shelf_size[0]) + " " +
        str(1.0*shelf_size[1]) + " " +
        str(1.0*shelf_size[2]) + "\n\
      }\n\
    }\n")

    #Appends both strings together into the string that will be outputted
    #as the world file
    #APPENDS BOTH STRINGS TOGETHER INTO THE STRING THAT WILL BE THE OUTPUT DATA
    #FOR THE WORLD FILE
    full_file_string = wbt_file_start + wbt_file_floor


    #CREATES OBJECTS OF SHELFS IN THE POSTIONS DEFINED BY 'placement_grid' AND
    #APPENDS THESE TO OUTPUT STRING

    #USED TO CONVERT THE 'i','j' VAULES INTO THE THE 'x','z' FORM USED BY WEBOTS
    #(WHERE THE MIDDLE POINT OF THE MAP IS 'x=0', 'z=0')
    j_conversion_x = math.floor((room_size[0]/shelf_size[0])/2)
    i_conversion_z = math.floor((room_size[1]/shelf_size[2])/2)

    #KEEPS TRACK OF SHELF NUMBERS
    shelf_num = 0

    #NESTED LOOP TO ITTERATE THROUGH THE 2D LIST
    for i in range(len(placement_grid)):
        for j in range(len(placement_grid[i])):
            #Checks if current index is a shelf (will need to add checks once
            #orientation is added for other kinds of shelfs)
            #CHECKS IF CURRENT INDEX IS A SHELF
            if placement_grid[i][j] == 0:
                #CHECKS IF THIS IS FIRST SHELF TO BE CREATED
                if not shelf_num:
                    #IF FIRST SHELF THEN CREATES SHELF ACORDING TO INPUT AND
                    #DEFINES THE GEOMETRY USED FOR ALL SUBSIQUENT SHELFS
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
                else:
                    #SHELF IS NOT FIRST SHELF SO SHOULD USE GEOMETRY DEFINED
                    #BY FIRST SHELF
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

                #APPENDS THE NEWLY CREATED SHELF'S CODE TO OUTPUT FILE
                full_file_string += obj
                #ADDS 1 TO 'shelf_num' TO KEEP TRACK OF NUMBER OF SHELFS
                shelf_num += 1

    #Writer to write the output string file to a file denoted by 'world_name'
    #in the format needed for webots map files
    #If file called the same as 'world_name' already exists it will overright it
    #if not a new file will be created

    #WRITER TO OUTPUT 'full_file_string' TO FILE DENOTED BY 'world_name'
    #FORMAT OUTPUTTED AS THE FORM NEEDED BY WEBOTS
    writer = open(world_name, "wb")
    writer.write(full_file_string.encode('utf-8'))
    writer.close()


#USED TO CREATE CODE DEFINING INSTANCE OF A BOX, WILL NEED TO BE CHANGED TO
#FIT FORMAT OF SHELF NODE
#
#@PARAM:
#   translation:
#       List of size 3 where index '0,1,2' defines shelf's 'x,y,z' coordinates
#
#   rotation:
#       List of size 4 where index '0,1,2,3' defines shelf's 'x,y,z,angle'
#       rotation values
#
#   scale:
#       List of size 3 where index '0,1,2' defines shelf's 'x,y,z' lengths in m
#
#   children:
#       String defining child nodes of shelf
#
#   boundingObject:
#       String defining the 'boundingObject' used by the shelf
#
#   name:
#       String defining the 'name' of the shelf
#
#
#@RETURNS:
#   String of code to create the shelf in webots
def create_box(translation, rotation, scale, children, boundingObject, name):

    #CREATS STRING ACORDING TO ARGUMENTS
    obj = (
"Solid {\n\
  translation " + str(translation[0]) + " " + str(translation[1]) + " " + str(translation[2]) + "\n\
  rotation " + str(rotation[0]) + " " + str(rotation[1]) + " " + str(rotation[2]) + " " + str(rotation[3]) + "\n"\
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

    #RETURNS STRING
    return obj
