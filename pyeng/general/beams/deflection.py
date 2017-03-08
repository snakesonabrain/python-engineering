#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

from pyeng.general.validation import ValidationDecorator, validate_float, validate_list
import numpy as np

BEAMPOINTLOAD_VALIDATORS = {
    'beam_length': {'type':'float','min_value':0.0,'max_value':None},
    'youngs_modulus': {'type':'float','min_value':0.0,'max_value':None},
    'moment_inertia': {'type':'float','min_value':0.0,'max_value':None},
    'point_load': {'type':'float','min_value':None,'max_value':None},
    'load_xmax': {'type': 'float', 'min_value': None, 'max_value': None},
    'supporttype_left': {'type':'string','options':("Free","Support","Clamped","Guided"),'regex':None},
    'supporttype_right': {'type':'string','options':("Free","Support","Clamped","Guided"),'regex':None},
    'seed': {'type': 'int', 'min_value': 1, 'max_value': None}
}

class BeamPointLoad(object):
    """
    Represents a thin linear elastic beam with a point load applied for which shear forces, moments, slopes and
    deflections are calculated under various combinations of geometry and support.

    Provided that the following conditions are met:

        - The beam is originally straight, and any taper is slight
        - The beam experiences only linear elastic deformation
        - The beam is slender (its length to height ratio is greater than 10)
        - Only small deflections are considered (max deflection less than 1/10 the span).

    In this case, the equation governing the beam's deflection (:math:`w`) can be approximated as:

    .. math::
        \\frac{\\mathrm{d}^{2}w(x)}{\\mathrm{d} x^{2}} = \\frac{M(x)}{E(x)I(x)}

    A beam instance is created using a constructor with the following arguments:

    :param beam_length: Total length of the beam (:math:`L`) [:math:`m`] - Suggested range: 0.0<= :math:`L`
    :param youngs_modulus: Young's modulus of the beam (:math:`E`) [:math:`kPa`] - Suggested range: 0.0<= :math:`E`
    :param moment_inertia: Area moment of intertia about the beam axis - See ``general.geometry.geom_2d.TwodimensionalShape`` (:math:`I`) [:math:`m4`] - Suggested range: 0.0<= :math:`I`
    :param point_load: Magnitude of the point load (:math:`P`) [:math:`kN`]
    :param load_xmax: X-coordinate of the point load application point measured from the leftmost support(:math:`x_{P}`) [:math:`m`] (optional, default=0.0) - Suggested range: 0.0 < :math:`x_{P}` < :math:`L`
    :param supporttype_left: Type of support at the leftmost support [-] (optional, default="Support") - Options = ("Free","Support","Clamped","Guided")
    :param supporttype_right: Type of support at the rightmost support [-] (optional, default="Support") - Options = ("Free","Support","Clamped","Guided")
    :param seed: Number of nodes along the beam length [-] (optional, default=50)

    This creates a beam according to the following sign convention:

    .. figure:: images/GeneralBeam.png
        :figwidth: 500
        :width: 400
        :align: center

        Sign convention and nomenclature for beams with point load applied.

    Shear forces, bending moments, slopes and deflections are calculated numerically along the beam length.
    Upon instance creation, the shear forces, bending moments, slopes and deflections are calculated. When properties
    of the beam are changed, the calculate function needs to be called again.
    Maximum or minimum values can be extracted by applying Python's built-in min() and max() functions to the results.
    Increasing the number of nodes will increase the accuracy.

    Examples:
        .. code-block:: python

            >>>beam = deflection.BeamPointLoad(beam_length=1.0,
                                               youngs_modulus=210.0e6,
                                               moment_inertia=0.01,
                                               point_load=1.0,
                                               load_xmax=0.4,
                                               supporttype_left="Clamped",
                                               supporttype_right="Support")
            >>>print("%20.12e meter" % min(beam.deflection))
            -3.657951072379e-09 meter
            >>>beam.seed = 10000 # Improve the accuracy by increasing the seed
            >>>beam.calculate()
            >>>print("%20.12e meter" % min(beam.deflection))
            -3.660072055407e-09 meter

    If the beam behaves elastically for a combined loading scenario, with linear elastic behaviour also applying
    to each of the individual loadcases, then the principle of superposition can be applied. According to this
    principle, the resulting deflections and slopes are simply the algebraic sum of the deflection and slope for
    each individual load combination. Small deflection theory also need to be applicable. To apply the principle of
    superposition, simply create two beam instances with the same support types and positions, length and cross-
    sectional properties and sum the resulting deflections. Note that the location of the resulting maximum deflection
    is not equal to the sum of the location of individual deflections.

    References - Wikipedia: https://en.wikipedia.org/wiki/Deflection_(engineering)

    """
    @ValidationDecorator(BEAMPOINTLOAD_VALIDATORS)
    def __init__(self, beam_length,youngs_modulus,moment_inertia,point_load,load_xmax=0.0,
                 supporttype_left="Support",supporttype_right="Support",seed=50,
                 fail_silently=True,**kwargs):

        self.load_xmax = load_xmax
        self.beam_length = beam_length
        self.point_load = point_load
        self.youngs_modulus = youngs_modulus
        self.moment_inertia = moment_inertia
        self.supporttype_left = supporttype_left
        self.supporttype_right = supporttype_right
        self.seed = seed

        self.reaction_left = np.NaN
        self.slope_left = np.NaN        # Radians!!
        self.moment_left = np.NaN
        self.deflection_left = np.NaN
        self.shear_force = np.NaN
        self.bending_moment = np.NaN
        self.slope = np.NaN
        self.deflection = np.NaN
        self.flip = False

        self.calculate()

    def check_cases(self):
        #region Cases
        if (self.supporttype_left=="Free" and self.supporttype_right=="Clamped") or \
                (self.supporttype_left=="Clamped" and self.supporttype_right=="Free"):

            if self.supporttype_left=="Clamped":
                self.flip = True
                self.a = self.beam_length - self.load_xmax
            else:
                self.a = self.load_xmax

            self.reaction_left = 0.0
            self.moment_left = 0.0
            self.slope_left = (self.point_load * ((self.beam_length - self.a)**2.0))/(2.0 * self.rigidity)
            self.deflection_left = (-self.point_load / (6.0 * self.rigidity)) * \
                                   (2.0*(self.beam_length**3.0) - (3.0 * (self.beam_length**2.0) * self.a) + (self.a**3.0))

        if (self.supporttype_left=="Support" and self.supporttype_right=="Clamped") or \
                (self.supporttype_left=="Clamped" and self.supporttype_right=="Support"):

            if self.supporttype_left=="Clamped":
                self.flip = True
                self.a = self.beam_length - self.load_xmax
            else:
                self.a = self.load_xmax

            self.reaction_left = (self.point_load/(2.0*(self.beam_length**3.0)))*\
                                 ((self.beam_length-self.a)**2.0)*\
                                 (2.0*self.beam_length+self.a)
            self.moment_left = 0.0
            self.slope_left = ((-self.point_load*self.a)/(4.0*self.rigidity*self.beam_length))*\
                              ((self.beam_length-self.a)**2.0)
            self.deflection_left = 0.0

        if (self.supporttype_left == "Guided" and self.supporttype_right == "Clamped") or \
                (self.supporttype_left == "Clamped" and self.supporttype_right == "Guided"):

            if self.supporttype_left == "Clamped":
                self.flip = True
                self.a = self.beam_length - self.load_xmax
            else:
                self.a = self.load_xmax

            self.reaction_left = 0.0
            self.moment_left = (self.point_load * ((self.beam_length - self.a) ** 2.0)) / \
                               (2.0 * self.beam_length)
            self.slope_left = 0.0
            self.deflection_left = (-self.point_load / (12.0 * self.rigidity)) * \
                                   ((self.beam_length - self.a) ** 2.0) * \
                                   (self.beam_length + 2.0 * self.a)

        if self.supporttype_left == "Clamped" and self.supporttype_right == "Clamped":

            self.a = self.load_xmax

            self.reaction_left = (self.point_load / (self.beam_length ** 3.0)) * \
                                 ((self.beam_length - self.a) ** 2.0) * \
                                 (self.beam_length + 2.0*self.a)
            self.moment_left = ((-self.point_load * self.a) / (self.beam_length ** 2.0)) * \
                               ((self.beam_length - self.a) ** 2.0)
            self.slope_left = 0.0
            self.deflection_left = 0.0

        if self.supporttype_left == "Support" and self.supporttype_right == "Support":

            self.a = self.load_xmax

            self.reaction_left = (self.point_load / self.beam_length) * (self.beam_length - self.a)
            self.moment_left = 0.0
            self.slope_left = ((-self.point_load * self.a) / (6.0 * self.rigidity * self.beam_length)) * \
                              (2.0 * self.beam_length - self.a) * \
                              (self.beam_length - self.a)
            self.deflection_left = 0.0

        if (self.supporttype_left == "Guided" and self.supporttype_right == "Support") or \
                (self.supporttype_left == "Support" and self.supporttype_right == "Guided"):

            if self.supporttype_left == "Support":
                self.flip = True
                self.a = self.beam_length - self.load_xmax
            else:
                self.a = self.load_xmax

            self.reaction_left = 0.0
            self.moment_left = self.point_load * (self.beam_length - self.a)
            self.slope_left = 0.0
            self.deflection_left = ((-self.point_load * (self.beam_length - self.a)) / (6.0 * self.rigidity)) * \
                                   (2.0 * (self.beam_length ** 2.0) + 2.0 * self.a * self.beam_length -
                                    (self.a ** 2.0))

    def calculate(self):
        self.rigidity = self.youngs_modulus * self.moment_inertia
        self.x = np.linspace(0.0, self.beam_length, self.seed)
        self.check_cases()
        self.calculate_multiplier()
        self.calculate_shearforce()
        self.calculate_bendingmoment()
        self.calculate_slope()
        self.calculate_deflection()

    def calculate_multiplier(self):
        self.multiplier = np.piecewise(self.x, [self.x < self.a, self.x >= self.a], [0, 1.0])

    def calculate_shearforce(self):
        self.shear_force = list(map(lambda mult: self.reaction_left - self.point_load*(mult**0.0),
                                    self.multiplier))
        if self.flip:
            self.shear_force = np.flipud(self.shear_force)

    def calculate_bendingmoment(self):
        self.bending_moment =  list(map(lambda x, mult: self.moment_left +
                                                        self.reaction_left*x -
                                                        self.point_load*mult*(x - self.a),
                                        self.x,
                                        self.multiplier))
        if self.flip:
            self.bending_moment = np.flipud(self.bending_moment)

    def calculate_slope(self):
        self.slope = list(map(lambda x,mult: self.slope_left +
                                             (self.moment_left * x / self.rigidity) +
                                             ((self.reaction_left * (x ** 2.0)) / (2.0 * self.rigidity)) -
                                             ((self.point_load * ((mult*(x - self.a)) ** 2.0)) / (2.0 * self.rigidity)),
                        self.x,
                        self.multiplier))
        if self.flip:
            self.slope = np.flipud(self.slope)

    def calculate_deflection(self):
        self.deflection = list(map(lambda x, mult: self.deflection_left +
                                                   (self.slope_left*x) +
                                                   ((self.moment_left*(x**2.0))/(2.0*self.rigidity)) +
                                                   ((self.reaction_left * (x**3.0))/(6.0 * self.rigidity)) -
                                                   ((self.point_load*((mult*(x - self.a))**3.0))/(6.0 * self.rigidity)),
                                   self.x,
                                   self.multiplier))
        if self.flip:
            self.deflection = np.flipud(self.deflection)