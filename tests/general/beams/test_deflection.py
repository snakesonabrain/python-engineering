#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

import unittest
import numpy as np
from pyeng.general.beams import deflection


class TestBeamPointLoad(unittest.TestCase):

    def setUp(self):
        self.beam_length = 1.0
        self.youngs_modulus = 1.0
        self.moment_inertia = 1.0

    def test_beam_free_clamped(self):
        beam = deflection.BeamPointLoad(beam_length=self.beam_length,
                                        youngs_modulus=self.youngs_modulus,
                                        moment_inertia=self.moment_inertia,
                                        point_load=1.0,
                                        load_xmax=0.5,
                                        supporttype_left="Free",
                                        supporttype_right="Clamped")

        self.assertEqual(beam.shear_force[-1],-1.0)
        self.assertEqual(beam.bending_moment[-1],-0.5)
        self.assertAlmostEqual(beam.slope[-1],0.0,10)
        self.assertAlmostEqual(beam.deflection[-1],0.0,10)

        beam_no_load = deflection.BeamPointLoad(beam_length=self.beam_length,
                                                youngs_modulus=self.youngs_modulus,
                                                moment_inertia=self.moment_inertia,
                                                point_load=1.0,
                                                load_xmax=0.0,
                                                supporttype_left="Clamped",
                                                supporttype_right="Free")
        self.assertAlmostEqual(beam_no_load.deflection[0],0.0,10)
        self.assertAlmostEqual(beam_no_load.deflection[-1],0.0,10)
        self.assertAlmostEqual(beam_no_load.deflection[25],0.0,10)

        beam_left = deflection.BeamPointLoad(beam_length=self.beam_length,
                                             youngs_modulus=self.youngs_modulus,
                                             moment_inertia=self.moment_inertia,
                                             point_load=1.0,
                                             load_xmax=0.4,
                                             supporttype_left="Free",
                                             supporttype_right="Clamped")
        beam_right = deflection.BeamPointLoad(beam_length=self.beam_length,
                                              youngs_modulus=self.youngs_modulus,
                                              moment_inertia=self.moment_inertia,
                                              point_load=1.0,
                                              load_xmax=0.6,
                                              supporttype_left="Clamped",
                                              supporttype_right="Free")
        self.assertAlmostEqual(beam_right.deflection[-1],beam_left.deflection[0],5)
        self.assertAlmostEqual(beam_right.slope[-1],beam_left.slope[0])

    def test_beam_guided_clamped(self):
        beam_1 = deflection.BeamPointLoad(beam_length=self.beam_length,
                                          youngs_modulus=self.youngs_modulus,
                                          moment_inertia=self.moment_inertia,
                                          point_load=1.0,
                                          load_xmax=0.4,
                                          supporttype_left="Guided",
                                          supporttype_right="Clamped")
        beam_2 = deflection.BeamPointLoad(beam_length=self.beam_length,
                                          youngs_modulus=self.youngs_modulus,
                                          moment_inertia=self.moment_inertia,
                                          point_load=1.0,
                                          load_xmax=0.6,
                                          supporttype_left="Clamped",
                                          supporttype_right="Guided")

        self.assertAlmostEqual(beam_1.deflection[0],beam_2.deflection[-1],4)
        self.assertEqual(beam_1.shear_force[-1],-1.0)
        beam_1_moment_b = (-(1.0 - (0.4**2.0)))/2.0
        self.assertEqual(beam_1.bending_moment[-1],beam_1_moment_b)
        self.assertAlmostEqual(beam_1.slope[-1],0.0,10)
        self.assertAlmostEqual(beam_1.deflection[-1],0.0,10)

    def test_beam_support_clamped(self):
        beam_1 = deflection.BeamPointLoad(beam_length=self.beam_length,
                                          youngs_modulus=self.youngs_modulus,
                                          moment_inertia=self.moment_inertia,
                                          point_load=1.0,
                                          load_xmax=0.4,
                                          supporttype_left="Support",
                                          supporttype_right="Clamped")
        beam_2 = deflection.BeamPointLoad(beam_length=self.beam_length,
                                          youngs_modulus=self.youngs_modulus,
                                          moment_inertia=self.moment_inertia,
                                          point_load=1.0,
                                          load_xmax=0.6,
                                          supporttype_left="Clamped",
                                          supporttype_right="Support")
        self.assertAlmostEqual(beam_1.slope[0],beam_2.slope[-1],4)
        beam_1_reaction_b = ((1.0*0.4)/(2.0*(1.0**3.0)))*(3.0*(1.0**2.0)-(0.4**2.0))
        self.assertAlmostEqual(beam_1.shear_force[-1],-beam_1_reaction_b,5)
        beam_1_moment_b = ((-1.0*0.4)/(2.0*(1.0**2.0)))*((1.0**2.0)-(0.4**2.0))
        self.assertAlmostEqual(beam_1.bending_moment[-1],beam_1_moment_b,5)
        self.assertAlmostEqual(beam_1.slope[-1],0.0,10)
        self.assertAlmostEqual(beam_1.deflection[-1],0.0,10)

    def test_beam_clamped_clamped(self):
        beam_1 = deflection.BeamPointLoad(beam_length=self.beam_length,
                                          youngs_modulus=self.youngs_modulus,
                                          moment_inertia=self.moment_inertia,
                                          point_load=1.0,
                                          load_xmax=0.4,
                                          supporttype_left="Clamped",
                                          supporttype_right="Clamped")
        beam_2 = deflection.BeamPointLoad(beam_length=self.beam_length,
                                          youngs_modulus=self.youngs_modulus,
                                          moment_inertia=self.moment_inertia,
                                          point_load=1.0,
                                          load_xmax=0.6,
                                          supporttype_left="Clamped",
                                          supporttype_right="Clamped")
        self.assertAlmostEqual(max(beam_1.deflection),max(beam_2.deflection),4)
        beam_1_reaction_b = ((1.0*(0.4**2.0))/(1.0**3.0))*(3.0*1.0-2.0*0.4)
        self.assertAlmostEqual(beam_1.shear_force[-1],-beam_1_reaction_b,5)
        beam_1_moment_b = ((-1.0*(0.4**2.0))/(1.0**2.0))*((1.0-0.4))
        self.assertAlmostEqual(beam_1.bending_moment[-1],beam_1_moment_b,5)
        self.assertAlmostEqual(beam_1.slope[-1],0.0,10)
        self.assertAlmostEqual(beam_1.deflection[-1],0.0,10)

    def test_beam_support_support(self):
        beam_1 = deflection.BeamPointLoad(beam_length=self.beam_length,
                                          youngs_modulus=self.youngs_modulus,
                                          moment_inertia=self.moment_inertia,
                                          point_load=1.0,
                                          load_xmax=0.4,
                                          supporttype_left="Support",
                                          supporttype_right="Support")
        beam_2 = deflection.BeamPointLoad(beam_length=self.beam_length,
                                          youngs_modulus=self.youngs_modulus,
                                          moment_inertia=self.moment_inertia,
                                          point_load=1.0,
                                          load_xmax=0.6,
                                          supporttype_left="Support",
                                          supporttype_right="Support")
        self.assertAlmostEqual(max(beam_1.deflection),max(beam_2.deflection),4)
        self.assertAlmostEqual(beam_1.shear_force[-1],-0.4,5)
        self.assertAlmostEqual(beam_1.bending_moment[-1],0.0,5)
        beam_1_slope_b = (0.4 / 6.0) * (1.0 - (0.4 ** 2.0))
        self.assertAlmostEqual(beam_1.slope[-1],beam_1_slope_b,10)
        self.assertAlmostEqual(beam_1.deflection[-1],0.0,10)

    def test_beam_guided_support(self):
        beam_1 = deflection.BeamPointLoad(beam_length=self.beam_length,
                                          youngs_modulus=self.youngs_modulus,
                                          moment_inertia=self.moment_inertia,
                                          point_load=1.0,
                                          load_xmax=0.4,
                                          supporttype_left="Guided",
                                          supporttype_right="Support")
        beam_2 = deflection.BeamPointLoad(beam_length=self.beam_length,
                                          youngs_modulus=self.youngs_modulus,
                                          moment_inertia=self.moment_inertia,
                                          point_load=1.0,
                                          load_xmax=0.6,
                                          supporttype_left="Support",
                                          supporttype_right="Guided")
        self.assertAlmostEqual(beam_1.deflection[0],beam_2.deflection[-1],4)
        self.assertAlmostEqual(beam_1.shear_force[-1],-1.0,5)
        self.assertAlmostEqual(beam_1.bending_moment[-1],0.0,5)
        beam_1_slope_b = 0.5 * (1.0 - (0.4 ** 2.0))
        self.assertAlmostEqual(beam_1.slope[-1],beam_1_slope_b,10)
        self.assertAlmostEqual(beam_1.deflection[-1],0.0,10)

    def test_changes(self):
        beam = deflection.BeamPointLoad(beam_length=self.beam_length,
                                        youngs_modulus=self.youngs_modulus,
                                        moment_inertia=self.moment_inertia,
                                        point_load=1.0,
                                        load_xmax=0.4,
                                        supporttype_left="Free",
                                        supporttype_right="Clamped")
        deflection_1 = beam.deflection[0]
        beam.supporttype_left="Clamped"
        beam.calculate()
        self.assertAlmostEqual(beam.deflection[0],0.0,10)
        beam.supporttype_left="Free"
        beam.youngs_modulus = 10.0
        beam.calculate()
        self.assertGreater(abs(deflection_1),abs(beam.deflection[0]))