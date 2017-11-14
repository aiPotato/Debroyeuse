#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Shred
tshis is a test
"""


from PIL import Image

def main (imageName, nb, prefix) :
    import os
    curPath = os.getcwd()

    temp = imageName.split(".")
    temp.pop()
    dirName = ".".join(temp)

    path = "../images/"+dirName+"/"
    os.chdir(path)

    shred(Image.open(imageName), nb, prefix)

    os.chdir(curPath)



def shred (image, nb, prefix) :
    """
    Shred the image given in parameter in nb vertical pieces. Creates nb new image files.

    :param image: the image to shred
    :type image:
    :param nb: number of pieces wanted
    :type nb: int
    :param prefix: the prefix of the new files
    :type prefix: str
    :side effect: creates new image files
    :return: None
    """
    x_size, y_size = image.size


    new_x_size = x_size//nb
    last_x_size = x_size//nb + image.size[0]%nb

    for i in range(nb) :
        if i != nb-1 :
            newImg = image.crop((i*new_x_size,0,(i+1)*new_x_size,y_size))
        else :
            newImg = image.crop((i*new_x_size,0, i*new_x_size + last_x_size ,y_size))
        newImg.save(prefix+str(i+1)+".png")

if __name__ == "__main__" :
    import sys
    if len(sys.argv) == 4 :
        main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
