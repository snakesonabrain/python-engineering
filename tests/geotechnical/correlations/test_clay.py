#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

import unittest
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
