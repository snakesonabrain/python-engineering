#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

import unittest
import numpy as np
import math
from pyeng.general.geometry import geom_2d


class Test_RighttriangleRight(unittest.TestCase):

    def setUp(self):
        self.shape = geom_2d.RightTriangleRight(1.0,1.0)

    def test_values(self):
        self.assertEqual(self.shape.centroid['area [m2]'],0.5)
        self.shape.base_width = 2.0
        self.assertEqual(self.shape.centroid['area [m2]'], 1.0)

    def test_error(self):
        self.assertRaises(ValueError,geom_2d.RightTriangleRight,-1.0,1.0,fail_silently=False)

    def test_error_after_modification(self):
        # Check that silent failures work as expected
        self.shape.base_width = -1.0
        self.assertEqual(math.isnan(self.shape.centroid['area [m2]']),True)
        # Check that explicit failure work as expected
        self.shape.fail_silently=False
        try:
            self.shape.base_width=-1.0
            exception_raised = False
        except:
            exception_raised = True
        self.assertEqual(exception_raised,True)


class Test_RightTriangleLeft(unittest.TestCase):

    def setUp(self):
        self.shape = geom_2d.RightTriangleLeft(1.0, 1.0)

    def test_values(self):
        self.assertEqual(self.shape.areamoment_inertia['I_xc [m4]'],(1.0/36.0))


class Test_GenericTriangle(unittest.TestCase):

    def setUp(self):
        self.shape = geom_2d.TriangleGeneric(1.0, 0.5, 1.0)

    def test_values(self):
        self.assertAlmostEqual(self.shape.radius_gyration['r_yc [m]'],0.204124,5)

    def test_error(self):
        self.assertRaises(ValueError,geom_2d.TriangleGeneric,1.0,2.0,1.0,fail_silently=False)


class Test_Rectangle(unittest.TestCase):

    def setUp(self):
        self.shape = geom_2d.Rectangle(0.5,1.0)

    def test_values(self):
        self.assertEqual(self.shape.product_inertia['I_xc_yc [m4]'],0.0)


class Test_Trapezoid(unittest.TestCase):

    def setUp(self):
        self.shape = geom_2d.Trapezoid(1.0,0.5,1.0)

    def test_values(self):
        self.assertAlmostEqual(self.shape.areamoment_inertia['I_xc [m4]'],0.060185,6)


class Test_Parallellogram(unittest.TestCase):

    def setUp(self):
        self.shape = geom_2d.Parallellogram(1.0,0.5,45.0)

    def test_values(self):
        self.assertAlmostEqual(self.shape.radius_gyration['r_y [m]'],0.7428,4)


class Test_Circle(unittest.TestCase):

    def setUp(self):
        self.shape = geom_2d.Circle(1.0)

    def test_values(self):
        self.assertAlmostEqual(self.shape.radius_gyration['r_y [m]'],1.118,3)


class Test_Ring(unittest.TestCase):

    def setUp(self):
        self.shape = geom_2d.Ring(outer_radius=1.0, inner_radius=0.5)

    def test_values(self):
        self.assertAlmostEqual(self.shape.areamoment_inertia['I_y [m4]'],3.0925,4)


class Test_SemiCircle(unittest.TestCase):

    def setUp(self):
        self.shape = geom_2d.SemiCircle(radius=1.0)

    def test_values(self):
        self.assertAlmostEqual(self.shape.areamoment_inertia['I_xc [m4]'],0.1098,4)
        self.assertAlmostEqual(self.shape.radius_gyration['r_xc [m]'],0.2643,4)


class Test_CircleSector(unittest.TestCase):

    def setUp(self):
        self.shape = geom_2d.CircleSector(radius=1.0,angle=30.0)

    def test_values(self):
        self.assertAlmostEqual(self.shape.areamoment_inertia['I_y [m4]'],0.2392,4)
        self.assertAlmostEqual(self.shape.radius_gyration['r_x [m]'],0.2080,4)


class Test_CircleSegment(unittest.TestCase):

    def setUp(self):
        self.shape = geom_2d.CircleSegment(radius=1.0,angle=30.0)

    def test_values(self):
        self.assertAlmostEqual(self.shape.areamoment_inertia['I_y [m4]'],0.0768,4)
        self.assertAlmostEqual(self.shape.radius_gyration['r_x [m]'],0.2255,4)


class Test_Parabola(unittest.TestCase):

    def setUp(self):
        self.shape = geom_2d.Parabola(width=1.0,height=0.5)

    def test_values(self):
        self.assertAlmostEqual(self.shape.areamoment_inertia['I_y [m4]'],0.2857,4)
        self.assertAlmostEqual(self.shape.radius_gyration['r_x [m]'],0.2236,4)


class Test_HalfParabola(unittest.TestCase):

    def setUp(self):
        self.shape = geom_2d.HalfParabola(width=1.0,height=0.5)

    def test_values(self):
        self.assertAlmostEqual(self.shape.areamoment_inertia['I_y [m4]'],0.1429,4)
        self.assertAlmostEqual(self.shape.radius_gyration['r_x [m]'],0.2236,4)


class Test_NDegreeParabolaOutside(unittest.TestCase):

    def setUp(self):
        self.shape = geom_2d.NDegreeParabolaOutside(width=1.0,height=0.5,exponent=3.0)

    def test_values(self):
        self.assertAlmostEqual(self.shape.areamoment_inertia['I_y [m4]'],0.0833,4)
        self.assertAlmostEqual(self.shape.radius_gyration['r_x [m]'],0.1826,4)


class Test_NDegreeParabolaInside(unittest.TestCase):

    def setUp(self):
        self.shape = geom_2d.NDegreeParabolaInside(width=1.0,height=0.5,exponent=3.0)

    def test_values(self):
        self.assertEqual(self.shape.areamoment_inertia['I_y [m4]'],0.15)
        self.assertAlmostEqual(self.shape.radius_gyration['r_x [m]'],0.2887,4)