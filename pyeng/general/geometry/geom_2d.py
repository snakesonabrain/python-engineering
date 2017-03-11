#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

from pyeng.general.validation import ValidationDecorator, validate_float
import numpy as np

class TwodimensionalShape(object):
    """
    Calculates geometrical properties of a 2D shape

    :returns:   Area of the shape (:math:`A`) [:math:`m2`], x-coordinate of the centroid (:math:`x_c`) [:math:`m`],
        y-coordinate of the centroid (:math:`y_c`) [:math:`m`], Area moment of inertia about the centroidal x-axis (:math:`I_{x_c}`) [:math:`m4`],
        Area moment of inertia about the centroidal y-axis (:math:`I_{y_c}`) [:math:`m4`],
        Area moment of inertia about the x-axis (:math:`I_x`) [:math:`m4`],
        Area moment of inertia about the y-axis (:math:`I_y`) [:math:`m4`],
        Polar area moment of inertia (:math:`J`) [:math:`m4`],
        Radius of gyration relative to the centroidal x-axis (:math:`r_{x_c}`) [:math:`m`],
        Radius of gyration relative to the centroidal y-axis (:math:`r_{y_c}`) [:math:`m`],
        Radius of gyration relative to the x-axis (:math:`r_x`) [:math:`m`],
        Radius of gyration relative to the y-axis (:math:`r_y`) [:math:`m`],
        Polar radius of gyration (:math:`r_p`) [:math:`m`],
        Product of inertia relative to the centroid (:math:`I_{x_c y_c}`) [:math:`m4`],
        Product of inertia relative to the axes shown in the figure (:math:`i_{xy}`) [:math:`m4`]

    :rtype: Python dictionary with keys: centroid['area [m2]'],centroid['x [m]'],centroid['y [m]'],areamoment_inertia['I_xc [m4]'],
        areamoment_inertia['I_yc [m4]'],areamoment_inertia['I_x [m4]'],areamoment_inertia['I_y [m4]'],radius_gyration['r_xc [m]'],
        radius_gyration['r_yc [m]'],radius_gyration['r_x [m]'],radius_gyration['r_y [m]'],product_inertia['I_xc_yc [m4]'],
        product_inertia['I_xy [m4]']

    Reference - Wikipedia: https://en.wikipedia.org/wiki/List_of_second_moments_of_area

    """

    def __init__(self):
        self.centroid = {'area [m2]': np.NaN, 'x [m]': np.NaN, 'y [m]': np.NaN}
        self.areamoment_inertia = {'I_xc [m4]': np.NaN,
                                   'I_yc [m4]': np.NaN,
                                   'I_x [m4]': np.NaN,
                                   'I_y [m4]': np.NaN,
                                   'J [m4]': np.NaN}
        self.radius_gyration = {'r_xc [m]': np.NaN,
                                'r_yc [m]': np.NaN,
                                'r_x [m]': np.NaN,
                                'r_y [m]': np.NaN,
                                'r_p [m]': np.NaN}
        self.product_inertia = {'I_xc_yc [m4]': np.NaN,
                                'I_x_y [m4]': np.NaN}

RIGHTTRIANGLERIGHT = {
    'base_width':{'type': 'float','min_value':0.0,'max_value':None},
    'height':{'type': 'float','min_value':0.0,'max_value':None},
}

class RightTriangleRight(TwodimensionalShape):
    """
    Represents a right triangle with the right angle on the right (see figure). Derived geometrical properties are calculated when an instance is created

    :param base_width: Width of the triangle base (:math:`b`) [:math:`m`]  - Suggested range: 0.0<=base_width
    :param height: Height of the triangle (:math:`h`) [:math:`m`]  - Suggested range: 0.0<=height

    .. math::
        A = \\frac{b h}{2}

        x_c = \\frac{2 b}{3}

        y_c = \\frac{h}{3}

        I_{x_c} = \\frac{b h^3}{36}

        I_{y_c} = \\frac{b^3 h}{36}

        I_x = \\frac{b h^3}{12}

        I_y = \\frac{b^3 h}{4}

        r^2_{x_c} = \\frac{h^2}{18}

        r^2_{y_c} = \\frac{b^2}{18}

        r^2_{x} = \\frac{h^2}{6}

        r^2_{y} = \\frac{b^2}{2}

        I_{x_c y_c} = \\frac{b^2 h^2}{72}

        I_{xy} = \\frac{b^2 h^2}{8}

    .. figure:: images/RightTriangleRight.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Geometry of a right triangle with right angle on the right

    """

    def __init__(self,base_width, height,fail_silently=True):
        self._base_width = base_width
        self._height = height
        self._fail_silently = fail_silently
        self.calculate()

    @property
    def base_width(self):
        return self._base_width

    @base_width.setter
    def base_width(self, value):
        self._base_width = value
        if value: self.calculate()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        if value: self.calculate()

    @property
    def fail_silently(self):
        return self._fail_silently

    @fail_silently.setter
    def fail_silently(self, value):
        self._fail_silently = value

    def calculate(self):
        self.calculate_validated(self._base_width, self._height, fail_silently=self._fail_silently)

    @ValidationDecorator(RIGHTTRIANGLERIGHT)
    def calculate_validated(self, base_width, height,fail_silently=True,**kwargs):

        super(RightTriangleRight, self).__init__()

        try:
            if not kwargs['validated']:
                raise ValueError("Error during function validation: %s" % kwargs['errorstring'])

            self.centroid['area [m2]'] = 0.5 * base_width * height
            self.centroid['x [m]'] = 2.0 * base_width / 3.0
            self.centroid['y [m]'] = height / 3.0

            self.areamoment_inertia['I_xc [m4]'] = (base_width * height ** 3.0) / 36.0
            self.areamoment_inertia['I_yc [m4]'] = (height * base_width ** 3.0) / 36.0
            self.areamoment_inertia['I_x [m4]'] = (base_width * height ** 3.0) / 12.0
            self.areamoment_inertia['I_y [m4]'] = (height * base_width ** 3.0) / 4.0

            self.radius_gyration['r_xc [m]'] = np.sqrt((height ** 2.0) / 18.0)
            self.radius_gyration['r_yc [m]'] = np.sqrt((base_width ** 2.0) / 18.0)
            self.radius_gyration['r_x [m]'] = np.sqrt((height ** 2.0) / 6.0)
            self.radius_gyration['r_y [m]'] = np.sqrt((base_width ** 2.0) / 2.0)

            self.product_inertia['I_xc_yc [m4]'] = ((base_width ** 2.0) * (height ** 2.0)) / 72.0
            self.product_inertia['I_x_y [m4]'] = ((base_width ** 2.0) * (height ** 2.0)) / 8.0

        except:
            super(RightTriangleRight, self).__init__()

            if fail_silently or fail_silently is None:
                pass
            else:
                raise


RIGHTTRIANGLELEFT = {
    'base_width':{'type': 'float','min_value':0.0,'max_value':None},
    'height':{'type': 'float','min_value':0.0,'max_value':None},
}

