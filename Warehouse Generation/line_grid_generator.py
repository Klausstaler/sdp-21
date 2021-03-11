#SDP2021
#GROUP21
#CREATED BY: REECE WALKER
#PREVIOUS VERSION BY: REECE WALKER
#CURRENT VERSION BY: REECE WALKER 15/02/2021

import math
from PIL import Image, ImageDraw

class LineGridGenerator():


#CREATES THE BASE IMAGE FOR THE 4 WAY (+) JUNCTION
#
#@PARAM:
#   size:
#       List of size 2 where index '0,1' define 'x,y' size of image respectivly
#
#   line_width:
#       Int stating the number of pixels line should take up (think rn odd
#       witdth will be out of line in some places)
#
#@RETURNS:
#       Object of the Image class showing the junction
    def __create_p_junction(self, size, line_width):
        img = Image.new("RGB", size, "white")
        drawer = ImageDraw.Draw(img)

        x_mid_point = (size[0]/2)-1
        y_mid_point = (size[1]/2)-1


        img = Image.new("RGB", size, "white")
        drawer = ImageDraw.Draw(img)
        drawer.line((0,y_mid_point, size[0],y_mid_point), fill="black", width=line_width)
        drawer.line((x_mid_point,0, x_mid_point,size[1]), fill="black", width=line_width)

        return img


    #CREATES THE BASE IMAGE FOR THE 3 WAY (T) JUNCTION
    #
    #@PARAM:
    #   size:
    #       List of size 2 where index '0,1' define 'x,y' size of image respectivly
    #
    #   line_width:
    #       Int stating the number of pixels line should take up (think rn odd
    #       witdth will be out of line in some places)
    #
    #@RETURNS:
    #       Tuple of Objects of the Image class showing the base T-junctions
    #       (2 needed incase of x,y of the image not being equal)
    def __create_t_junction(self, size, line_width):

        x_mid_point = (size[0]/2)-1
        y_mid_point = (size[1]/2)-1

        img1 = Image.new("RGB", size, "white")
        drawer1 = ImageDraw.Draw(img1)
        drawer1.line((0,y_mid_point, size[0],y_mid_point), fill="black", width=line_width)
        drawer1.line((x_mid_point,y_mid_point, x_mid_point,size[1]), fill="black", width=line_width)

        img2 = Image.new("RGB", size, "white")
        drawer2 = ImageDraw.Draw(img2)
        drawer2.line((0,y_mid_point, x_mid_point,y_mid_point), fill="black", width=line_width)
        drawer2.line((x_mid_point,0, x_mid_point,size[1]), fill="black", width=line_width)

        return (img1, img2)


    #CREATES THE BASE IMAGE FOR THE STRAIGHT LINE
    #
    #@PARAM:
    #   size:
    #       List of size 2 where index '0,1' define 'x,y' size of image respectivly
    #
    #   line_width:
    #       Int stating the number of pixels line should take up (think rn odd
    #       witdth will be out of line in some places)
    #
    #@RETURNS:
    #       Tuple of Objects of the Image class showing the 2 straight lines
    #       (2 needed incase of x,y of the image not being equal)
    def __create_line(self, size, line_width):

        x_mid_point = (size[0]/2)-1
        y_mid_point = (size[1]/2)-1

        img1 = Image.new("RGB", size, "white")
        drawer1 = ImageDraw.Draw(img1)
        drawer1.line((x_mid_point,0, x_mid_point,size[1]), fill="black", width=line_width)

        img2 = Image.new("RGB", size, "white")
        drawer2 = ImageDraw.Draw(img2)
        drawer2.line((0,y_mid_point, size[0],y_mid_point), fill="black", width=line_width)

        return (img1, img2)


        #CREATES THE LINE ON A SHELF NODE
        #
        #@PARAM:
        #   size:
        #       List of size 2 where index '0,1' define 'x,y' size of image respectivly
        #
        #   line_width:
        #       Int stating the number of pixels line should take up (think rn odd
        #       witdth will be out of line in some places)
        #
        #   shelf_line_dist:
        #       Int defining amount of pixels needed to be between shelf and it's
        #       acces line (where 30 = 1m between shelf and line)
        #
        #@RETURNS:
        #       Tuple of Objects of the Image class showing the 2 straight lines
        #       (2 needed incase of x,y of the image not being equal)
        def __create_shelf_line(self, full_image, size, shelf_line_dist, line_width):

            x_mid_point = (size[0]/2)-1
            y_mid_point = (size[1]/2)-1

            drawer = ImageDraw.Draw(full_image)
            drawer.line(((shelf_line_dist/2),0, x_mid_point,size[1]), fill="black", width=line_width)
            return full_image


    #CREATES THE BASE IMAGE FOR THE RIGHT ANGLE TURNS
    #
    #@PARAM:
    #   size:
    #       List of size 2 where index '0,1' define 'x,y' size of image respectivly
    #
    #   line_width:
    #       Int stating the number of pixels line should take up (think rn odd
    #       witdth will be out of line in some places)
    #
    #@RETURNS:
    #       Tuple of Objects of the Image class showing the base turns
    #       (2 needed incase of x,y of the image not being equal)
    def __create_turn(self, size, line_width):

        x_mid_point = (size[0]/2)-1
        y_mid_point = (size[1]/2)-1

        img1 = Image.new("RGB", size, "white")
        drawer1 = ImageDraw.Draw(img1)
        drawer1.line((0,y_mid_point, x_mid_point+(line_width/2),y_mid_point), fill="black", width=line_width)
        drawer1.line((x_mid_point,y_mid_point, x_mid_point,size[1]), fill="black", width=line_width)

        img2 = Image.new("RGB", size, "white")
        drawer2 = ImageDraw.Draw(img2)
        drawer2.line((x_mid_point-(line_width/2)+1,y_mid_point, size[0],y_mid_point), fill="black", width=line_width)
        drawer2.line((x_mid_point,y_mid_point, x_mid_point,size[1]), fill="black", width=line_width)

        return (img1, img2)


    #CREATES THE FULL FLOOR LINEGRID ACORDING TO THE ARGUMENTS
    #
    #@PARAM:
    #   shelf_size:
    #       List of form x,y which defines the x,y size of shelf in pixels
    #
    #   shelf_line_dist:
    #       Int defining amount of pixels needed to be between shelf and it's
    #       acces line (where 30 = 1m between shelf and line)
    #
    #   grid_array:
    #       2D List where 'grid_array[i][j]' refairs to node x=i, z=j
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
    #
    #
    #@RETURNS:
    #   Image object detailing the full floor grid
    def create_line_grid(self, shelf_size, shelf_line_dist, grid_array):

        #DEFINES THE line_width (IN PIXELS), SHOULD BE EVEN AND IS HARD CODED
        #AS THE TAPE LINE WILL BE THE SAME SIZE REGUARDLESS OF WAREHOUSE SIZE
        line_width = 2

        #DEFINES SIZE OF EACH NODE AND NUMBER OF PIXELS IN EACH IMAGE
        size = [max(shelf_size), max(shelf_size)]

        #CALLS PRIVATE METHODS TO CREATE EACH GRID IMAGE NEEDED
        (v_line, h_line) =              self.__create_line(size, line_width)
        p_junction =                    self.__create_p_junction(size, line_width)
        (t_h_junction, t_v_junction) =  self.__create_t_junction(size, line_width)
        (e_s_turn, n_e_turn) =          self.__create_turn(size, line_width)

        #WORKS OUT THE total_width AND total_height OF THE FINAL IMAGE
        #AND CREATES A BLANK white IMAGE OF THIS SIZE
        total_width = size[0] * len(grid_array[0])
        total_height = size[1] * len(grid_array)
        ##total_width = 2048
        ##total_height = 2048
        full_image = Image.new("RGB", (total_width, total_height), "white")

        #NESTED LOOP TO LOOK THROUGH grid_array AND PLACE THE CORRECT GRID IMAGE
        #ACORDING TO THE VALUES IN grid_array
        for i in range(len(grid_array)):

            #CREATES A BLANK IMAGE THAT WILL DISPLAY THE CURRENT ROW
            row_image = Image.new("RGB", (total_width, size[1]), "white")
            for j in range(len(grid_array[i])):

                #HOIZONTAL LINE SHOULD BE PLACED
                if grid_array[i][j] == 4:
                    row_image.paste(h_line, (size[0]*j, 0))

                #VERTICAL LINE SHOULD BE PLACED
                elif grid_array[i][j] == 5:
                    row_image.paste(v_line, (size[0]*j, 0))

                #PLUS JUNCTION SHOULD BE PLACED
                elif grid_array[i][j] == 6:
                    row_image.paste(p_junction, (size[0]*j, 0))

                #T JUNCTION SHOULD BE PLACED
                elif grid_array[i][j] >= 7 and grid_array[i][j] <= 10:
                    if grid_array[i][j] < 9:
                        #SHOULD USE THE T JUCTION WITH THE FULL VERTICAL LINE
                        row_image.paste(t_v_junction.rotate((grid_array[i][j]-7)*180), (size[0]*j, 0))
                    else:
                        #SHOULD USE THE T JUCTION WITH THE FULL HORIZONTAL LINE
                        row_image.paste(t_h_junction.rotate((grid_array[i][j]-9)*180), (size[0]*j, 0))

                #RIGHT ANGLE TURN SHOULD BE PLACED
                elif grid_array[i][j] == 11 or grid_array[i][j] == 13:
                    #SHOULD USE EAST TO SOUTH TURN
                    row_image.paste(e_s_turn.rotate((grid_array[i][j]-11)*90), (size[0]*j, 0))
                elif grid_array[i][j] == 12 or grid_array[i][j] == 14:
                    #SHOULD USE NORTH TO EAST TURN
                    row_image.paste(n_e_turn.rotate((grid_array[i][j]-12)*90), (size[0]*j, 0))

            #PLACES row_image ONTO full_image AT THE CORRECT SPOT FOR CURRENT ROW
            full_image.paste(row_image, (0, size[1]*i))

        #DRAWS LINES FROM PATH TO SHELF NODES
        for i in range(len(grid_array)):
            for j in range(len(grid_array[i])):
                if grid_array[i][j] >= 0 and grid_array[i][j] <=3:

                    if grid_array[i][j] == 0:
                        x_mid_point = (size[0]/2)-1
                        y_mid_point = (size[1]/2)-1

                        drawer = ImageDraw.Draw(full_image)
                        drawer.line((((size[0]*j) + x_mid_point, (size[1]*(i-1)) + y_mid_point),
                        (size[0]*j) + x_mid_point, (size[1]*(i+1)) - shelf_size[0]),
                        fill="black", width=line_width)

                        # drawer.line(((size[0]*j)+(shelf_line_dist/2), (size[1]*(i-1))+y_mid_point,
                        # (size[0]*j)+(shelf_line_dist/2), (size[1]*(i+1))-(shelf_line_dist + shelf_size[0])),
                        # fill="black", width=line_width)
                        #
                        # drawer = ImageDraw.Draw(full_image)
                        # drawer.line(((size[0]*(j+1))-(shelf_line_dist/2), (size[1]*(i-1))+y_mid_point,
                        # (size[0]*(j+1))-(shelf_line_dist/2), (size[1]*(i+1))-(shelf_line_dist + shelf_size[0])),
                        # fill="black", width=line_width)
                        #
                        # drawer = ImageDraw.Draw(full_image)
                        # drawer.line(((size[0]*j)+(shelf_line_dist/2), ((size[1]*(i+1)-(shelf_line_dist + shelf_size[0]))),
                        # (size[0]*(j+1))-(shelf_line_dist/2), ((size[1]*(i+1)-(shelf_line_dist + shelf_size[0])))),
                        # fill="black", width=line_width)


                    elif grid_array[i][j] == 1:
                        x_mid_point = (size[0]/2)-1
                        y_mid_point = (size[1]/2)-1

                        drawer = ImageDraw.Draw(full_image)
                        drawer.line(((size[0]*j) + shelf_size[0], ((size[1]*i) + y_mid_point),
                        (size[0]*(j+1)) + x_mid_point, ((size[1]*i) + y_mid_point)),
                        fill="black", width=line_width)


                        # drawer.line(((size[0]*j)+(shelf_size[0] + shelf_line_dist), (size[1]*i)+(shelf_line_dist/2),
                        # (size[0]*(j+1))+x_mid_point, (size[1]*i)+(shelf_line_dist/2)),
                        # fill="black", width=line_width)
                        #
                        # drawer = ImageDraw.Draw(full_image)
                        # drawer.line(((size[0]*j)+(shelf_size[0] + shelf_line_dist), (size[1]*(i+1))-(shelf_line_dist/2),
                        # (size[0]*(j+1))+x_mid_point, (size[1]*(i+1))-(shelf_line_dist/2)),
                        # fill="black", width=line_width)
                        #
                        # drawer = ImageDraw.Draw(full_image)
                        # drawer.line(((size[0]*j)+(shelf_size[0] + shelf_line_dist), (size[1]*i)+(shelf_line_dist/2),
                        # (size[0]*j)+(shelf_size[0] + shelf_line_dist), (size[1]*(i+1))-(shelf_line_dist/2)),
                        # fill="black", width=line_width)



                    elif grid_array[i][j] == 2:
                        x_mid_point = (size[0]/2)-1
                        y_mid_point = (size[1]/2)-1

                        drawer = ImageDraw.Draw(full_image)
                        drawer.line((((size[0]*j) + x_mid_point, (size[1]*(i)) + shelf_size[0],
                        (size[0]*j) + x_mid_point, (size[1]*(i+1)) + y_mid_point)),
                        fill="black", width=line_width)

                        #drawer = ImageDraw.Draw(full_image)
                        # drawer.line(((size[0]*j)+(shelf_line_dist/2), ((size[1]*(i)+(shelf_line_dist + shelf_size[0]))),
                        # (size[0]*j)+(shelf_line_dist/2),(size[1]*(i+1))+y_mid_point),
                        # fill="black", width=line_width)
                        #
                        # drawer = ImageDraw.Draw(full_image)
                        # drawer.line(((size[0]*(j+1))-(shelf_line_dist/2), ((size[1]*(i)+(shelf_line_dist + shelf_size[0]))),
                        # (size[0]*(j+1))-(shelf_line_dist/2), (size[1]*(i+1))+y_mid_point),
                        # fill="black", width=line_width)
                        #
                        # drawer = ImageDraw.Draw(full_image)
                        # drawer.line(((size[0]*j)+(shelf_line_dist/2), (((size[1]*(i))+(shelf_line_dist + shelf_size[0]))),
                        # (size[0]*(j+1))-(shelf_line_dist/2), (((size[1]*(i))+(shelf_line_dist + shelf_size[0])))),
                        # fill="black", width=line_width)


                    else:
                        x_mid_point = (size[0]/2)-1
                        y_mid_point = (size[1]/2)-1

                        drawer = ImageDraw.Draw(full_image)
                        drawer.line(((size[0]*j) - x_mid_point, (size[1]*i) + y_mid_point,
                        (size[0]*(j+1)) - shelf_size[0], (size[1]*i) + y_mid_point),
                        fill="black", width=line_width)

                        # drawer.line(((size[0]*(j-1))+x_mid_point, (size[1]*i)+(shelf_line_dist/2),
                        # (size[0]*(j+1))-(shelf_line_dist + shelf_size[0]), (size[1]*i)+(shelf_line_dist/2)),
                        # fill="black", width=line_width)
                        #
                        # drawer = ImageDraw.Draw(full_image)
                        # drawer.line(((size[0]*(j-1))+x_mid_point, (size[1]*(i+1))-(shelf_line_dist/2),
                        # (size[0]*(j+1))-(shelf_line_dist + shelf_size[0]), (size[1]*(i+1))-(shelf_line_dist/2)),
                        # fill="black", width=line_width)
                        #
                        # drawer = ImageDraw.Draw(full_image)
                        # drawer.line(((size[0]*(j+1))-(shelf_line_dist + shelf_size[0]), (size[1]*i)+(shelf_line_dist/2),
                        # ((size[0]*(j+1))-(shelf_line_dist + shelf_size[0])), (size[1]*(i+1))-(shelf_line_dist/2)),
                        # fill="black", width=line_width)
        #n = 0;
        #while(pow(n, 2) < total_width){
        #    n++
        #}
        power_width = 2048
        power_height = 2048
        full_image_powered = Image.new("RGB", (power_width, power_height), "orange")
        offset = ((power_width - total_width) // 2, (power_height - total_height) // 2)
        full_image_powered.paste(full_image, offset)



        #RETURNS THE FULL IMAGE OF THE FLOOR GRID
        return full_image_powered
