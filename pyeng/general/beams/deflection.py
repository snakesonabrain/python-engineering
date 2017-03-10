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

    def __init__(self, beam_length,youngs_modulus,moment_inertia,point_load,load_xmax=0.0,
                 supporttype_left="Support",supporttype_right="Support",seed=50, fail_silently=True):
        self._beam_length = beam_length
        self._youngs_modulus = youngs_modulus
        self._moment_inertia = moment_inertia
        self._point_load = point_load
        self._load_xmax = load_xmax
        self._supporttype_left = supporttype_left
        self._supporttype_right = supporttype_right
        self._seed = seed
        self._fail_silently = fail_silently
        self.calculate()

    @property
    def beam_length(self):
        return self._beam_length

    @beam_length.setter
    def beam_length(self, value):
        self._beam_length = value
        if value: self.calculate()

    @property
    def youngs_modulus(self):
        return self._youngs_modulus

    @youngs_modulus.setter
    def youngs_modulus(self, value):
        self._youngs_modulus = value
        if value: self.calculate()

    @property
    def moment_inertia(self):
        return self._moment_inertia

    @moment_inertia.setter
    def moment_inertia(self, value):
        self._moment_inertia = value
        if value: self.calculate()

    @property
    def point_load(self):
        return self._point_load

    @point_load.setter
    def point_load(self, value):
        self._point_load = value
        if value: self.calculate()

    @property
    def load_xmax(self):
        return self._load_xmax

    @load_xmax.setter
    def load_xmax(self, value):
        self._load_xmax = value
        if value: self.calculate()

    @property
    def supporttype_left(self):
        return self._supporttype_left

    @supporttype_left.setter
    def supporttype_left(self, value):
        self._supporttype_left = value
        if value: self.calculate()

    @property
    def supporttype_right(self):
        return self._supporttype_right

    @supporttype_right.setter
    def supporttype_right(self, value):
        self._supporttype_right = value
        if value: self.calculate()

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value
        if value: self.calculate()

    @property
    def fail_silently(self):
        return self._fail_silently

    @fail_silently.setter
    def fail_silently(self, value):
        self._fail_silently = value

    def calculate(self):
        self.calculate_validated(self._beam_length, self._youngs_modulus, self._moment_inertia,
                                 self._point_load, load_xmax = self._load_xmax,
                                 supporttype_left = self._supporttype_left, supporttype_right = self._supporttype_right,
                                 seed = self._seed, fail_silently=self._fail_silently)

    @ValidationDecorator(BEAMPOINTLOAD_VALIDATORS)
    def calculate_validated(self, beam_length,youngs_modulus,moment_inertia,point_load,load_xmax=0.0,
                 supporttype_left="Support",supporttype_right="Support",seed=50,
                 fail_silently=True,**kwargs):

        self.reaction_left = np.NaN
        self.slope_left = np.NaN        # Radians!!
        self.moment_left = np.NaN
        self.deflection_left = np.NaN
        self.shear_force = np.NaN
        self.bending_moment = np.NaN
        self.slope = np.NaN
        self.deflection = np.NaN
        rigidity = youngs_modulus * moment_inertia
        flip = False

        try:
            if not kwargs['validated']:
                raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

            #region Cases
            if (supporttype_left=="Free" and supporttype_right=="Clamped") or \
                    (supporttype_left=="Clamped" and supporttype_right=="Free"):

                if supporttype_left=="Clamped":
                    flip = True
                    a = beam_length - load_xmax
                else:
                    a = load_xmax

                self.reaction_left = 0.0
                self.moment_left = 0.0
                self.slope_left = (point_load * ((beam_length - a)**2.0))/(2.0 * rigidity)
                self.deflection_left = (-point_load / (6.0 * rigidity)) * \
                                       (2.0*(beam_length**3.0) - (3.0 * (beam_length**2.0) * a) + (a**3.0))

            if (supporttype_left=="Support" and supporttype_right=="Clamped") or \
                    (supporttype_left=="Clamped" and supporttype_right=="Support"):

                if supporttype_left=="Clamped":
                    flip = True
                    a = beam_length - load_xmax
                else:
                    a = load_xmax

                self.reaction_left = (point_load/(2.0*(beam_length**3.0)))*\
                                     ((beam_length-a)**2.0)*\
                                     (2.0*beam_length+a)
                self.moment_left = 0.0
                self.slope_left = ((-point_load*a)/(4.0*rigidity*beam_length))*\
                                  ((beam_length-a)**2.0)
                self.deflection_left = 0.0

            if (supporttype_left == "Guided" and supporttype_right == "Clamped") or \
                    (supporttype_left == "Clamped" and supporttype_right == "Guided"):

                if supporttype_left == "Clamped":
                    flip = True
                    a = beam_length - load_xmax
                else:
                    a = load_xmax

                self.reaction_left = 0.0
                self.moment_left = (point_load * ((beam_length - a) ** 2.0)) / \
                                   (2.0 * beam_length)
                self.slope_left = 0.0
                self.deflection_left = (-point_load / (12.0 * rigidity)) * \
                                       ((beam_length - a) ** 2.0) * \
                                       (beam_length + 2.0 * a)

            if supporttype_left == "Clamped" and supporttype_right == "Clamped":

                a = load_xmax

                self.reaction_left = (point_load / (beam_length ** 3.0)) * \
                                     ((beam_length - a) ** 2.0) * \
                                     (beam_length + 2.0*a)
                self.moment_left = ((-point_load * a) / (beam_length ** 2.0)) * \
                                   ((beam_length - a) ** 2.0)
                self.slope_left = 0.0
                self.deflection_left = 0.0

            if supporttype_left == "Support" and supporttype_right == "Support":

                a = load_xmax

                self.reaction_left = (point_load / beam_length) * (beam_length - a)
                self.moment_left = 0.0
                self.slope_left = ((-point_load * a) / (6.0 * rigidity * beam_length)) * \
                                  (2.0 * beam_length - a) * \
                                  (beam_length - a)
                self.deflection_left = 0.0

            if (supporttype_left == "Guided" and supporttype_right == "Support") or \
                    (supporttype_left == "Support" and supporttype_right == "Guided"):

                if supporttype_left == "Support":
                    flip = True
                    a = beam_length - load_xmax
                else:
                    a = load_xmax

                self.reaction_left = 0.0
                self.moment_left = point_load * (beam_length - a)
                self.slope_left = 0.0
                self.deflection_left = ((-point_load * (beam_length - a)) / (6.0 * rigidity)) * \
                                       (2.0 * (beam_length ** 2.0) + 2.0 * a * beam_length -
                                        (a ** 2.0))

            self.x = np.linspace(0.0, beam_length, seed)

            self.multiplier = np.piecewise(self.x, [self.x < a, self.x >= a], [0, 1.0])

            self.shear_force = list(map(lambda mult: self.reaction_left - point_load*(mult**0.0),
                                        self.multiplier))
            if flip:
                self.shear_force = np.flipud(self.shear_force)

            self.bending_moment =  list(map(lambda x, mult: self.moment_left +
                                                            self.reaction_left*x -
                                                            point_load*mult*(x - a),
                                            self.x,
                                            self.multiplier))
            if flip:
                self.bending_moment = np.flipud(self.bending_moment)

            self.slope = list(map(lambda x,mult: self.slope_left +
                                                 (self.moment_left * x / rigidity) +
                                                 ((self.reaction_left * (x ** 2.0)) / (2.0 * rigidity)) -
                                                 ((point_load * ((mult*(x - a)) ** 2.0)) / (2.0 * rigidity)),
                            self.x,
                            self.multiplier))
            if flip:
                self.slope = np.flipud(self.slope)

            self.deflection = list(map(lambda x, mult: self.deflection_left +
                                                       (self.slope_left*x) +
                                                       ((self.moment_left*(x**2.0))/(2.0*rigidity)) +
                                                       ((self.reaction_left * (x**3.0))/(6.0 * rigidity)) -
                                                       ((point_load*((mult*(x - a))**3.0))/(6.0 * rigidity)),
                                       self.x,
                                       self.multiplier))
            if flip:
                self.deflection = np.flipud(self.deflection)

        except:
            self.reaction_left = np.NaN
            self.slope_left = np.NaN  # Radians!!
            self.moment_left = np.NaN
            self.deflection_left = np.NaN
            self.shear_force = np.NaN
            self.bending_moment = np.NaN
            self.slope = np.NaN
            self.deflection = np.NaN

            if fail_silently or fail_silently is None:
                print("Error raised but silenced")
            else:
                raise