class RightTriangleLeft(TwodimensionalShape):
    """
    Represents a right triangle with the right angle on the left (see figure). Derived geometrical properties are calculated when an instance is created

    :param base_width: Width of the triangle base (:math:`b`) [:math:`m`]  - Suggested range: 0.0<=base_width
    :param height: Height of the triangle (:math:`h`) [:math:`m`]  - Suggested range: 0.0<=height

    .. math::
        A = \\frac{b h}{2}

        x_c = \\frac{b}{3}

        y_c = \\frac{h}{3}

        I_{x_c} = \\frac{b h^3}{36}

        I_{y_c} = \\frac{b^3 h}{36}

        I_x = \\frac{b h^3}{12}

        I_y = \\frac{b^3 h}{12}

        r^2_{x_c} = \\frac{h^2}{18}

        r^2_{y_c} = \\frac{b^2}{18}

        r^2_{x} = \\frac{h^2}{6}

        r^2_{y} = \\frac{b^2}{6}

        I_{x_c y_c} = \\frac{- b^2 h^2}{72}

        I_{xy} = \\frac{b^2 h^2}{24}

    .. figure:: images/RightTriangleLeft.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Geometry of a right triangle with right angle on the left

    """

    def __init__(self,base_width, height,fail_silently=True):

        self._base_width = base_width
        self._height = height
        self._fail_silently = fail_silently
        self.calculate()

    @property
    def base_width(self):
        return self._base_width

    @base_width.setter
    def base_width(self, value):
        self._base_width = value
        if value: self.calculate()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        if value: self.calculate()

    @property
    def fail_silently(self):
        return self._fail_silently

    @fail_silently.setter
    def fail_silently(self, value):
        self._fail_silently = value

    def calculate(self):
        self.calculate_validated(self._base_width, self._height, fail_silently=self._fail_silently)

    @ValidationDecorator(RIGHTTRIANGLELEFT)
    def calculate_validated(self, base_width, height, fail_silently=True, **kwargs):

        super(RightTriangleLeft, self).__init__()

        try:
            if not kwargs['validated']:
                raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

            self.centroid['area [m2]'] = 0.5 * base_width * height
            self.centroid['x [m]'] = base_width / 3.0
            self.centroid['y [m]'] = height / 3.0

            self.areamoment_inertia['I_xc [m4]'] = (base_width * height**3.0)/36.0
            self.areamoment_inertia['I_yc [m4]'] = (height * base_width**3.0)/36.0
            self.areamoment_inertia['I_x [m4]'] = (base_width * height**3.0)/12.0
            self.areamoment_inertia['I_y [m4]'] = (height * base_width**3.0)/12.0

            self.radius_gyration['r_xc [m]'] = np.sqrt((height**2.0)/18.0)
            self.radius_gyration['r_yc [m]'] = np.sqrt((base_width**2.0)/18.0)
            self.radius_gyration['r_x [m]'] = np.sqrt((height**2.0)/6.0)
            self.radius_gyration['r_y [m]'] = np.sqrt((base_width**2.0)/6.0)

            self.product_inertia['I_xc_yc [m4]'] = (-(base_width**2.0)*(height**2.0))/72.0
            self.product_inertia['I_x_y [m4]'] = ((base_width**2.0)*(height**2.0))/24.0

        except:
            super(RightTriangleLeft, self).__init__()

            if fail_silently or fail_silently is None:
                pass
            else:
                raise

TRIANGLEGENERIC = {
    'base_full_width':{'type': 'float','min_value':0.0,'max_value':None},
    'height':{'type': 'float','min_value':0.0,'max_value':None},
    'base_offset':{'type': 'float','min_value':0.0,'max_value':None},
}

class TriangleGeneric(TwodimensionalShape):
    """
    Represents a generic triangle with the long edge aligned with the x-axis (see figure). Derived geometrical properties are calculated upon object creation.

    :param base_full_width: Width of the triangle base (:math:`b`) [:math:`m`]  - Suggested range: 0.0<=base_full_width
    :param base_offset: Distance between the origin and the highest vertex, measured along the x-axis (:math:`a`) [:math:`m`] - Suggested range: 0.0<=base_offset<base_full_width
    :param height: Height of the triangle (:math:`h`) [:math:`m`] - Suggested range: 0.0<=height

    .. math::
        A = \\frac{b h}{2}

        x_c = \\frac{a + b}{3}

        y_c = \\frac{h}{3}

        I_{x_c} = \\frac{b h^3}{36}

        I_{y_c} = \\frac{\\left[ b h (b^2 - ab + a^2) \\right]}{36}

        I_x = \\frac{b h^3}{12}

        I_y = \\frac{\\left[ b h (b^2 + ab + a^2) \\right]}{12}

        r^2_{x_c} = \\frac{h^2}{18}

        r^2_{y_c} = \\frac{b^2 - ab + a^2}{18}

        r^2_{x} = \\frac{h^2}{6}

        r^2_{y} = \\frac{b^2 + ab + a^2}{6}

        I_{x_c y_c} = \\frac{b h^2 (2a - b)}{72}

        I_{xy} = \\frac{b h^2 (2a + b)}{24}

    .. figure:: images/TriangleGeneric.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Geometric a a triangle with longest edge aligned with the x-axis

    """

    def __init__(self, base_full_width, base_offset, height, fail_silently=True):

        self._base_full_width = base_full_width
        self._base_offset = base_offset
        self._height = height
        self._fail_silently = fail_silently

        self.calculate()

    @property
    def base_full_width(self):
        return self._base_full_width

    @base_full_width.setter
    def base_full_width(self, value):
        self._base_full_width = value
        if value: self.calculate()

    @property
    def base_offset(self):
        return self._base_offset

    @base_offset.setter
    def base_offset(self, value):
        self._base_offset = value
        if value: self.calculate()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        if value: self.calculate()

    @property
    def fail_silently(self):
        return self._fail_silently

    @fail_silently.setter
    def fail_silently(self, value):
        self._fail_silently = value

    def calculate(self):
        self.calculate_validated(self._base_full_width, self._base_offset, self.height, fail_silently=self._fail_silently)

    @ValidationDecorator(TRIANGLEGENERIC)
    def calculate_validated(self, base_full_width, base_offset, height, fail_silently=True,**kwargs):

        super(TriangleGeneric, self).__init__()

        try:
            if not kwargs['validated']:
                raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

            validate_float('base_offset',base_offset,min_value=0.0,max_value=base_full_width)

            self.centroid['area [m2]'] = 0.5 * base_full_width * height
            self.centroid['x [m]'] = (base_full_width + base_offset) / 3.0
            self.centroid['y [m]'] = height / 3.0

            self.areamoment_inertia['I_xc [m4]'] = (base_full_width * height**3.0)/36.0
            self.areamoment_inertia['I_yc [m4]'] = (height * base_full_width *
                                                    ((base_full_width**2.0) - (base_full_width*base_offset) + (base_offset**2.0)))/36.0
            self.areamoment_inertia['I_x [m4]'] = (base_full_width * height**3.0)/12.0
            self.areamoment_inertia['I_y [m4]'] = (height * base_full_width *
                                                    ((base_full_width**2.0) + (base_full_width*base_offset) + (base_offset**2.0)))/12.0

            self.radius_gyration['r_xc [m]'] = np.sqrt((height**2.0)/18.0)
            self.radius_gyration['r_yc [m]'] = np.sqrt(((base_full_width**2.0) - (base_full_width*base_offset) + (base_offset**2.0))/18.0)
            self.radius_gyration['r_x [m]'] = np.sqrt((height**2.0)/6.0)
            self.radius_gyration['r_y [m]'] = np.sqrt(((base_full_width**2.0) + (base_full_width*base_offset) + (base_offset**2.0))/6.0)

            self.product_inertia['I_xc_yc [m4]'] = (base_full_width*(height**2.0)*(2.0*base_offset - base_full_width))/72.0
            self.product_inertia['I_x_y [m4]'] = (base_full_width*(height**2.0)*(2.0*base_offset + base_full_width))/24.0

        except Exception as err:
            super(TriangleGeneric, self).__init__()

            if fail_silently or fail_silently is None:
                pass
            else:
                raise ValueError(str(err))

