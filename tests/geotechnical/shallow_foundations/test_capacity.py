import unittest

import numpy as np

from pyeng.geotechnical.shallow_foundations import capacity


class Test_nq_frictionangle_sand(unittest.TestCase):
    def test_values(self):
        nq_calc = capacity.nq_frictionangle_sand(
            friction_angle=30.0, fail_silently=False)
        self.assertAlmostEqual(nq_calc['Nq [-]'], 18.4, 1)


class Test_ngamma_frictionangle_vesic(unittest.TestCase):
    def test_values(self):
        ngamma_calc = capacity.ngamma_frictionangle_vesic(
            friction_angle=30.0, fail_silently=False)
        self.assertAlmostEqual(ngamma_calc['Ngamma [-]'], 22.4, 1)


class Test_ngamma_frictionangle_meyerhof(unittest.TestCase):
    def test_values(self):
        ngamma_calc = capacity.ngamma_frictionangle_meyerhof(
            friction_angle=30.0, fail_silently=False)
        self.assertAlmostEqual(ngamma_calc['Ngamma [-]'], 15.7, 1)


class Test_ngamma_frictionangle_davisbooker(unittest.TestCase):
    def test_values(self):
        ngamma_calc = capacity.ngamma_frictionangle_davisbooker(
            friction_angle=30.0, roughness_factor=0.0,fail_silently=False)
        self.assertAlmostEqual(ngamma_calc['Ngamma [-]'], 8.63, 1)
        ngamma_calc = capacity.ngamma_frictionangle_davisbooker(
            friction_angle=30.0, roughness_factor=1.0, fail_silently=False)
        self.assertAlmostEqual(ngamma_calc['Ngamma [-]'], 16.1, 1)
        ngamma_calc = capacity.ngamma_frictionangle_davisbooker(
            friction_angle=30.0, roughness_factor=0.5, fail_silently=False)
        self.assertAlmostEqual(ngamma_calc['Ngamma [-]'], 12.3, 1)