#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Shred
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

    new_x_size = image.size[0]//nb
    last_x_size = image.size[0]//nb + image.size[0]%nb

    for i in range(nb) :
        if i != nb-1 :
            newImg = Image.new("RGB",(new_x_size,image.size[1]))
        else :
            newImg = Image.new('RGB',last_x_size,image.size[1])
        newImg.save(prefix+str(i+1))

if __name__ == "__main__" :
    import sys
    if len(sys.argv) == 3 :
        main(sys.argv[1], sys.argv[2], sys.argv[3])