RECTANGLE = {
    'base_width':{'type': 'float','min_value':0.0,'max_value':None},
    'height':{'type': 'float','min_value':0.0,'max_value':None},
}

class Rectangle(TwodimensionalShape):
    """
    Represents a rectangle with sides aligned with the x- and y-axes (see figure). Derived geometrical properties are calculated upon object creation.

    :param width: Width of the rectangle (:math:`b`) [:math:`m`]  - Suggested range: 0.0<=width
    :param height: Height of the rectangle (:math:`h`) [:math:`m`]  - Suggested range: 0.0<=height

    .. math::
        A = b h

        x_c = \\frac{b}{2}

        y_c = \\frac{h}{2}

        I_{x_c} = \\frac{b h^3}{12}

        I_{y_c} = \\frac{b^3 h}{12}

        I_x = \\frac{b h^3}{3}

        I_y = \\frac{b^3 h}{3}

        J = \\frac{\\left[ bh (b^2 + h^2) \\right]}{12}

        r^2_{x_c} = \\frac{h^2}{12}

        r^2_{y_c} = \\frac{b^2}{12}

        r^2_{x} = \\frac{h^2}{3}

        r^2_{y} = \\frac{b^2}{3}

        r^2_{p} = \\frac{b^2 + h^2}{12}

        I_{x_c y_c} = 0

        I_{xy} = \\frac{b^2  h^2}{4}

    .. figure:: images/Rectangle.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Geometry of a rectangle

    """

    def __init__(self, base_width, height, fail_silently=True):
        self._base_width = base_width
        self._height = height
        self._fail_silently = fail_silently
        self.calculate()

    @property
    def base_width(self):
        return self._base_width

    @base_width.setter
    def base_width(self, value):
        self._base_width = value
        if value: self.calculate()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        if value: self.calculate()

    @property
    def fail_silently(self):
        return self._fail_silently

    @fail_silently.setter
    def fail_silently(self, value):
        self._fail_silently = value

    def calculate(self):
        self.calculate_validated(self._base_width, self._height, fail_silently=self._fail_silently)

    @ValidationDecorator(RECTANGLE)
    def calculate_validated(self, base_width, height, fail_silently=True, **kwargs):

        super(Rectangle, self).__init__()

        try:
            if not kwargs['validated']:
                raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

            self.centroid['area [m2]'] = base_width * height
            self.centroid['x [m]'] = base_width / 2.0
            self.centroid['y [m]'] = height / 2.0

            self.areamoment_inertia['I_xc [m4]'] = (base_width * height**3.0)/12.0
            self.areamoment_inertia['I_yc [m4]'] = (height * base_width**3.0)/12.0
            self.areamoment_inertia['I_x [m4]'] = (base_width * height**3.0)/3.0
            self.areamoment_inertia['I_y [m4]'] = (height * base_width**3.0)/3.0
            self.areamoment_inertia['J [m4]'] = (base_width*height*((base_width**2.0)+(height**2.0)))/12.0

            self.radius_gyration['r_xc [m]'] = np.sqrt((height**2.0)/12.0)
            self.radius_gyration['r_yc [m]'] = np.sqrt((base_width**2.0)/12.0)
            self.radius_gyration['r_x [m]'] = np.sqrt((height**2.0)/3.0)
            self.radius_gyration['r_y [m]'] = np.sqrt((base_width**2.0)/3.0)
            self.radius_gyration['r_p [m]'] = np.sqrt(((base_width**2.0)+(height**2.0))/12.0)

            self.product_inertia['I_xc_yc [m4]'] = 0.0
            self.product_inertia['I_x_y [m4]'] = ((base_width**2.0)*(height**2.0))/4.0

        except:
            super(Rectangle, self).__init__()

            if fail_silently or fail_silently is None:
                pass
            else:
                raise

TRAPEZOID = {
    'longest_base':{'type': 'float','min_value':0.0,'max_value':None},
    'shortest_base':{'type': 'float','min_value':0.0,'max_value':None},
    'height':{'type': 'float','min_value':0.0,'max_value':None},
}

class Trapezoid(TwodimensionalShape):
    """
    Represents a trapezoid with longest base aligned with the x-axis (see figure). Derived geometrical properties are calculated upon object creation.

    :param longest_base: Length of the longest base (:math:`b`) [:math:`m`]  - Suggested range: 0.0<=longest_base
    :param shortest_base: Length of the shortest base (:math:`a`) [:math:`m`]  - Suggested range: 0.0<=shortest_base<longest_base
    :param height: Height of the trapezoid (:math:`h`) [:math:`m`]  - Suggested range: 0.0<=height

    .. math::
        A = \\frac{h (a+b)}{2}

        y_c = \\frac{h(2a+b)}{3(a+b)}

        I_{x_c} = \\frac{h^3 (a^2 + 4 a b + b^2)}{36 (a + b)}

        I_x = \\frac{h^3 (3a + b)}{12}

        r^2_{x_c} = \\frac{h^2 (a^2 + 4 a b + b^2)}{18 (a + b)}

        r^2_{x} = \\frac{h^2 (3a + b)}{6 (a + b)}

    .. figure:: images/Trapezoid.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Geometry of a trapezoid with longest base aligned with the x-axis

    """

    def __init__(self, longest_base, shortest_base, height, fail_silently=True):
        self._longest_base = longest_base
        self._shortest_base = shortest_base
        self._height = height
        self._fail_silently = fail_silently
        self.calculate()

    @property
    def longest_base(self):
        return self._longest_base

    @longest_base.setter
    def longest_base(self, value):
        self._longest_base = value
        if value: self.calculate()

    @property
    def shortest_base(self):
        return self._shortest_base

    @shortest_base.setter
    def shortest_base(self, value):
        self._shortest_base = value
        if value: self.calculate()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        if value: self.calculate()

    @property
    def fail_silently(self):
        return self._fail_silently

    @fail_silently.setter
    def fail_silently(self, value):
        self._fail_silently = value

    def calculate(self):
        self.calculate_validated(self._longest_base, self._shortest_base, self._height, fail_silently=self._fail_silently)

    @ValidationDecorator(TRAPEZOID)
    def calculate_validated(self, longest_base, shortest_base, height, fail_silently=True, **kwargs):

        super(Trapezoid, self).__init__()

        try:
            if not kwargs['validated']:
                raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

            validate_float('shortest_base',shortest_base,min_value=0.0,max_value=longest_base)


            self.centroid['area [m2]'] = 0.5 * height * (longest_base + shortest_base)
            self.centroid['y [m]'] = (height * (2.0*shortest_base + longest_base))/(3.0*(shortest_base + longest_base))

            self.areamoment_inertia['I_xc [m4]'] = ((height**3.0)*((shortest_base**2.0)+
                                                                   (4.0*shortest_base*longest_base)+
                                                                   (longest_base**2.0)))/(36.0*
                                                                                          (longest_base+shortest_base))
            self.areamoment_inertia['I_x [m4]'] = ((height**3.0)*(3.0*shortest_base + longest_base))/12.0

            self.radius_gyration['r_xc [m]'] = np.sqrt(((height**2.0)*((shortest_base**2.0) +
                                                                       (4.0 * shortest_base * longest_base) +
                                                                       (longest_base**2.0)))/
                                                       (18.0*(longest_base+shortest_base)))
            self.radius_gyration['r_x [m]'] = np.sqrt(((height**2.0)*(3.0*shortest_base + longest_base))/
                                                      (6.0 * (longest_base + shortest_base)))

        except:
            super(Trapezoid, self).__init__()

            if fail_silently or fail_silently is None:
                pass
            else:
                raise

