#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

import unittest
from pyeng.geotechnical.classification import index_tests

class Test_plasticity_chart(unittest.TestCase):

    def test_values(self):
        self.assertEqual(index_tests.plasticity_chart(40.0,
                                                      1.0)
                         ['classification [-]'],
                         "Inorganic Silts of Medium Comprssibility and Organic Silts")

        self.assertEqual(index_tests.plasticity_chart(40.0,
                                                      1.0)
                         ['aline_PI [%]'],
                         0.73*20.0)