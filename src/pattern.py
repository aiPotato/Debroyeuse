#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Pattern module
"""

from PIL import Image


class Pattern(object):
    """
    Pattern constructor

    :param list_coords: (a list of pixel coordinates)
    :type list_coords: list of (int,int)
    :rtype: Pattern
    :return: the pattern built from the list coordinates
    :UC: list_coords is not empty

    """
    
    def __init__(self, list_coords):
        pass


    def get_coords(self):
        """
        Return the list of all coordinates of the pattern

        :rtype: list of (int,int)
        """
        pass
    
    def get_moments(self):
        """
        Return the list of the 9 moments of the pattern

        :rtype: list of floats
        """
        pass
    
    def distance(self,p2):
        """
        Return the distance between the patterns self and p2

        :rtype: a non negative float
        """
        pass
