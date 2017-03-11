#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

from pyeng.general.validation import ValidationDecorator
import numpy as np

PLASTICITY_CHART = {
    'liquid_limit': {'type': 'float', 'min_value': 0.0, 'max_value': 100.0},
    'plasticity_index': {'type': 'float', 'min_value': 0.0, 'max_value': 70.0},
}


@ValidationDecorator(PLASTICITY_CHART)
def plasticity_chart(liquid_limit, plasticity_index, fail_silently=True, **kwargs):
    """
    Classification of fine-grained soils according to their plasticity. The plasticity chart comprises six regions divided by the so-called A-line. Soil above the A-line are inorganic clays and soils below the A-line are inorganic silts, organic silts or organic clays.

    :param liquid_limit: Liquid limit (:math:`w_L`) [:math:`\%`]  - Suggested range: 0.0<=liquid_limit<=100.0
    :param plasticity_index: Plasticity index (:math:`PI`) [:math:`\%`]  - Suggested range: 0.0<=plasticity_index<=70.0

    .. math::
        PI = 0.73 (w_L - 20)

    :returns:   Classification [:math:`-`], Aline plasticity index (:math:`PI_{Aline}`) [:math:`\%`]

    :rtype: Python dictionary with keys ['classification [-]','aline_PI [%]']

    .. figure:: images/Casagrande_chart.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Plasticity chart according to Casagrande (1948)

    Reference - Casagrande, A. (1948). Classification and Identification of Soils. Transaction, ASCE, vol. 113, 901-930.

    """

    try:

        if not kwargs['validated']:
            raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

        if liquid_limit < 20.0:
            aline_PI = 0.0
        else:
            aline_PI = 0.73 * (liquid_limit - 20.0)

        if liquid_limit < 30.0:
            if plasticity_index < aline_PI:
                classification = "Inorganic Silts of Low Compressibility"
            else:
                classification = "Inorganic Clays of Low Plasticity"
        elif 30.0 <= liquid_limit < 50.0:
            if plasticity_index < aline_PI:
                classification = "Inorganic Silts of Medium Comprssibility and Organic Silts"
            else:
                classification = "Inorganic Clays of Medium Plasticity"
        else:
            if plasticity_index < aline_PI:
                classification = "Inorganic Silts of High Comprssibility and Organic Clays"
            else:
                classification = "Inorganic Clays of High Plasticity"

        return {
            'classification [-]': classification,
            'aline_PI [%]': aline_PI,
        }

    except:
        if fail_silently or fail_silently is None:
            return {
                'classification [-]': None,
                'aline_PI [%]': np.NaN,
            }
        else:
            raise