PARALLELLOGRAM = {
    'length_x':{'type': 'float','min_value':0.0,'max_value':None},
    'length_inclined':{'type': 'float','min_value':0.0,'max_value':None},
    'angle':{'type': 'float','min_value':0.0,'max_value':90.0},
}

class Parallellogram(TwodimensionalShape):
    """
    Represents a parallellogram with one side aligned with the x-axis (see figure). Derived geometrical properties are calculated upon object creation.

    :param length_x: Length of the parallellogram side aligned with the x-axis (:math:`b`) [:math:`m`]  - Suggested range: 0.0<=length_x
    :param length_inclined: Length of the inclined side of the parallellogram (:math:`a`) [:math:`m`]  - Suggested range: 0.0<=length_inclined
    :param angle: Angle between the x-axis and the inclined side (:math:`\\theta`) [:math:`deg`]  - Suggested range: 0.0<=angle<=90.0

    .. math::
        A = a b \\sin \\theta

        x_c = \\frac{b + a \\cos \\theta}{2}

        y_c = \\frac{a \\sin \\theta}{2}

        I_{x_c} = \\frac{a^3 b \\sin ^3 \\theta}{12}

        I_{y_c} = \\frac{\\left[ a b \\sin \\theta (b^2 + a^2 \\cos ^2 \\theta) \\right]}{12}

        I_x = \\frac{a^3 b \\sin ^3 \\theta}{3}

        I_y = \\frac{\\left[ a b \\sin \\theta (b^2 + a^2 \\cos ^2 \\theta) \\right]}{3} - \\frac{a^2 b^2 \\sin \\theta \\cos \\theta}{6}

        r^2_{x_c} = \\frac{(a \\sin \\theta)^2}{12}

        r^2_{y_c} = \\frac{b^2 + a^2 \\cos ^2 \\theta}{12}

        r^2_{x} = \\frac{(a \\sin \\theta)^2}{3}

        r^2_{y} = \\frac{(b + a \\cos \\theta)^2}{3} - \\frac{a b \\cos \\theta}{6}

        I_{x_c y_c} = \\frac{a^3 b \\sin ^2 \\theta \\cos \\theta}{12}

    .. figure:: images/Parallellogram.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Geometry of a parallellogram

    """

    def __init__(self, length_x, length_inclined, angle, fail_silently=True):
        self._length_x = length_x
        self._length_inclined = length_inclined
        self._angle = angle
        self._fail_silently = fail_silently
        self.calculate()

    @property
    def length_x(self):
        return self._length_x

    @length_x.setter
    def length_x(self, value):
        self._length_x = value
        if value: self.calculate()

    @property
    def length_inclined(self):
        return self._length_inclined

    @length_inclined.setter
    def length_inclined(self, value):
        self._length_inclined = value
        if value: self.calculate()

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        if value: self.calculate()

    @property
    def fail_silently(self):
        return self._fail_silently

    @fail_silently.setter
    def fail_silently(self, value):
        self._fail_silently = value

    def calculate(self):
        self.calculate_validated(self._length_x, self._length_inclined, self._angle, fail_silently=self._fail_silently)

    @ValidationDecorator(PARALLELLOGRAM)
    def calculate_validated(self, length_x, length_inclined, angle, fail_silently=True, **kwargs):

        super(Parallellogram, self).__init__()

        try:
            if not kwargs['validated']:
                raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

            theta = np.deg2rad(angle)

            self.centroid['area [m2]'] = length_inclined * length_x * np.sin(theta)
            self.centroid['x [m]'] = 0.5 * (length_x + length_inclined * np.cos(theta))
            self.centroid['y [m]'] = 0.5 * length_inclined * np.sin(theta)

            self.areamoment_inertia['I_xc [m4]'] = (length_x * (length_inclined**3.0) * ((np.sin(theta))**3.0))/12.0
            self.areamoment_inertia['I_yc [m4]'] = (length_x*length_inclined*np.sin(theta)*((length_x**2.0)+
                                                                                            ((length_inclined**2.0)*
                                                                                             ((np.cos(theta))**2.0))))/12.0
            self.areamoment_inertia['I_x [m4]'] = (length_x * (length_inclined**3.0) * ((np.sin(theta))**3.0))/3.0
            self.areamoment_inertia['I_y [m4]'] = ((length_x*length_inclined*np.sin(theta)*((length_x**2.0)+
                                                                                            ((length_inclined**2.0)*
                                                                                             ((np.cos(theta))**2.0))))/3.0) - \
                                                  (((length_inclined**2.0)*(length_x**2.0)*np.sin(theta)*np.cos(theta))/6.0)

            self.radius_gyration['r_xc [m]'] = np.sqrt(((length_inclined*np.sin(theta))**2.0)/12.0)
            self.radius_gyration['r_yc [m]'] = np.sqrt(((length_x**2.0)+((length_inclined*np.cos(theta))**2.0))/12.0)
            self.radius_gyration['r_x [m]'] = np.sqrt(((length_inclined*np.sin(theta))**2.0)/3.0)
            self.radius_gyration['r_y [m]'] = np.sqrt((((length_x + length_inclined*np.cos(theta))**2.0)/3.0) -
                                                      ((length_x*length_inclined*np.cos(theta))/6.0))

            self.product_inertia['I_xc_yc [m4]'] = ((length_inclined**3.0)*length_x*((np.sin(theta))**2.0)*(np.cos(theta)))/12.0

        except:
            super(Parallellogram, self).__init__()

            if fail_silently or fail_silently is None:
                pass
            else:
                raise

CIRCLE = {
    'radius':{'type': 'float','min_value':0.0,'max_value':None},
}

class Circle(TwodimensionalShape):
    """
    Represents a circle tangent to the x- and y-axes (see figure). Derived geometrical properties are calculated upon object creation.

    :param radius: Radius (NOT diameter) of the circle (:math:`a`) [:math:`m`]  - Suggested range: 0.0<=radius

    .. math::
        A = \\pi a^2

        x_c = a

        y_c = a

        I_{x_c} = \\frac{\\pi a^4}{4}

        I_{y_c} = \\frac{\\pi a^4}{4}

        I_x = \\frac{5 \\pi a^4}{4}

        I_y = \\frac{5 \\pi a^4}{4}

        J = \\frac{\\pi a^4}{2}

        r^2_{x_c} = \\frac{a^2}{4}

        r^2_{y_c} = \\frac{a^2}{4}

        r^2_{x} = \\frac{5 a^2}{4}

        r^2_{y} = \\frac{5 a^2}{4}

        r^2_{p} = \\frac{a^2}{2}

        I_{x_c y_c} = 0

        I_{xy} = A a^2

    .. figure:: images/Circle.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Geometry of a circle

    """

    def __init__(self, radius, fail_silently=True):
        self._radius = radius
        self._fail_silently = fail_silently
        self.calculate()

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        if value: self.calculate()

    @property
    def fail_silently(self):
        return self._fail_silently

    @fail_silently.setter
    def fail_silently(self, value):
        self._fail_silently = value

    def calculate(self):
        self.calculate_validated(self._radius, fail_silently=self._fail_silently)

    @ValidationDecorator(CIRCLE)
    def calculate_validated(self, radius, fail_silently=True, **kwargs):

        super(Circle, self).__init__()

        try:
            if not kwargs['validated']:
                raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

            self.centroid['area [m2]'] = np.pi * (radius**2.0)
            self.centroid['x [m]'] = radius
            self.centroid['y [m]'] = radius

            self.areamoment_inertia['I_xc [m4]'] = 0.25 * np.pi * (radius**4.0)
            self.areamoment_inertia['I_yc [m4]'] = 0.25 * np.pi * (radius**4.0)
            self.areamoment_inertia['I_x [m4]'] = 0.25 * 5.0 * np.pi * (radius**4.0)
            self.areamoment_inertia['I_y [m4]'] = 0.25 * 5.0 * np.pi * (radius**4.0)
            self.areamoment_inertia['J [m4]'] = 0.5 * np.pi * (radius**4.0)

            self.radius_gyration['r_xc [m]'] = np.sqrt(0.25 * (radius**2.0))
            self.radius_gyration['r_yc [m]'] = np.sqrt(0.25 * (radius**2.0))
            self.radius_gyration['r_x [m]'] = np.sqrt(0.25 * 5.0 * (radius**2.0))
            self.radius_gyration['r_y [m]'] = np.sqrt(0.25 * 5.0 * (radius**2.0))
            self.radius_gyration['r_p [m]'] = np.sqrt(0.5 * (radius**2.0))

            self.product_inertia['I_xc_yc [m4]'] = 0.0
            self.product_inertia['I_x_y [m4]'] = (radius**4.0)* np.pi

        except:
            super(Circle, self).__init__()

            if fail_silently or fail_silently is None:
                pass
            else:
                raise

