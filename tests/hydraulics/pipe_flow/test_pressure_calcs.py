#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

import unittest
from pyeng.hydraulics.pipe_flow import pressure_calcs
import numpy as np
import math
# Unit test

class Test_pressuredrop_relativeroughness_moody(unittest.TestCase):

    def test_fail_silently(self):
        pressure_calcs.pressuredrop_relativeroughness_moody(100.0,
                                                            1.0,
                                                            "Water mains,old",
                                                            10.0,
                                                            5.0,
                                                            1050.0)
        self.assertEqual(math.isnan(
            pressure_calcs.pressuredrop_relativeroughness_moody(
                100.0,
                1.0,
                "Water mains,old",
                10.0,
                5.0,
                1050.0)['friction_factor [-]']),
                         True)

    def test_fail_with_error(self):
        self.assertRaises(ValueError,
                          pressure_calcs.pressuredrop_relativeroughness_moody,
                          100.0,
                          1.0,
                          "Water mains,old",
                          10.0,
                          5.0,
                          1050.0,
                          fail_silently=False)

    def test_values(self):
        self.assertAlmostEqual(
            pressure_calcs.pressuredrop_relativeroughness_moody(1.0e6,
                                                                1.0,
                                                                "Water mains,old",
                                                                10.0,
                                                                5.0,
                                                                1050.0)['friction_factor [-]'],
            0.02, 2)

        self.assertAlmostEqual(
            pressure_calcs.pressuredrop_relativeroughness_moody(1.0e6,
                                                                1.0,
                                                                "Water mains,old",
                                                                10.0,
                                                                5.0,
                                                                1050.0,
                                                                relative_roughness=0.001)['friction_factor [-]'],
            0.02, 2)

        self.assertEqual(
            pressure_calcs.pressuredrop_relativeroughness_moody(1.0e6,
                                                                0.3,
                                                                "Water mains,old",
                                                                10.0,
                                                                5.0,
                                                                1050.0)['flow_regime [-]'],
            "Complete turbulence")

        self.assertEqual(
            pressure_calcs.pressuredrop_relativeroughness_moody(1.0e6,
                                                                2.0,
                                                                "Water mains,old",
                                                                10.0,
                                                                5.0,
                                                                1050.0)['flow_regime [-]'],
            "Transition Region")
