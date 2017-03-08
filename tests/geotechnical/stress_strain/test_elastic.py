#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

import unittest
from pyeng.geotechnical.stress_strain import elastic

class Test_stresses_pointload_boussinesq(unittest.TestCase):
    def test_values(self):
        self.assertAlmostEqual(
            elastic.stresses_pointload_boussinesq(100.0,
                                                  0.0,
                                                  0.0,
                                                  1.0)['sigma_z [kPa]'],
            47.75, 2)


class Test_stresses_lineload_boussinesq(unittest.TestCase):
    def test_values(self):
        self.assertAlmostEqual(elastic.stresses_lineload_boussinesq(1.0, 1.0, 1.0)['sigma_z [kPa]'], 0.159, 3)
        self.assertAlmostEqual(elastic.stresses_lineload_boussinesq(1.0, 1.0, 1.0)['sigma_x [kPa]'], 0.159, 3)
        self.assertAlmostEqual(elastic.stresses_lineload_boussinesq(1.0, 1.0, 1.0)['tau_zx [kPa]'], 0.159, 3)



class Test_stresses_striploadconstant_boussinesq(unittest.TestCase):
    def test_values(self):
        self.assertAlmostEqual(elastic.stresses_striploadconstant_boussinesq(1.0, 1.0, 0.0, 1.0)['sigma_z [kPa]'],
                               0.409, 3)
        self.assertAlmostEqual(elastic.stresses_striploadconstant_boussinesq(1.0, 1.0, 0.0, 1.0)['sigma_x [kPa]'],
                               0.091, 3)
        self.assertAlmostEqual(elastic.stresses_striploadconstant_boussinesq(1.0, 1.0, 0.0, 1.0)['tau_zx [kPa]'],
                               -0.159, 3)

# Unit test

class Test_stresses_striploadtriangular_boussinesq(unittest.TestCase):
    def test_values(self):
        self.assertAlmostEqual(
            elastic.stresses_striploadtriangular_boussinesq(1.0, 1.0, 0.0, 1.0)['sigma_z [kPa]'],
            0.159, 3)
        self.assertAlmostEqual(
            elastic.stresses_striploadtriangular_boussinesq(1.0, 1.0, 0.0, 1.0)['sigma_x [kPa]'],
            0.061, 3)
        self.assertAlmostEqual(
            elastic.stresses_striploadtriangular_boussinesq(1.0, 1.0, 0.0, 1.0)['tau_zx [kPa]'],
            -0.091, 3)


class Test_stresses_circle_boussinesq(unittest.TestCase):
    def test_values(self):
        self.assertAlmostEqual(elastic.stresses_circle_boussinesq(1.0, 1.0, 1.0,)['sigma_z [kPa]'], 0.646, 3)
        self.assertAlmostEqual(elastic.stresses_circle_boussinesq(1.0, 1.0, 1.0, )['sigma_r [kPa]'], -0.862, 3)


class Test_stresses_rectangle_boussinesq(unittest.TestCase):
    def test_values(self):
        self.assertAlmostEqual(
            elastic.stresses_rectangle_boussinesq(1.0, 1.0, 0.5, 1.0)['sigma_z [kPa]'], 0.1202, 4)
        self.assertAlmostEqual(
            elastic.stresses_rectangle_boussinesq(1.0, 1.0, 0.5, 1.0)['sigma_x [kPa]'], 0.0247, 4)
        self.assertAlmostEqual(
            elastic.stresses_rectangle_boussinesq(1.0, 1.0, 0.5, 1.0)['sigma_y [kPa]'], 0.0088, 4)
        self.assertAlmostEqual(
            elastic.stresses_rectangle_boussinesq(1.0, 1.0, 0.5, 1.0)['tau_zx [kPa]'], 0.0447, 4)

    def test_errors(self):
        self.assertRaises(ValueError, elastic.stresses_rectangle_boussinesq, 1.0, 0.5,
                          1.0, 1.0, fail_silently=False)