RING = {
    'outer_radius':{'type': 'float','min_value':0.0,'max_value':None},
    'inner_radius':{'type': 'float','min_value':0.0,'max_value':None},
}

class Ring(TwodimensionalShape):
    """
    Represents a ring tangent to the x- and y-axes (see figure). Derived geometrical properties are calculated upon object creation.

    :param outer_radius: Outer radius of the ring (:math:`a`) [:math:`m`]  - Suggested range: 0.0<=outer_radius
    :param inner_radius: Inner radius of the ring (:math:`b`) [:math:`m`]  - Suggested range: 0.0<=inner_radius

    .. math::
        A = \\pi (a^2 - b^2)

        x_c = a

        y_c = a

        I_{x_c} = \\frac{\\pi (a^4 - b^4)}{4}

        I_{y_c} = \\frac{\\pi (a^4 - b^4)}{4}

        I_x = \\frac{5 \\pi a^4}{4} - \\pi a^2 b^2 - \\frac{\\pi b^4}{4}

        I_y = \\frac{5 \\pi a^4}{4} - \\pi a^2 b^2 - \\frac{\\pi b^4}{4}

        J = \\frac{\\pi (a^4 - b^4)}{2}

        r^2_{x_c} = \\frac{a^2 +  b^2}{4}

        r^2_{y_c} = \\frac{a^2 + b^2}{4}

        r^2_{x} = \\frac{5 a^2 + b^2}{4}

        r^2_{y} = \\frac{5 a^2 + b^2}{4}

        r^2_{p} = \\frac{a^2+ b^2}{2}

        I_{x_c y_c} = 0

        I_{xy} = \\pi a^2 (a^2 - b^2)

    .. figure:: images/Ring.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Geometry of a ring

    """

    def __init__(self, outer_radius, inner_radius, fail_silently=True):
        self._outer_radius = outer_radius
        self._inner_radius = inner_radius
        self._fail_silently = fail_silently
        self.calculate()

    @property
    def outer_radius(self):
        return self._outer_radius

    @outer_radius.setter
    def outer_radius(self, value):
        self._outer_radius = value
        if value: self.calculate()

    @property
    def inner_radius(self):
        return self._inner_radius

    @inner_radius.setter
    def inner_radius(self, value):
        self._inner_radius = value
        if value: self.calculate()

    @property
    def fail_silently(self):
        return self._fail_silently

    @fail_silently.setter
    def fail_silently(self, value):
        self._fail_silently = value

    def calculate(self):
        self.calculate_validated(self._outer_radius, self._inner_radius, fail_silently=self._fail_silently)

    @ValidationDecorator(RING)
    def calculate_validated(self, outer_radius, inner_radius, fail_silently=True, **kwargs):

        super(Ring, self).__init__()

        try:
            if not kwargs['validated']:
                raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

            validate_float('inner_radius', inner_radius, min_value=0.0, max_value=outer_radius)

            self.centroid['area [m2]'] = np.pi * (outer_radius**2.0 - inner_radius**2.0)
            self.centroid['x [m]'] = outer_radius
            self.centroid['y [m]'] = outer_radius

            self.areamoment_inertia['I_xc [m4]'] = 0.25 * np.pi * (outer_radius**4.0 - inner_radius**4.0)
            self.areamoment_inertia['I_yc [m4]'] = 0.25 * np.pi * (outer_radius**4.0 - inner_radius**4.0)
            self.areamoment_inertia['I_x [m4]'] = (0.25 * 5.0 * np.pi * (outer_radius**4.0)) - \
                                                  (np.pi*(outer_radius**2.0)*(inner_radius**2.0)) - \
                                                  (0.25 * np.pi * (inner_radius**4.0))
            self.areamoment_inertia['I_y [m4]'] = (0.25 * 5.0 * np.pi * (outer_radius**4.0)) - \
                                                  (np.pi*(outer_radius**2.0)*(inner_radius**2.0)) - \
                                                  (0.25 * np.pi * (inner_radius**4.0))
            self.areamoment_inertia['J [m4]'] = 0.5 * np.pi * ((outer_radius**4.0) - (inner_radius**4.0))

            self.radius_gyration['r_xc [m]'] = np.sqrt(0.25 * (outer_radius**2.0 + inner_radius**2.0))
            self.radius_gyration['r_yc [m]'] = np.sqrt(0.25 * (outer_radius**2.0 + inner_radius**2.0))
            self.radius_gyration['r_x [m]'] = np.sqrt(0.25 * (5.0 * (outer_radius**2.0) + (inner_radius**2.0)))
            self.radius_gyration['r_y [m]'] = np.sqrt(0.25 * (5.0 * (outer_radius**2.0) + (inner_radius**2.0)))
            self.radius_gyration['r_p [m]'] = np.sqrt(0.5 * (outer_radius**2.0 + inner_radius**2.0))

            self.product_inertia['I_xc_yc [m4]'] = 0.0
            self.product_inertia['I_x_y [m4]'] = np.pi * (outer_radius**2.0) * (outer_radius**2.0 - inner_radius**2.0)

        except:
            super(Ring, self).__init__()

            if fail_silently or fail_silently is None:
                pass
            else:
                raise

SEMICIRCLE = {
    'radius':{'type': 'float','min_value':0.0,'max_value':None},
}

