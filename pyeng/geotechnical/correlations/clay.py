#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

from pyeng.general.validation import ValidationDecorator
import numpy as np

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

