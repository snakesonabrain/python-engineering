#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

# Django and native Python packages
import logging
import traceback

# 3rd party packages
import numpy as np

# Project imports
from pyeng.general.validation import ValidationDecorator, Validator


LATERALEARTHPRESSURE_PLASTICITY_MASSARSCH = {
    'plasticity_index': {'type': 'float', 'min_value': 20.0, 'max_value': 70.0},
}


@ValidationDecorator(LATERALEARTHPRESSURE_PLASTICITY_MASSARSCH)
def lateralearthpressure_plasticity_massarsch(plasticity_index, fail_silently=True, **kwargs):
    """
    Calculates the coefficient of lateral earth pressure at rest from the plasticity index for a normally consolidated clay. The correlation is based on a number of tests on normally consolidated italian clays. For PI<20%, the correlation overestimates the coefficient of lateral earth pressure at rest.

    :param plasticity_index: Plasticity index (:math:`PI`) [:math:`\%`]  - Suggested range: 20.0<=plasticity_index<=70.0

    :returns:   Ko (:math:`Ko`) [:math:`-`]

    :rtype: Python dictionary with keys ['Ko [-]']

    .. figure:: images/lateralearthpressure_plasticity_massarsch.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Correlation between coefficient of lateral earth pressure at rest and plasticity index for normally consolidated Italian clays

    Reference - Massarsch K.R. (1979). Lateral earth pressure in normally consolidated clay. 8th ECSMFE, Brighton, 2: 245-249

    """

    try:

        if not kwargs['validated']:
            raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

        # Calculation statements
        Ko = np.interp(plasticity_index,
                       [0.0, 110.0],
                       [0.4668587896253603, 0.8631123919308359])

        return {
            'Ko [-]': Ko,
        }

    except:
        if fail_silently or fail_silently is None:
            return {
                'Ko [-]': np.NaN,
            }
        else:
            raise


SECONDARYCOMPRESSIONRATIO_WATERCONTENT_MESRI = {
    'water_content': {'type': 'float', 'min_value': 10.0, 'max_value': 2000.0},
}


@ValidationDecorator(SECONDARYCOMPRESSIONRATIO_WATERCONTENT_MESRI)
def secondarycompressionratio_watercontent_mesri(water_content, fail_silently=True, **kwargs):
    """
    For a given clay the logarithm of the secondary compression ratio :math:`C_{\\alpha \\epsilon}` shows a linear correlation with the logarithm of the natural water content. Note that the secondary compression ratio is NOT equal to the ratio of the secondary compression index :math:`C_{\\alpha}` to the compression index :math:`C_c`. The definitions are given in the equations below.

    :param water_content: Natural water content of the clay (:math:`w`) [:math:`\%`]  - Suggested range: 10.0<=water_content<=2000.0

    .. math::
        C_{\\alpha \\epsilon} = \\frac{C_{\\alpha}}{1 + e_o}

        \\text{Organic soft clays} \\quad C_{\\alpha}/C_c = 0.05 \\pm 0.01

        \\text{Inorganic soft clays} \\quad C_{\\alpha}/C_c = 0.04 \\pm 0.01

        \\text{Sands} \\quad C_{\\alpha}/C_c = 0.015 \\pm 0.03

    :returns:   Secondary compression ratio (:math:`C_{\\alpha \\epsilon}`) [:math:`\%`]

    :rtype: Python dictionary with keys ['secondary_compression_ratio [%]']

    .. figure:: images/secondarycompressionratio_watercontent_mesri.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Secondary compression ratio vs water content based on data from 12 natural clays

    Mesri G, Godlewski P.M. (1977). Time and stress-compressibility interrelationship. Journal of Geotechnical Eng. Division, ASCE, GT5: 417-430.

    """

    try:

        if not kwargs['validated']:
            raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

        secondary_compression_ratio = 10.0**(np.interp(np.log10(water_content),
                                                       [np.log10(9.999703334951846), np.log10(3822.2040801773114)],
                                                       [np.log10(0.10000890047953175), np.log10(39.942386556889026)]))

        return {
            'secondary_compression_ratio [%]': secondary_compression_ratio,
        }

    except:
        if fail_silently or fail_silently is None:
            return {
                'secondary_compression_ratio [%]': np.NaN,
            }
        else:
            raise


GMAX_CPTCLAY_MAYNERIX95 = {
    'cone_resistance': {'type': 'float', 'min_value': 0.0, 'max_value': 120.0},
    'density': {'type': 'float', 'min_value': 1000.0, 'max_value': 3000.0},
    'coefficient_1': {'type': 'float', 'min_value': None, 'max_value': None},
    'coefficient_2': {'type': 'float', 'min_value': None, 'max_value': None},
}

GMAX_CPTCLAY_MAYNERIX95_ERRORRETURN = {
    'Vs [m/s]': np.nan,
    'Gmax [kPa]': np.nan,
}


