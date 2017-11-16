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
        self.__coords = list_coords
        self.__surface = len(list_coords)
        self.__gravity= self.__calc_gravity()
        self.__moments = self.__setMoments()



    def __calc_gravity(self):
        """
        Calculates the gravity center of the pattern

        :rType: Tuple
        :Examples:

        >>> p1=Pattern([(1,1),(1,1),(1,1),(1,1)])
        >>> p1.get_gravity()
        (1, 1)
        >>> p1=Pattern([(1,1),(-1,-1),(-1,-1),(1,1)])
        >>> p1.get_gravity()
        (0, 0)
        """
        gravity_center=[0,0]
        coords=self.get_coords()
        surface=self.get_surface()

        for i in range(surface):
            gravity_center[0] += coords[i][0]
            gravity_center[1] += coords[i][1]
        gravity_center[0]//=surface
        gravity_center[1]//=surface
        return tuple(gravity_center)

    def __setMoments(self):
        """
        Returns the list of 9 moments for the object self

        :rtype: list
        """
        moments = []
        for d in range(3) :
            for e in range(3) :
                moments.append( self.__calc_moment(d,e) )
        return moments

    def __calc_moment(self,d,e) :
        """
        Return the moment of order d,e of the object self

        :param d: the first order of the moment to compute
        :type d: int
        :param e: the second order of the moment to compute
        :type e: int
        :return: the moment of order d,e
        :rtype: float
        """
        x_grav, y_grav = self.get_gravity()
        coords = self.get_coords()
        moment = 0.
        for i in range(1,self.get_surface()+1) :
            x_i, y_i = coords[i-1]
            moment += (x_i - x_grav)**d * (y_i - y_grav)**e
        return moment

    def get_coords(self):
        """
        Return the list of all coordinates of the pattern

        :rtype: list of (int,int)
        """
        return self.__coords

    def get_moments(self):
        """
        Return the list of the 9 moments of the pattern

        :rtype: list of floats
        """
        return self.__moments

    def get_gravity(self):
        """
        Return the gravity center of the pattern

        :rType: Tuple
        """
        return self.__gravity

    def get_surface(self):
        """
        Return the surface of the pattern

        :rType: int
        """
        return self.__surface

    def distance(self,p2):
        """
        Return the distance between the patterns self and p2
        :param p2: Pnother pattern
        :type p2: Pattern
        :rtype: a non negative floats
        :Examples:

        >>> p1=Pattern([(3,1),(4,1),(5,3)])
        >>> p2=p1
        >>> p1.distance(p2)
        0.0
        """
        greater = (self.get_moments()[0] - p2.get_moments()[0])**2**(1/2)
        for i in range(1, len(self.get_moments())):
            tmp=(self.get_moments()[i] - p2.get_moments()[i])**2**(1/2)
            if greater < tmp :
                greater = tmp
        return greater

if __name__ == '__main__' :
    import doctest
    doctest.testmod()
