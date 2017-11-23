from stack import Stack
import colors
from pattern import Pattern
from PIL import Image


CATALOG = []


def is_black(coord,image):
    """
    Test if the pixel of coordinate "coord" is a nuance of black
    :param coord: coordinate of the pixel you want to check
    :type coord: Tuple
    :param image: Your openned image
    :type image: Image
    """
    r,g,b = image.getpixel(coord)
    return r==g and g==b and r<240

def extract_pattern (image,coord, color= colors.red):
    """
    Extract pattern of an image, from the gven coordinate "coord"
    And color the pattern with the color given
    :param image: Your openned image
    :type image: Image
    :param coord: The pixel coordinate
    :type coord: Tuple
    :param color: The color to color the pattern (default : red)
    :type color: Tuple
    """
    coord_stack=Stack()
    coord_stack.push(coord)
    coord_list=[]
    image.putpixel(coord_stack.top(),color)

    while(not coord_stack.is_empty()):
        coord_list.append(coord_stack.top())
        x,y=coord_stack.top()
        coord_stack.pop()

        try:
            if is_black((x+1,y),image):
                coord_stack.push((x+1,y))
                image.putpixel((x+1,y),color)

        except IndexError:
            pass

        try:
            if is_black((x-1,y),image):
                coord_stack.push((x-1,y))
                image.putpixel((x-1,y),color)

        except IndexError:
            pass

        try:
            if is_black((x,y+1),image):
                coord_stack.push((x,y+1))
                image.putpixel((x,y+1),color)

        except IndexError:
            pass

        try:
            if is_black((x,y-1),image):
                coord_stack.push((x,y-1))
                image.putpixel((x,y-1),color)

        except IndexError:
            pass


    return coord_list


def find_extremity_band (prefix, reverse = False) :
    """
    Find the start image if reverse is False, the end image if True
    """


def find_extremity_patterns (image) :
    """
    Find the extremity pattern of the image and color them
    :param image: Your opened image
    """

    len_x, len_y = image.size

    for i in range (len_y) :
        if is_black((0,i),image) :
            extract_pattern(image, (0,i), colors.blue)
        if is_black((len_x-1,i),image) :
            extract_pattern(image, (len_x-1 ,i), colors.blue)



def catalog_append (image) :
    """
    add to the catalog the complete patterns found in image
    """
    len_x, len_y = image.size

    find_extremity_patterns(image)

    for i in range (0,len_y,2) :
        for j in range (len_x) :
            if is_black((j,i), image) :
                CATALOG.append(Pattern(extract_pattern(image, (j,i))))

    image.save("test3.png")
