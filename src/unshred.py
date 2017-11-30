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

def is_blue(coord,image):
    """
    Test if the pixel is blue
    :param coord: coordinate of the pixel you want to check
    :type coord: Tuple
    :param image: Your openned image
    :type image: Image
    """
    return colors.blue==image.getpixel(coord)

def extract_pattern (image,coord, color= colors.red, is_color=is_black):
    """
    Extract pattern of an image, from the gven coordinate "coord"
    And color the pattern with the color given
    :param image: Your openned image
    :type image: Image
    :param coord: The pixel coordinate
    :type coord: Tuple
    :param color: The color to color the pattern (default : red)
    :type color: Tuple
    :param is_color: the function that you want to use to detect the pattern
    :type is_color: function
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
            if is_color((x+1,y),image):
                coord_stack.push((x+1,y))
                image.putpixel((x+1,y),color)

        except IndexError:
            pass

        try:
            if is_color((x-1,y),image):
                coord_stack.push((x-1,y))
                image.putpixel((x-1,y),color)

        except IndexError:
            pass

        try:
            if is_color((x,y+1),image):
                coord_stack.push((x,y+1))
                image.putpixel((x,y+1),color)

        except IndexError:
            pass

        try:
            if is_color((x,y-1),image):
                coord_stack.push((x,y-1))
                image.putpixel((x,y-1),color)

        except IndexError:
            pass


    return coord_list

def number_of_images (path, prefix) :
    import os
    return int(os.popen("ls "+path+" | grep "+prefix+" | wc").read().split()[0])


def find_extremity_band (prefix_path, reverse = False) :
    """
    Find the start image if reverse is False, the end image if True
    """
    pass

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


def generate_catalog (path, prefix) :
    """
    Create the catalog containing all the valid pattern in all the bands
    :param path: the path to the folder containing the pictures
    :type path: str
    :param prefix: the prefix name of the pictures
    :type prefix: str
    """
    nb = number_of_images(path, prefix)
    for i in range (nb) :
        img = Image.open(path+prefix+str(i+1)+".png")
        img = img.convert('RGB')
        catalog_append(img)



def score_calculation(image):
    """
    Computes the score of theimage:
para:m image: The imageyou want to compute score
:type image: Image
    """
    x_size, y_size = image.size
    unshred_patterns = []
    score=0
    for i in range(y_size):
        for j in range(x_size):
            if is_blue((j,i), image):
                unshred_patterns.append( Pattern(extract_pattern(image,(j,i),colors.green,is_blue)) )

    for i in unshred_patterns:
        for j in CATALOG:
            if i.distance(j) <= 0.01:
                score += 1
    return score


def join_pictures (leftImage, rightImage):
    """
    Creates and return a new picture composed of leftImage (on the left) and rightImage (on the right)
    :param leftImage: the image you want on the left of the result image
    :type leftImage: Image
    :param rightImage: the image you want on the right of the result image
    :type leftImage: Image
    :return: a new image composed of leftImage and rightImage
    :rtype: Image
    """
    xsizel, ysizel = leftImage.size
    xsizer, ysizer = rightImage.size
    imJoin = Image.new("RGB", (xsizel+xsizer, ysizel) )
    imJoin.paste(leftImage, (0,0) )
    imJoin.paste(rightImage, (xsizel,0) )

    return imJoin


def debug_compute_score (imLeftName, imRightName) :
    imLeft = Image.open("../images/complainte/"+imLeftName)
    imRight = Image.open("../images/complainte/"+imRightName)
    imLeft = imLeft.convert("RGB")
    imRight = imRight.convert("RGB")
    find_extremity_patterns(imLeft)
    find_extremity_patterns(imRight)
    catalog_append(imLeft)
    catalog_append(imRight)
    imJoin = join_pictures(imLeft, imRight)
    print( score_calculation(imJoin) )
    imJoin.save("test.png")
    return imJoin
