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


def generate_catalog (images) :
    """
    Create the catalog containing all the valid pattern in all the bands
    :param images: a list of image streams
    :type images: list

    """
    for img in images :
        catalog_append(img)


def clean_catalog() :
    """
    Deletes doubles in the CATALOG of patterns
    """
    copy = CATALOG.copy()
    for i in copy :
        for j in range:
            pass




def score_calculation(leftImage, rightImage):
    """
    Computes the score of the image
    :param image: The image you want to compute score
    :type image: Image
    """

    frontier = leftImage.size[0]

    image = join_pictures(leftImage, rightImage)

    x_size, y_size = image.size
    unshred_patterns = []
    score=0
    for i in range(y_size):
        for j in range(frontier-2,frontier+3) :
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

def open_image (path) :
    """
    open an image in rgb mode
    """
    return Image.open(path).convert("RGB")

def images_stream (path, prefix) :
    """
    Return a list of streams of images
    """
    nb_image = number_of_images(path,prefix)
    images = []
    for i in range(nb_image) :
        images.append(open_image(path+prefix+str(i+1)+".png"))

    return images

def find_extremities (images) :
    """
    Color the extremity pattern of all the images in the list images
    """
    for img in images :
        find_extremity_patterns(img)

def compute_score_matrix (path, prefix) :
    """
    Return the matrix of the scores
    """

    images = images_stream(path,prefix)

    find_extremities(images)

    generate_catalog(images)

    nb_image = len(images)

    matrix = []

    for i in range(nb_image) :
        scores = []
        imLeft = images[i]

        for j in range(nb_image) :

            if i == j :
                scores.append(None)
            else :
                imRight = images[j]

                scores.append (score_calculation(imLeft, imRight))

        matrix.append(scores)

    return matrix

def prefix_couples(score_matrix) :
    """
    give the list of the matching couples of pictures
    """

    couples = []

    for i in range(len(score_matrix)) :
        maxScore = 0
        maxIndex = 0
        for j in range(len(score_matrix[i])) :
            if score_matrix[i][j] == None :
                continue
            elif maxScore < score_matrix[i][j]:
                maxScore = score_matrix[i][j]
                maxIndex = j

        if maxScore == 0 :
            couples.append((i+1,))
        else :
            couples.append((i+1,maxIndex+1))

    return couples

def restore_order(couples) :
    """
    Gives the order of the images in order to recreate it
    :param couples: a list of tuples containing the indices of the matching pairs of pictures
    :type couples: list
    """
    occDict = occur_dict(couples)

    keys = occDict.keys()
    values = occDict.values()

    index = 0

    for i in range(len(values)) :
        if len(values[i]) == 1 :                                    # unfinished
            first = keys[i]




def occur_dict(couples) :
    """
    create the dictionnary of occurences and positions of each prefix in the list of tuples 'couples'
    """
    occ = dict()
    for i in range(len(couples)) :
        for j in couples[i] :

            if j in occ :
                occ[j].append(i)
            else :
                occ[j] = [i]
    return occ


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