@Validator(GMAX_CPTCLAY_MAYNERIX95, GMAX_CPTCLAY_MAYNERIX95_ERRORRETURN)
def gmax_cptclay_maynerix95(
        cone_resistance, density,
        coefficient_1=1.75, coefficient_2=0.627, **kwargs):
    """
    Calculates the small-strain shear modulus for intact and fissured clays. This relation is used when initial void ratio is difficult to estimate.

    :param cone_resistance: Cone tip resistance (:math:`q_c`) [:math:`MPa`] - Suggested range: 0.0 <= cone_resistance <= 120.0
    :param density: Density of the soil material (:math:`\\rho`) [:math:`kg/m3`] - Suggested range: 1000.0 <= density <= 3000.0
    :param coefficient_1: First coefficient (multiplier) in the correlation (:math:``) [:math:`-`] (optional, default= 1.75)
    :param coefficient_2: Second coefficient (exponent) in the correlation (:math:``) [:math:`-`] (optional, default= 0.627)

    .. math::
        V_s = 1.75 \\cdot (q_c)^{0.627}

        G_{max} = \\rho \\cdot V_s^2

    :returns: Dictionary with the following keys:

        - 'Vs [m/s]': Shear wave velocity (:math:`V_s`)  [:math:`m/s`]
        - 'Gmax [kPa]': Small-strain shear modulus (:math:`G_{max}`)  [:math:`kPa`]

    Reference - Ameratunga, J., Sivakugan, N., Das, B.M., 2016. Correlations of Soil and Rock Properties in Geotechnical Engineering. Springer, India.

    """

    _vs = coefficient_1 * (1e3 * cone_resistance) ** coefficient_2
    _gmax = density * (_vs ** 2) * 1e-3

    return {
        'Vs [m/s]': _vs,
        'Gmax [kPa]': _gmax,
    }


PERMEABILITY_REMOULDEDCLAY_CARRIERBECKMAN = {
    'void_ratio': {'type': 'float', 'min_value': 0.0, 'max_value': 4.0},
    'plastic_limit': {'type': 'float', 'min_value': 0.0, 'max_value': 100.0},
    'plasticity_index': {'type': 'float', 'min_value': 0.0, 'max_value': 100.0},
    'coefficient_1': {'type': 'float', 'min_value': None, 'max_value': None},
    'coefficient_2': {'type': 'float', 'min_value': None, 'max_value': None},
    'coefficient_3': {'type': 'float', 'min_value': None, 'max_value': None},
    'coefficient_4': {'type': 'float', 'min_value': None, 'max_value': None},
}

PERMEABILITY_REMOULDEDCLAY_CARRIERBECKMAN_ERRORRETURN = {
    'k [m/s]': np.nan,
}


@Validator(PERMEABILITY_REMOULDEDCLAY_CARRIERBECKMAN, PERMEABILITY_REMOULDEDCLAY_CARRIERBECKMAN_ERRORRETURN)
def permeability_remouldedclay_carrierbeckman(
        void_ratio, plastic_limit, plasticity_index,
        coefficient_1=0.0174, coefficient_2=0.027, coefficient_3=0.242, coefficient_4=4.29, **kwargs):
    """
    The correlation provides the permeability of remoulded clay based on the void ratio of the clay and the Atterberg limits.

    :param void_ratio: Void ratio for the remoulded clay (:math:`e`) [:math:`-`] - Suggested range: 0.0 <= void_ratio <= 4.0
    :param plastic_limit: Plastic limit of the clay (:math:`PL`) [:math:`pct`] - Suggested range: 0.0 <= plastic_limit <= 100.0
    :param plasticity_index: Plasticity index of the clay (:math:`PI`) [:math:`pct`] - Suggested range: 0.0 <= plasticity_index <= 100.0
    :param coefficient_1: First coefficient in the equation (:math:``) [:math:`-`] (optional, default= 0.0174)
    :param coefficient_2: Second coefficient in the equation (:math:``) [:math:`-`] (optional, default= 0.027)
    :param coefficient_3: Third coefficient in the equation (:math:``) [:math:`-`] (optional, default= 0.242)
    :param coefficient_4: Fourth coefficient in the equation (:math:``) [:math:`-`] (optional, default= 4.29)

    .. math::
        k(m/s) \\approx \\frac{0.0174}{1+e} \\left[ \\frac{e-0.027 \\cdot (PL - 0.242 \\cdot PI)}{PI} \\right]^{4.29}

    :returns: Dictionary with the following keys:

        - 'k [m/s]': Permeability of the remoulded clay (:math:`k`)  [:math:`m/s`]

    Reference - Carrier WD III, Beckman JF (1984) Correlations between index tests and the properties of remolded clays. Geotechnique 34(2):211–228

    """

    _k = (coefficient_1 / (1 + void_ratio)) * \
         (((void_ratio - coefficient_2 * (plastic_limit - coefficient_3 * plasticity_index)) /
           (plasticity_index)) ** coefficient_4)

    return {
        'k [m/s]': _k,
    }