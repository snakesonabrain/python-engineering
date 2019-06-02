#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

# Django and native Python packages
import warnings

# 3rd party packages
import numpy as np

# Project imports
from pyeng.general.validation import Validator


NQ_FRICTIONANGLE_SAND = {
    'friction_angle': {'type': 'float', 'min_value': 20.0, 'max_value': 50.0},
}

NQ_FRICTIONANGLE_SAND_ERRORRETURN = {
    'Nq [-]': np.NaN,
}


@Validator(NQ_FRICTIONANGLE_SAND, NQ_FRICTIONANGLE_SAND_ERRORRETURN)
def nq_frictionangle_sand(
        friction_angle,
        **kwargs):
    """
    Calculate the bearing capacity factor Nq from the friction angle

    :param friction_angle: Peak effective friction angle (:math:`\\phi_p^{\\prime}`) [:math:`deg`] - Suggested range: 20.0 <= friction_angle <= 50.0

    .. math::
        N_q = e^{\\pi \\tan \\phi_p^{\\prime}} \\tan^2 \\left( 45^{\\circ} + \\frac{ \\phi_p^{\\prime}}{2} \\right)

    :returns: Dictionary with the following keys:

        - 'Nq [-]': Bearing capacity factor (:math:`N_q`)  [:math:`-`]

    Reference - Budhu (2011) Introduction to soil mechanics and foundations

    """

    _Nq = np.exp(np.pi * np.tan(np.radians(friction_angle))) * \
          ((np.tan(np.radians(45.0 + 0.5 * friction_angle))) ** 2.0)

    return {
        'Nq [-]': _Nq,
    }


NGAMMA_FRICTIONANGLE_VESIC = {
    'friction_angle': {'type': 'float', 'min_value': 20.0, 'max_value': 50.0},
}

NGAMMA_FRICTIONANGLE_VESIC_ERRORRETURN = {
    'Ngamma [-]': np.NaN,
}


@Validator(NGAMMA_FRICTIONANGLE_VESIC, NGAMMA_FRICTIONANGLE_VESIC_ERRORRETURN)
def ngamma_frictionangle_vesic(
        friction_angle,
        **kwargs):
    """
    Calculates the bearing capacity factor Ngamma according to the equation proposed by Vesic (1973). Note that alternative formulations are available.

    :param friction_angle: Peak drained friction angle (:math:`\\phi_p^{\\prime}`) [:math:`deg`] - Suggested range: 20.0 <= friction_angle <= 50.0

    .. math::
        N_{\\gamma} = 2 (N_q + 1) \\tan \\phi_p^{\\prime}

    :returns: Dictionary with the following keys:

        - 'Ngamma [-]': Bearing capacity factor (:math:`N_{\\gamma}`)  [:math:`-`]

    Reference - Budhu (2011) Introduction to soil mechanics and foundations

    """

    _Ngamma = 2.0 * (nq_frictionangle_sand(friction_angle)['Nq [-]'] + 1.0) * np.tan(np.radians(friction_angle))

    return {
        'Ngamma [-]': _Ngamma,
    }


NGAMMA_FRICTIONANGLE_MEYERHOF = {
    'friction_angle': {'type': 'float', 'min_value': 20.0, 'max_value': 50.0},
    'frictionangle_multiplier': {'type': 'float', 'min_value': None, 'max_value': None},
}

NGAMMA_FRICTIONANGLE_MEYERHOF_ERRORRETURN = {
    'Ngamma [-]': np.NaN,
}


@Validator(NGAMMA_FRICTIONANGLE_MEYERHOF, NGAMMA_FRICTIONANGLE_MEYERHOF_ERRORRETURN)
def ngamma_frictionangle_meyerhof(
        friction_angle,
        frictionangle_multiplier=1.4, **kwargs):
    """
    Calculates the bearing capacity factor Ngamma according to the equation proposed by Meyerhof (1976). This formulation is more conservative compared to the Vesic formulation.

    :param friction_angle: Peak drained friction angle (:math:`\\phi_p^{\\prime}`) [:math:`deg`] - Suggested range: 20.0 <= friction_angle <= 50.0
    :param frictionangle_multiplier: Multiplier on the friction angle (:math:`\\alpha_1`) [:math:`-`] (optional, default= 1.4)

    .. math::
        N_{\\gamma} = (N_q - 1) \\tan (1.4 \\phi_p^{\\prime})

    :returns: Dictionary with the following keys:

        - 'Ngamma [-]': Bearing capacity factor (:math:`N_{\\gamma}`)  [:math:`-`]

    Reference - Budhu (2011) Introduction to soil mechanics and foundations

    """

    _Ngamma = (nq_frictionangle_sand(friction_angle)['Nq [-]'] - 1.0) * np.tan(
        np.radians(frictionangle_multiplier * friction_angle))

    return {
        'Ngamma [-]': _Ngamma,
    }


