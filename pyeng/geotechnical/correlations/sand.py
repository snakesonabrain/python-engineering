#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

from pyeng.general.validation import ValidationDecorator
import numpy as np

FRICTIONANGLE_OVERBURDEN_KLEVEN = {
    'sigma_vo_eff': {'type': 'float', 'min_value': 10.0, 'max_value': 800.0},
    'relative_density': {'type': 'float', 'min_value': 40.0, 'max_value': 100.0},
    'Ko': {'type': 'float', 'min_value': 0.3, 'max_value': 2.0},
    'max_friction_angle': {'type': 'float', 'min_value': None, 'max_value': None},
}


@ValidationDecorator(FRICTIONANGLE_OVERBURDEN_KLEVEN)
def frictionangle_overburden_kleven(sigma_vo_eff, relative_density, Ko=0.5, max_friction_angle=45.0, fail_silently=True,
                                    **kwargs):
    """
    This function calculates the friction angle according to the chart proposed by Kleven (1986). The function takes into account the effective confining pressure of the sand and its relative density. The function was calibrated on North Sea sand tests with confining pressures ranging from 10 to 800kPa. Lower confinement clearly leads to higher friction angles. The fit to the data is not excellent and this function should be compared to site-specific testing or other correlations.


    :param sigma_vo_eff: Effective vertical stress (:math:`\\sigma \\prime _{vo}`) [:math:`kPa`]  - Suggested range: 10.0<=sigma_vo_eff<=800.0
    :param relative_density: Relative density of sand (:math:`D_r`) [:math:`Percent`]  - Suggested range: 40.0<=relative_density<=100.0
    :param Ko: Coefficient of lateral earth pressure at rest (:math:`K_o`) [:math:`-`] (optional, default=0.5) - Suggested range: 0.3<=Ko<=2.0
    :param max_friction_angle: The maximum allowable effective friction angle (:math:`\\phi \\prime _{max}`) [:math:`deg`] (optional, default=45.0)

    :returns:   Peak drained friction angle (:math:`\\phi_d`) [:math:`deg`], Mean effective stress (:math:`\\sigma \\prime _m`) [:math:`kPa`]

    :rtype: Python dictionary with keys ['phi [deg]','sigma_m [kPa]']

    .. figure:: images/Phi_Kleven.png
        :figwidth: 500
        :width: 400
        :align: center

        Data and interpretation chart according to Kleven (Lunne et al (1997))

    Reference - Lunne, T., Robertson, P.K., Powell, J.J.M. (1997). Cone penetration testing in geotechnical practice.  SPON press

    Examples:
        .. code-block:: python

            >>>phi = friction_angle_kleven(sigma_vo_eff=100.0,relative_density=60.0,Ko=1.0)['phi [deg]']
            35.8

    """

    try:

        if not kwargs['validated']:
            raise ValueError("Error during function validation: %s" % kwargs['errorstring'])

        # Calculation statements
        sigma_m = ((1.0 + 2.0 * Ko) / 3.0) * sigma_vo_eff

        if relative_density > 100.0:
            relative_density = 100.0

        if sigma_m < 10.0:
            phi = 0.2183 * relative_density + 25.667
        elif sigma_m >= 10.0 and sigma_m < 25.0:
            phi1 = 0.2183 * relative_density + 25.667
            phi2 = 0.2175 * relative_density + 24.75
            phi = phi1 + ((phi2 - phi1) / (25.0 - 10.0)) * (sigma_m - 10.0)
        elif sigma_m >= 25.0 and sigma_m < 50.0:
            phi1 = 0.2175 * relative_density + 24.75
            phi2 = 0.22 * relative_density + 23.5
            phi = phi1 + ((phi2 - phi1) / (50.0 - 25.0)) * (sigma_m - 25.0)
        elif sigma_m >= 50.0 and sigma_m < 100.0:
            phi1 = 0.22 * relative_density + 23.5
            phi2 = 0.2175 * relative_density + 22.75
            phi = phi1 + ((phi2 - phi1) / (100.0 - 50.0)) * (sigma_m - 50.0)
        elif sigma_m >= 100.0 and sigma_m < 200.0:
            phi1 = 0.2175 * relative_density + 22.75
            phi2 = 0.2 * relative_density + 23.0
            phi = phi1 + ((phi2 - phi1) / (200.0 - 100.0)) * (sigma_m - 100.0)
        elif sigma_m >= 200.0 and sigma_m < 400.0:
            phi1 = 0.2 * relative_density + 23
            phi2 = 0.1925 * relative_density + 22.75
            phi = phi1 + ((phi2 - phi1) / (400.0 - 200.0)) * (sigma_m - 200.0)
        elif sigma_m >= 400.0 and sigma_m < 800.0:
            phi1 = 0.1925 * relative_density + 22.75
            phi2 = 0.195 * relative_density + 21.3
            phi = phi1 + ((phi2 - phi1) / (800.0 - 400.0)) * (sigma_m - 400.0)

        phi = min(phi, max_friction_angle)

        return {
            'phi [deg]': phi,
            'sigma_m [kPa]': sigma_m,
        }

    except Exception as err:
        if fail_silently or fail_silently is None:
            return {
                'phi [deg]': np.NaN,
                'sigma_m [kPa]': np.NaN,
            }
        else:
            raise