class SemiCircle(TwodimensionalShape):
    """
    Represents a semicircle passing through the origin and with circle center on the x-axis (see figure). Derived geometrical properties are calculated upon object creation.

    :param radius: Radius (NOT diameter) of the semicircle (:math:`a`) [:math:`m`]  - Suggested range: 0.0<=radius

    .. math::
        A = \\frac{\\pi a^2}{2}

        x_c = a

        y_c = \\frac{4 a}{3 \\pi}

        I_{x_c} = \\frac{a^4 (9 \\pi^2 - 64)}{72 \\pi}

        I_{y_c} = \\frac{\\pi a^4}{8}

        I_x = \\frac{\\pi a^4}{8}

        I_y = \\frac{5 \\pi a^4}{8}

        r^2_{x_c} = \\frac{a^2 (9 \\pi^2 - 64)}{36 \\pi^2}

        r^2_{y_c} = \\frac{a^2}{4}

        r^2_{x} = \\frac{a^2}{4}

        r^2_{y} = \\frac{5 a^2}{4}

        I_{x_c y_c} = 0

        I_{xy} = \\frac{2 a^2}{3}

    .. figure:: images/SemiCircle.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Geometry of a semi-circle

    """

    def __init__(self, radius, fail_silently=True):
        self._radius = radius
        self._fail_silently = fail_silently
        self.calculate()

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        if value: self.calculate()

    @property
    def fail_silently(self):
        return self._fail_silently

    @fail_silently.setter
    def fail_silently(self, value):
        self._fail_silently = value

    def calculate(self):
        self.calculate_validated(self._radius, fail_silently=self._fail_silently)

    @ValidationDecorator(SEMICIRCLE)
    def calculate_validated(self, radius, fail_silently=True, **kwargs):

        super(SemiCircle, self).__init__()

        try:
            if not kwargs['validated']:
                raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

            self.centroid['area [m2]'] = 0.5 * np.pi * (radius**2.0)
            self.centroid['x [m]'] = radius
            self.centroid['y [m]'] = (4.0 * radius)/(3.0 * np.pi)

            self.areamoment_inertia['I_xc [m4]'] = ((radius**4.0)*(9.0*(np.pi**2.0) - 64.0))/(72.0 * np.pi)
            self.areamoment_inertia['I_yc [m4]'] = 0.125 * np.pi * (radius**4.0)
            self.areamoment_inertia['I_x [m4]'] = 0.125 * np.pi * (radius**4.0)
            self.areamoment_inertia['I_y [m4]'] = 0.125 * 5.0 * np.pi * (radius**4.0)

            self.radius_gyration['r_xc [m]'] = np.sqrt(((radius**2.0)*(9.0*(np.pi**2.0) - 64.0))/(36.0 * (np.pi**2.0)))
            self.radius_gyration['r_yc [m]'] = np.sqrt(0.25 * (radius**2.0))
            self.radius_gyration['r_x [m]'] = np.sqrt(0.25 * (radius**2.0))
            self.radius_gyration['r_y [m]'] = np.sqrt(0.25 * 5.0 * (radius**2.0))

            self.product_inertia['I_xc_yc [m4]'] = 0.0
            self.product_inertia['I_x_y [m4]'] = (2.0 * (radius**2.0)/ 3.0)

        except:
            super(SemiCircle, self).__init__()

            if fail_silently or fail_silently is None:
                pass
            else:
                raise

CIRCLESECTOR = {
    'radius':{'type': 'float','min_value':0.0,'max_value':None},
    'angle':{'type': 'float','min_value':0.0,'max_value':90.0},
}

class CircleSector(TwodimensionalShape):
    """
    Represents a circle sector divided in two by the x-axis and with circle center at the origin (see figure). Derived geometrical properties are calculated upon object creation.

    :param radius: Radius of the circle sector (:math:`a`) [:math:`m`]  - Suggested range: 0.0<=radius
    :param angle: Absolute value of the angle between the x-axis and the edge of the circle sector (:math:`\\theta`) [:math:`deg`]  - Suggested range: 0.0<=angle<=90.0

    .. math::
        A = a^2 \\theta

        x_c = \\frac{2 a}{3} \\frac{\\sin \\theta}{\\theta}

        y_c = 0

        I_x = \\frac{a^4 (\\theta - \\sin \\theta \\cos \\theta)}{4}

        I_y = \\frac{a^4 (\\theta + \\sin \\theta \\cos \\theta)}{4}

        r^2_{x} = \\frac{a^2}{4} \\frac{\\theta - \\sin \\theta \\cos \\theta}{\\theta}

        r^2_{y} = \\frac{a^2}{4} \\frac{\\theta + \\sin \\theta \\cos \\theta}{\\theta}

        I_{x_c y_c} = 0

        I_{xy} = 0

    .. figure:: images/CircleSector.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Geometry of a circle sector

    """

    def __init__(self, radius, angle, fail_silently=True):
        self._radius = radius
        self._angle = angle
        self._fail_silently = fail_silently
        self.calculate()

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        if value: self.calculate()

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        if value: self.calculate()

    @property
    def fail_silently(self):
        return self._fail_silently

    @fail_silently.setter
    def fail_silently(self, value):
        self._fail_silently = value

    def calculate(self):
        self.calculate_validated(self._radius, self._angle, fail_silently=self._fail_silently)

    @ValidationDecorator(CIRCLESECTOR)
    def calculate_validated(self, radius, angle, fail_silently=True, **kwargs):

        super(CircleSector, self).__init__()

        try:
            if not kwargs['validated']:
                raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

            theta = np.deg2rad(angle)

            self.centroid['area [m2]'] = (radius**2.0) * theta
            self.centroid['x [m]'] = (2.0 * radius * np.sin(theta))/(3.0 * theta)
            self.centroid['y [m]'] = 0.0

            self.areamoment_inertia['I_x [m4]'] = 0.25 * (radius**4.0) * (theta - np.sin(theta)*np.cos(theta))
            self.areamoment_inertia['I_y [m4]'] = 0.25 * (radius**4.0) * (theta + np.sin(theta)*np.cos(theta))

            self.radius_gyration['r_x [m]'] = np.sqrt(0.25 * (radius**2.0) * ((theta - np.sin(theta)*np.cos(theta))/(theta)))
            self.radius_gyration['r_y [m]'] = np.sqrt(0.25 * (radius**2.0) * ((theta + np.sin(theta)*np.cos(theta))/(theta)))

            self.product_inertia['I_xc_yc [m4]'] = 0.0
            self.product_inertia['I_x_y [m4]'] = 0.0

        except:
            super(CircleSector, self).__init__()

            if fail_silently or fail_silently is None:
                pass
            else:
                raise

