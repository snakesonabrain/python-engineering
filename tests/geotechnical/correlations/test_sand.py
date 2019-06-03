#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

# Django and native Python packages
import unittest

# 3rd party packages

# Project imports
from pyeng.geotechnical.correlations import sand


class Test_friction_angle_kleven(unittest.TestCase):
    
    def test_values(self):
        self.assertEqual(sand.frictionangle_overburden_kleven(10.0,100.0,Ko=1.0,max_friction_angle=50.0)['phi [deg]'],47.497)
        self.assertEqual(sand.frictionangle_overburden_kleven(10.0,100.0,Ko=1.0,)['phi [deg]'],45.0)
        
    def test_ranges(self):
        self.assertRaises(ValueError,sand.frictionangle_overburden_kleven,1.0,100.0,Ko=0.6,fail_silently=False)


class Test_lateralearthpressure_relativedensity_bellotti(unittest.TestCase):

    def test_values(self):
        self.assertAlmostEqual(sand.lateralearthpressure_relativedensity_bellotti(50.0)['Ko [-]'], 0.46, 2)


class Test_gmax_cptsand_lunne(unittest.TestCase):

    def test_values(self):
        self.assertAlmostEqual(
            sand.gmax_cptsand_lunne(cone_resistance=10.0, sigma_vo_eff=100.0)['Gmax [kPa]'], 91886.6, 1)


class Test_permeability_grainsize_chapuis(unittest.TestCase):

    def test_values(self):
        self.assertAlmostEqual(
            sand.permeability_grainsize_chapuis(void_ratio=0.4, d10=0.6)['k [m/s]'], 0.001, 4)