LATERALEARTHPRESSURE_RELATIVEDENSITY_BELLOTTI = {
    'relative_density': {'type': 'float', 'min_value': 20.0, 'max_value': 100.0},
}


@ValidationDecorator(LATERALEARTHPRESSURE_RELATIVEDENSITY_BELLOTTI)
def lateralearthpressure_relativedensity_bellotti(relative_density, fail_silently=True, **kwargs):
    """
    Calculates the coefficient of lateral earth pressure at rest from sand relative density. The underlying data was gathered using calibration chamber testing on sands of different relative density.

    :param relative_density: Relative density of sand (:math:`D_r`) [:math:`\%`]  - Suggested range: 20.0<=relative_density<=100.0

    :returns:   Coefficient at lateral earth pressure at rest (:math:`Ko`) [:math:`-`]

    :rtype: Python dictionary with keys ['Ko [-]']

    .. figure:: images/lateralearthpressure_relativedensity_bellotti.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Coefficient of lateral earth pressure at rest for normally consolidated sand based on relative density

    Reference - Bellotti et al. (1985). Laboratory validation of in-situ tests. Italian Geotechnical Society Jubilee Volume, XI ICSMFE, San Francisco

    """

    try:

        if not kwargs['validated']:
            raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

        Ko = np.interp(relative_density,
                       [19.3421756638788, 21.026724113654915, 22.858269268677304, 24.98493424572667, 27.41347751400974,
                        29.989017487539066, 32.86193010616428, 35.884092253104676, 38.75249922559207, 41.16752555546169,
                        43.73405423671538, 45.99645180366647, 49.16223142124975, 52.025006336064884, 55.18965954211371,
                        57.75055616569515, 60.76145419729098, 64.67573427951902, 67.83588183943004, 70.99940863394443,
                        74.46143448508914, 77.0189518740672, 80.47985131367744, 84.24262904452144, 87.70352848413168,
                        90.86254963250826, 94.47495142350257, 98.23547633127762, 99.43961026160909],
                        [0.6584269662921348, 0.6280898876404495, 0.601123595505618, 0.5797752808988764, 0.5573033707865169,
                         0.5382022471910113, 0.5224719101123596, 0.5078651685393258, 0.4966292134831461, 0.4876404494382023,
                         0.4775280898876405, 0.47078651685393264, 0.46292134831460674, 0.45730337078651684, 0.450561797752809,
                         0.4460674157303371, 0.4426966292134832, 0.43820224719101125, 0.4359550561797753, 0.43033707865168547,
                         0.4269662921348315, 0.42584269662921354, 0.42359550561797754, 0.42022471910112363, 0.41797752808988764,
                         0.41685393258426967, 0.41348314606741576, 0.41235955056179774, 0.41123595505617977]
        )

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