CIRCLESEGMENT = {
    'radius':{'type': 'float','min_value':0.0,'max_value':None},
    'angle':{'type': 'float','min_value':0.0,'max_value':90.0},
}
class CircleSegment(TwodimensionalShape):
    """
    Represents a circle segment divided in two by the x-axis and with circle center at the origin (see figure). Derived geometrical properties are calculated upon object creation.

    :param radius: Radius of the circle segment (:math:`a`) [:math:`m`]  - Suggested range: 0.0<=radius
    :param angle: Absolute value of the angle between the x-axis and the edge of the circle sector (:math:`\\theta`) [:math:`deg`]  - Suggested range: 0.0<=angle<=90.0

    .. math::
        A = a^2 \\left( \\theta - \\frac{\\sin (2 \\theta)}{2} \\right)

        x_c = \\frac{2 a}{3} \\frac{\\sin ^3 \\theta}{\\theta - \\sin \\theta \\cos \\theta}

        y_c = 0

        I_x = \\frac{A a^2}{4} \\left[ 1 - \\frac{2 \\sin ^3 \\theta \\cos \\theta}{3 \\theta - 3 \\sin \\theta \\cos \\theta} \\right]

        I_y = \\frac{A a^2}{4} \\left[ 1 + \\frac{2 \\sin ^3 \\theta \\cos \\theta}{\\theta - \\sin \\theta \\cos \\theta} \\right]

        r^2_{x} = \\frac{a^2}{4} \\left[ 1 - \\frac{2 \\sin ^3 \\theta \\cos \\theta}{3 \\theta - 3 \\sin \\theta \\cos \\theta} \\right]

        r^2_{y} = \\frac{a^2}{4} \\left[ 1 + \\frac{2 \\sin ^3 \\theta \\cos \\theta}{\\theta - \\sin \\theta \\cos \\theta} \\right]

        I_{x_c y_c} = 0

        I_{xy} = A a^2

    .. figure:: images/CircleSegment.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Geometry of a circle segment

    """

    def __init__(self, radius, angle, fail_silently=True):
        self._radius = radius
        self._angle = angle
        self._fail_silently = fail_silently
        self.calculate()

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        if value: self.calculate()

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        if value: self.calculate()

    @property
    def fail_silently(self):
        return self._fail_silently

    @fail_silently.setter
    def fail_silently(self, value):
        self._fail_silently = value

    def calculate(self):
        self.calculate_validated(self._radius, self._angle, fail_silently=self._fail_silently)

    @ValidationDecorator(CIRCLESEGMENT)
    def calculate_validated(self, radius, angle, fail_silently=True, **kwargs):

        super(CircleSegment, self).__init__()

        try:
            if not kwargs['validated']:
                raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

            theta = np.deg2rad(angle)

            self.centroid['area [m2]'] = (radius**2.0) * (theta - (0.5 * np.sin(2.0 * theta)))
            self.centroid['x [m]'] = (2.0 * radius * (np.sin(theta)**3.0))/(3.0 * (theta - np.sin(theta)*np.cos(theta)))
            self.centroid['y [m]'] = 0.0

            self.areamoment_inertia['I_x [m4]'] = 0.25 * self.centroid['area [m2]'] * (radius**2.0) * \
                                                  (1.0 - ((2.0 * (np.sin(theta)**3.0) * np.cos(theta))/
                                                          (3.0*theta - 3.0 * np.sin(theta) * np.cos(theta))))
            self.areamoment_inertia['I_y [m4]'] = 0.25 * self.centroid['area [m2]'] * (radius**2.0) * \
                                                  (1.0 + ((2.0 * (np.sin(theta)**3.0) * np.cos(theta))/
                                                          (theta - np.sin(theta) * np.cos(theta))))

            self.radius_gyration['r_x [m]'] = np.sqrt(0.25 * (radius**2.0) * \
                                                  (1.0 - ((2.0 * (np.sin(theta)**3.0) * np.cos(theta))/
                                                          (3.0*theta - 3.0 * np.sin(theta) * np.cos(theta)))))
            self.radius_gyration['r_y [m]'] = np.sqrt(0.25 * self.centroid['area [m2]'] * (radius**2.0) * \
                                                  (1.0 + ((2.0 * (np.sin(theta)**3.0) * np.cos(theta))/
                                                          (theta - np.sin(theta) * np.cos(theta)))))
            self.product_inertia['I_xc_yc [m4]'] = 0.0
            self.product_inertia['I_x_y [m4]'] = 0.0

        except:
            super(CircleSegment, self).__init__()

            if fail_silently or fail_silently is None:
                pass
            else:
                raise

PARABOLA = {
    'width':{'type': 'float','min_value':0.0,'max_value':None},
    'height':{'type': 'float','min_value':0.0,'max_value':None},
}

class Parabola(TwodimensionalShape):
    """
    Represents a parabola divided in two by the x-axis (see figure). Derived geometrical properties are calculated upon object creation.

    :param width: Offset between the origin and the edge of the parabola (:math:`a`) [:math:`m`]  - Suggested range: 0.0<=width
    :param height: Height of the parabola measured from the x-axis to the intersection with the parabola (:math:`b`) [:math:`m`]  - Suggested range: 0.0<=height

    .. math::
        A = \\frac{4 a b}{3}

        x_c = \\frac{3 a}{5}

        y_c = 0

        I_{x_c} = \\frac{4 a b^3}{15}

        I_{y_c} = \\frac{16 a^3 b}{175}

        I_x = \\frac{4 a b^3}{15}

        I_y = \\frac{4 a^3 b}{7}

        r^2_{x_c} = \\frac{b^2}{5}

        r^2_{y_c} = \\frac{12 a^2}{175}

        r^2_{x} = \\frac{b^2}{5}

        r^2_{y} = \\frac{3 a^2}{7}

        I_{x_c y_c} = 0

        I_{xy} = 0

    .. figure:: images/Parabola.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Geometry of a parabola

    """

    def __init__(self, width, height, fail_silently=True):
        self._width = width
        self._height = height
        self._fail_silently = fail_silently
        self.calculate()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        if value: self.calculate()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        if value: self.calculate()

    @property
    def fail_silently(self):
        return self._fail_silently

    @fail_silently.setter
    def fail_silently(self, value):
        self._fail_silently = value

    def calculate(self):
        self.calculate_validated(self._width, self._height, fail_silently=self._fail_silently)

    @ValidationDecorator(PARABOLA)
    def calculate_validated(self, width, height, fail_silently=True, **kwargs):

        super(Parabola, self).__init__()

        try:
            if not kwargs['validated']:
                raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

            self.centroid['area [m2]'] = (4.0 * width * height) / 3.0
            self.centroid['x [m]'] = (3.0 * width) / 5.0
            self.centroid['y [m]'] = 0.0

            self.areamoment_inertia['I_xc [m4]'] = (4.0 * width * (height**3.0)) / 15.0
            self.areamoment_inertia['I_yc [m4]'] = (16.0 * (width**3.0) * height) / 175.0
            self.areamoment_inertia['I_x [m4]'] = (4.0 * width * (height**3.0)) / 15.0
            self.areamoment_inertia['I_y [m4]'] = (4.0 * (width**3.0) * height) / 7.0

            self.radius_gyration['r_xc [m]'] = np.sqrt((height**2.0)/5.0)
            self.radius_gyration['r_yc [m]'] = np.sqrt((12.0 * (width**2.0))/175.0)
            self.radius_gyration['r_x [m]'] = np.sqrt((height**2.0)/5.0)
            self.radius_gyration['r_y [m]'] = np.sqrt((3.0 * (width**2.0))/7.0)

            self.product_inertia['I_xc_yc [m4]'] = 0.0
            self.product_inertia['I_x_y [m4]'] = 0.0

        except:
            super(Parabola, self).__init__()

            if fail_silently or fail_silently is None:
                pass
            else:
                raise

HALFPARABOLA = {
    'width':{'type': 'float','min_value':0.0,'max_value':None},
    'height':{'type': 'float','min_value':0.0,'max_value':None},
}

class HalfParabola(TwodimensionalShape):
    """
    Represents one half of a parabola, the proportion above the x-axis (see figure). Derived geometrical properties are calculated upon object creation.

    :param width: Offset between the origin and the edge of the shape, measured along the x-axis (:math:`a`) [:math:`m`]  - Suggested range: 0.0<=width
    :param height: Height of the parabola measured from the x-axis to the parabola curve (:math:`b`) [:math:`m`]  - Suggested range: 0.0<=height

    .. math::
        A = \\frac{2 a b}{3}

        x_c = \\frac{3 a}{5}

        y_c = \\frac{3 b}{8}

        I_x = \\frac{2 a b^3}{15}

        I_y = \\frac{2 a^3 b}{7}

        r^2_{x} = \\frac{b^2}{5}

        r^2_{y} = \\frac{3 a^2}{7}

    .. figure:: images/HalfParabola.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Geometry of half a parabola

    """

    def __init__(self, width, height, fail_silently=True):
        self._width = width
        self._height = height
        self._fail_silently = fail_silently
        self.calculate()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        if value: self.calculate()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        if value: self.calculate()

    @property
    def fail_silently(self):
        return self._fail_silently

    @fail_silently.setter
    def fail_silently(self, value):
        self._fail_silently = value

    def calculate(self):
        self.calculate_validated(self._width, self._height, fail_silently=self._fail_silently)

    @ValidationDecorator(HALFPARABOLA)
    def calculate_validated(self, width, height, fail_silently=True, **kwargs):

        super(HalfParabola, self).__init__()

        try:
            if not kwargs['validated']:
                raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

            self.centroid['area [m2]'] = (2.0 * width * height) / 3.0
            self.centroid['x [m]'] = (3.0 * width) / 5.0
            self.centroid['y [m]'] = (3.0 * height) / 8.0

            self.areamoment_inertia['I_x [m4]'] = (2.0 * width * (height**3.0)) / 15.0
            self.areamoment_inertia['I_y [m4]'] = (2.0 * (width**3.0) * height) / 7.0

            self.radius_gyration['r_x [m]'] = np.sqrt((height**2.0)/5.0)
            self.radius_gyration['r_y [m]'] = np.sqrt((3.0 * (width**2.0))/7.0)

        except:
            super(HalfParabola, self).__init__()

            if fail_silently or fail_silently is None:
                pass
            else:
                raise

