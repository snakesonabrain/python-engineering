#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

import unittest
from pyeng.geotechnical.consolidation import onedimensional
import numpy as np

# Unit test

class Test_consolidation_drainage_janbu(unittest.TestCase):
    def test_values(self):
        self.assertEqual(
            onedimensional.consolidation_drainage_janbu(time=(3600.0 * 24.0 * 365.0),
                                                        consolidation_coefficient=10.0,
                                                        drainage_path_length=1.0,
                                                        drainage_type="double", stress_distribution="constant")[
                'time_factor [-]'], 10.0)

        self.assertAlmostEqual(
            onedimensional.consolidation_drainage_janbu(time=(3600.0 * 24.0 * 365.0),
                                                        consolidation_coefficient=0.4,
                                                        drainage_path_length=1.0,
                                                        drainage_type="double", stress_distribution="constant")[
                'consolidation_degree [%]'], 70.6, 1)

        self.assertAlmostEqual(
            onedimensional.consolidation_drainage_janbu(time=(3600.0 * 24.0 * 365.0),
                                                        consolidation_coefficient=0.4,
                                                        drainage_path_length=1.0,
                                                        drainage_type="single",
                                                        stress_distribution="triangular increasing")[
                'consolidation_degree [%]'], 61.8, 1)

        self.assertAlmostEqual(
            onedimensional.consolidation_drainage_janbu(time=(3600.0 * 24.0 * 365.0),
                                                        consolidation_coefficient=0.4,
                                                        drainage_path_length=1.0,
                                                        drainage_type="single",
                                                        stress_distribution="triangular decreasing")[
                'consolidation_degree [%]'], 79.0, 1)