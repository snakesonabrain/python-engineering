#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

# Django and native Python packages
import unittest

# 3rd party packages

# Project imports
from pyeng.geotechnical.correlations import clay


class Test_lateralearthpressure_plasticity_massarsch(unittest.TestCase):
    def test_values(self):
        self.assertAlmostEqual(clay.lateralearthpressure_plasticity_massarsch(50.0)['Ko [-]'], 0.65,2)


class Test_secondarycompressionratio_watercontent_mesri(unittest.TestCase):
    def test_values(self):
        self.assertAlmostEqual(
            clay.secondarycompressionratio_watercontent_mesri(77.8)['secondary_compression_ratio [%]'],
            0.80, 1)
        self.assertAlmostEqual(
            clay.secondarycompressionratio_watercontent_mesri(56.1)['secondary_compression_ratio [%]'],
            0.57, 1)
        self.assertAlmostEqual(
            clay.secondarycompressionratio_watercontent_mesri(811.0)['secondary_compression_ratio [%]'],
            8.38, 2)


class Test_gmax_cptclay_maynerix95(unittest.TestCase):
    def test_values(self):
        self.assertAlmostEqual(
            clay.gmax_cptclay_maynerix95(cone_resistance=1.0, density=1750)['Gmax [kPa]'],
            30982.3, 1)


class Test_permeability_remouldedclay_carrierbeckman(unittest.TestCase):
    def test_values(self):
        self.assertAlmostEqual(
            clay.permeability_remouldedclay_carrierbeckman(
                void_ratio=1, plastic_limit=30, plasticity_index=30)['k [m/s]'],
            6.7e-11, 12)