NGAMMA_FRICTIONANGLE_DAVISBOOKER = {
    'friction_angle': {'type': 'float', 'min_value': 20.0, 'max_value': 50.0},
    'roughness_factor': {'type': 'float', 'min_value': 0.0, 'max_value': 1.0},
    'multiplier_smooth': {'type': 'float', 'min_value': None, 'max_value': None},
    'multiplier_rough': {'type': 'float', 'min_value': None, 'max_value': None},
    'multiplier_exp_smooth': {'type': 'float', 'min_value': None, 'max_value': None},
    'multiplier_exp_rough': {'type': 'float', 'min_value': None, 'max_value': None},
}

NGAMMA_FRICTIONANGLE_DAVISBOOKER_ERRORRETURN = {
    'Ngamma [-]': np.NaN,
    'Ngamma_smooth [-]': np.NaN,
    'Ngamma_rough [-]': np.NaN,
}


@Validator(NGAMMA_FRICTIONANGLE_DAVISBOOKER, NGAMMA_FRICTIONANGLE_DAVISBOOKER_ERRORRETURN)
def ngamma_frictionangle_davisbooker(
        friction_angle, roughness_factor,
        multiplier_smooth=0.0663, multiplier_rough=0.1054, multiplier_exp_smooth=9.3, multiplier_exp_rough=9.6,
        **kwargs):
    """
    Calculates the bearing capacity factor Ngamma according to the equation proposed by Davis and Booker (1971). This formulation is based on a more refined plasticity method and takes the roughness into account. This method is preferred in principle.

    :param friction_angle: Peak drained friction angle (:math:`\\phi_p^{\\prime}`) [:math:`deg`] - Suggested range: 20.0 <= friction_angle <= 50.0
    :param roughness_factor: Footing roughness factor where 0 is fully smooth and 1 is fully rough (:math:`R_{inter}`) [:math:`-`] - Suggested range: 0.0 <= roughness_factor <= 1.0
    :param multiplier_smooth: Multiplier for smooth footings (:math:`\\alpha_1`) [:math:`-`] (optional, default= 0.0663)
    :param multiplier_rough: Multiplier for rough footings (:math:`\\alpha_2`) [:math:`-`] (optional, default= 0.1054)
    :param multiplier_exp_smooth: Multiplier on exponential term for smooth footings (:math:`\\alpha_3`) [:math:`-`] (optional, default= 9.3)
    :param multiplier_exp_rough: Multiplier on exponential term for roughfootings (:math:`\\alpha_4`) [:math:`-`] (optional, default= 9.6)

    .. math::
        N_{\\gamma} = \\begin{cases}
            0.1054 \\exp (9.6 \\phi_p^{\\prime})       & \\quad \\text{for rough footings}\\\\
            0.0663 \\exp(9.3 \\phi_p^{\\prime})  & \\quad \\text{for smooth footings}
          \\end{cases}

    :returns: Dictionary with the following keys:

        - 'Ngamma [-]': Bearing capacity factor (:math:`N_{\\gamma}`)  [:math:`-`]
        - 'Ngamma_smooth [-]': Bearing capacity factor for smooth footing (:math:`N_{\\gamma,smooth}`)  [:math:`-`]
        - 'Ngamma_rough [-]': Bearing capacity factor for rough footing (:math:`N_{\\gamma,rough}`)  [:math:`-`]

    Reference - Budhu (2011) Introduction to soil mechanics and foundations

    """
    _Ngamma_smooth = multiplier_smooth * np.exp(multiplier_exp_smooth * np.radians(friction_angle))
    _Ngamma_rough = multiplier_rough * np.exp(multiplier_exp_rough * np.radians(friction_angle))
    _Ngamma = np.interp(roughness_factor, [0.0, 1.0], [_Ngamma_smooth, _Ngamma_rough])

    return {
        'Ngamma [-]': _Ngamma,
        'Ngamma_smooth [-]': _Ngamma_smooth,
        'Ngamma_rough [-]': _Ngamma_rough,
    }