NDEGREEPARABOLAOUTSIDE = {
    'width':{'type': 'float','min_value':0.0,'max_value':None},
    'height':{'type': 'float','min_value':0.0,'max_value':None},
    'exponent':{'type': 'float','min_value':0.0,'max_value':None},
}

class NDegreeParabolaOutside(TwodimensionalShape):
    """
    Represents the outside of an Nth degree parabola, positioned above the x-axis (see figure). Derived geometrical properties are calculated upon object creation.

    :param width: Width of the Nth degree parabola measured along the x-axis (:math:`b`) [:math:`m`]  - Suggested range: 0.0<=width
    :param height: Height of the Nth degree parabola (:math:`h`) [:math:`m`]  - Suggested range: 0.0<=height
    :param exponent: Exponent of the Nth degree parabola (:math:`n`) [:math:`-`]  - Suggested range: 0.0<=exponent

    .. math::
        A = \\frac{b h}{n + 1}

        x_c = \\frac{n + 1}{n + 2} b

        y_c = \\frac{h}{2} \\frac{n + 1}{2n + 1}

        I_x = \\frac{b h^3}{3 (3n + 1)}

        I_y = \\frac{h b^3}{n + 3}

        r^2_{x} = \\frac{h^2 (n + 1)}{3 (3n + 1)}

        r^2_{y} = \\frac{n + 1}{n + 3} b^2

        y = \\frac{h}{b^n} x^n

    .. figure:: images/NDegreeParabolaOutside.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Geometry of the outside of an Nth degree parabola

    """

    def __init__(self, width, height, exponent, fail_silently=True):
        self._width = width
        self._height = height
        self._exponent = exponent
        self._fail_silently = fail_silently
        self.calculate()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        if value: self.calculate()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        if value: self.calculate()

    @property
    def exponent(self):
        return self._exponent

    @exponent.setter
    def exponent(self, value):
        self._exponent = value
        if value: self.calculate()

    @property
    def fail_silently(self):
        return self._fail_silently

    @fail_silently.setter
    def fail_silently(self, value):
        self._fail_silently = value

    def calculate(self):
        self.calculate_validated(self._width, self._height, self._exponent, fail_silently=self._fail_silently)

    @ValidationDecorator(NDEGREEPARABOLAOUTSIDE)
    def calculate_validated(self, width, height, exponent, fail_silently=True, **kwargs):

        super(NDegreeParabolaOutside, self).__init__()

        try:
            if not kwargs['validated']:
                raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

            self.centroid['area [m2]'] = (width * height) / (exponent + 1.0)
            self.centroid['x [m]'] = width * ((exponent + 1.0) / (exponent + 2.0))
            self.centroid['y [m]'] = 0.5 * height *((exponent + 1.0)/(2.0 * exponent + 1.0))

            self.areamoment_inertia['I_x [m4]'] = (width * (height**3.0))/(3.0 * (3.0 * exponent + 1.0))
            self.areamoment_inertia['I_y [m4]'] = (height * (width**3.0))/(exponent + 3.0)

            self.radius_gyration['r_x [m]'] = np.sqrt(((height**2.0)*(exponent + 1.0))/(3.0 * (3.0 * exponent + 1.0)))
            self.radius_gyration['r_y [m]'] = np.sqrt((width**2.0)*((exponent + 1.0)/(exponent + 3.0)))

        except:
            super(NDegreeParabolaOutside, self).__init__()

            if fail_silently or fail_silently is None:
                pass
            else:
                raise

NDEGREEPARABOLAINSIDE = {
    'width':{'type': 'float','min_value':0.0,'max_value':None},
    'height':{'type': 'float','min_value':0.0,'max_value':None},
    'exponent':{'type': 'float','min_value':0.0,'max_value':None},
}

class NDegreeParabolaInside(TwodimensionalShape):
    """
    Represents the inside of an Nth degree parabola, positioned above the x-axis (see figure). Derived geometrical properties are calculated upon object creation.

    :param width: Width of the Nth degree parabola measured along the x-axis (:math:`b`) [:math:`m`]  - Suggested range: 0.0<=width
    :param height: Height of the Nth degree parabola (:math:`h`) [:math:`m`]  - Suggested range: 0.0<=height
    :param exponent: Exponent of the Nth degree parabola (:math:`n`) [:math:`-`]  - Suggested range: 0.0<=exponent

    .. math::
        A = \\frac{n}{n + 1} b h

        x_c = \\frac{n + 1}{2n + 1} b

        y_c = \\frac{n + 1}{2 (n + 2)} h

        I_x = \\frac{n}{3 (n + 3)} b h^3

        I_y = \\frac{n}{3n + 1} b^3 h

        r^2_{x} = \\frac{n + 1}{3 (n + 1)} h^2

        r^2_{y} = \\frac{n + 1}{3n + 1} b^2

        y = \\frac{h}{b^{1/n}} x^{1/n}

    .. figure:: images/NDegreeParabolaInside.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Geometry of the inside of the Nth degree parabola

    """

    def __init__(self, width, height, exponent, fail_silently=True):
        self._width = width
        self._height = height
        self._exponent = exponent
        self._fail_silently = fail_silently
        self.calculate()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        if value: self.calculate()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        if value: self.calculate()

    @property
    def exponent(self):
        return self._exponent

    @exponent.setter
    def exponent(self, value):
        self._exponent = value
        if value: self.calculate()

    @property
    def fail_silently(self):
        return self._fail_silently

    @fail_silently.setter
    def fail_silently(self, value):
        self._fail_silently = value

    def calculate(self):
        self.calculate_validated(self._width, self._height, self._exponent, fail_silently=self._fail_silently)

    @ValidationDecorator(NDEGREEPARABOLAINSIDE)
    def calculate_validated(self, width, height, exponent, fail_silently=True, **kwargs):

        super(NDegreeParabolaInside, self).__init__()

        try:
            if not kwargs['validated']:
                raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

            self.centroid['area [m2]'] = ((exponent) / (exponent + 1.0)) * (width * height)
            self.centroid['x [m]'] = width * ((exponent + 1.0) / (2.0 * exponent + 1.0))
            self.centroid['y [m]'] = height *((exponent + 1.0)/(2.0 * (exponent + 2.0)))

            self.areamoment_inertia['I_x [m4]'] = (width * (height**3.0)) * (exponent / (3.0 * (exponent + 3.0)))
            self.areamoment_inertia['I_y [m4]'] = (height * (width**3.0)) * (exponent / (3.0 * exponent + 1.0))

            self.radius_gyration['r_x [m]'] = np.sqrt((height**2.0)*((exponent + 1.0))/(3.0 * (exponent + 1.0)))
            self.radius_gyration['r_y [m]'] = np.sqrt((width**2.0)*((exponent + 1.0)/(3.0 * exponent + 1.0)))

        except:
            super(NDegreeParabolaInside, self).__init__()

            if fail_silently or fail_silently is None:
                pass
            else:
                raise