import math
from PIL import Image, ImageDraw

class LineGridGenerator():

    def __create_p_junction(self, size, line_width):
        img = Image.new("RGB", size, "white")
        drawer = ImageDraw.Draw(img)

        if (size[0]%2 == 1):
            x_line = int(math.floor(size[0]/2))
        else:
            x_line = int((size[0]/2)-1)

        if (size[1]%2 == 1):
            y_line = int(math.floor(size[1]/2))
        else:
            y_line = int((size[1]/2)-1)

        img = Image.new("RGB", size, "white")
        drawer = ImageDraw.Draw(img)
        drawer.line((0,y_line, size[0],y_line), fill="black", width=line_width)
        drawer.line((x_line,0, x_line,size[1]), fill="black", width=line_width)

        img.save("p.jpg")
        return img


    def __create_t_junction(self, size, line_width):

        if (size[0]%2 == 1):
            y_line = int(math.floor(size[1]/2))
        else:
            y_line = int((size[1]/2)-1)

        if (size[1]%2 == 1):
            x_line = int(math.floor(size[0]/2))
        else:
            x_line = int((size[0]/2)-1)

        img1 = Image.new("RGB", size, "white")
        drawer1 = ImageDraw.Draw(img1)
        drawer1.line((0,y_line, size[0],y_line), fill="black", width=line_width)
        drawer1.line((x_line,y_line, x_line,size[1]), fill="black", width=line_width)

        img2 = Image.new("RGB", size, "white")
        drawer2 = ImageDraw.Draw(img2)
        drawer2.line((0,y_line, x_line,y_line), fill="black", width=line_width)
        drawer2.line((x_line,0, x_line,size[1]), fill="black", width=line_width)

        img1.save("t1.jpg")
        img2.save("t2.jpg")
        return (img1, img2)


    def __create_line(self, size, line_width):

        if (size[0]%2 == 1):
            y_line = int(math.floor(size[1]/2))
        else:
            y_line = int((size[1]/2)-1)

        if (size[1]%2 == 1):
            x_line = int(math.floor(size[0]/2))
        else:
            x_line = int((size[0]/2)-1)

        img1 = Image.new("RGB", size, "white")
        drawer1 = ImageDraw.Draw(img1)
        drawer1.line((x_line,0, x_line,size[1]), fill="black", width=line_width)

        img2 = Image.new("RGB", size, "white")
        drawer2 = ImageDraw.Draw(img2)
        drawer2.line((0,y_line, size[0],y_line), fill="black", width=line_width)

        img1.save("l1.jpg")
        img2.save("l2.jpg")
        return (img1, img2)

    def __create_turn(self, size, line_width):

        if (size[0]%2 == 1):
            y_line = int(math.floor(size[1]/2))
        else:
            y_line = int((size[1]/2)-1)

        if (size[1]%2 == 1):
            x_line = int(math.floor(size[0]/2))
        else:
            x_line = int((size[0]/2)-1)

        img1 = Image.new("RGB", size, "white")
        drawer = ImageDraw.Draw(img1)
        drawer.line((0,y_line, x_line+int(line_width/2),y_line), fill="black", width=line_width)
        drawer.line((x_line,y_line, x_line,size[1]), fill="black", width=line_width)

        img2 = Image.new("RGB", size, "white")
        drawer = ImageDraw.Draw(img2)
        drawer.line((x_line,y_line, size[0], y_line), fill="black", width=line_width)
        drawer.line((x_line,y_line, x_line,size[1]), fill="black", width=line_width)


        img1.save("turn.jpg")
        img2.save("turn2.jpg")
        return img1, img2

    def create_line_grid(self, size, grid_array):
        if (max(size)%2 == 1):
            line_width = int(math.floor(max(size)*0.10))
        else:
            line_width = int(max(size)*0.10)

        (v_line, h_line) =              self.__create_line(size, line_width)
        p_junction =                    self.__create_p_junction(size, line_width)
        (t_h_junction, t_v_junction) =  self.__create_t_junction(size, line_width)
        (e_s_turn, n_e_turn) =          self.__create_turn(size, line_width)

        total_width = size[0] * len(grid_array[0])
        total_height = size[1] * len(grid_array)

        full_image = Image.new("RGB", (total_width, total_height), "white")

        for i in range(len(grid_array)):

            row_image = Image.new("RGB", (total_width, size[1]), "white")
            for j in range(len(grid_array[i])):

                if grid_array[i][j] == 4:
                    row_image.paste(h_line, (size[0]*j, 0))

                elif grid_array[i][j] == 5:
                    row_image.paste(v_line, (size[0]*j, 0))

                elif grid_array[i][j] == 6:
                    row_image.paste(p_junction, (size[0]*j, 0))

                elif grid_array[i][j] >= 7 and grid_array[i][j] <= 10:
                    if grid_array[i][j] < 9:
                        row_image.paste(t_v_junction.rotate((grid_array[i][j]-7)*180), (size[0]*j, 0))
                    else:
                        row_image.paste(t_h_junction.rotate((grid_array[i][j]-9)*180), (size[0]*j, 0))

                elif grid_array[i][j] == 11 or grid_array[i][j] == 13:
                    row_image.paste(e_s_turn.rotate((grid_array[i][j]-11)*90), (size[0]*j, 0))
                elif grid_array[i][j] == 12 or grid_array[i][j] == 14:
                    row_image.paste(n_e_turn.rotate((grid_array[i][j]-12)*90), (size[0]*j, 0))

            full_image.paste(row_image, (0, size[1]*i))

        return full_image
