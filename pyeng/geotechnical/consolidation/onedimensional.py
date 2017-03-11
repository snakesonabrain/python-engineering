#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

from pyeng.general.validation import ValidationDecorator
import numpy as np

CONSOLIDATION_DRAINAGE_JANBU = {
    'time': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'consolidation_coefficient': {'type': 'float', 'min_value': 0.1, 'max_value': 10000.0},
    'drainage_path_length': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'drainage_type': {'type': 'string', 'options': ("single", "double"), 'regex': None},
    'stress_distribution': {'type': 'string', 'options': ("constant", "triangular increasing", "triangular decreasing"),
                            'regex': None},
}


@ValidationDecorator(CONSOLIDATION_DRAINAGE_JANBU)
def consolidation_drainage_janbu(time, consolidation_coefficient, drainage_path_length, drainage_type="double",
                                 stress_distribution="constant", fail_silently=True, **kwargs):
    """
    Calculates the average degree of consolidation for different drainage characteristics and initial stress distribution. For double drainage, an analytical solution is obtained by curve fitting to the numerical solution. For triangular stress distribution and double drainage, the same solution as for a constant stress distribution and double drainage is obtained. For one-sided drainage, this is no longer the case. For one-sided drainage and triangular stress distributions, the chart according to Janbu (1956) is interpolated.

    In a thin layer of partially drained soil, a uniform stress distribution applies. In deep homogeneous clay, a triangular stress distribution, decreasing with depth applies.

    Note that the drainage path length is half of the layer thickness for double drainage and equal to the layer thickness for single-sided drainage.

    :param time: Drainage time (:math:`t`) [:math:`s`]  - Suggested range: 0.0<=time
    :param consolidation_coefficient: Coefficient of consolidation (:math:`c_v`) [:math:`m2/yr`]  - Suggested range: 0.1<=consolidation_coefficient<=10000.0
    :param drainage_path_length: The length of the drainage path (:math:`H_{dr}`) [:math:`m`]  - Suggested range: 0.0<=drainage_path_length
    :param drainage_type: Double-sided or single-sided drainage (:math:`-`) [:math:`-`] (optional, default="double")Options: ("constant","triangular increasing","triangular decreasing"), regex: None
    :param stress_distribution: Type of initial stress distribution (:math:`-`) [:math:`-`] (optional, default="constant")Options: ("constant","triangular increasing","triangular decreasing"), regex: None

    .. math::
        T_v = \\frac{c_v t}{H_{dr}^2}

        \\text{Double drainage: }

        T_v = \\frac{\\pi}{4} (\\frac{U}{100})^2 \\quad U < 60\\%

        T_v = 1.781 - 0.933 \\log(100 - U) \\quad U \\geq 60\\%

    :returns:   Average degree of consolidation (:math:`U`) [:math:`%`], Time factor (:math:`T_v`) [:math:`-`]

    :rtype: Python dictionary with keys ['consolidation_degree [%]','time_factor [-]']

    .. figure:: images/consolidation_drainage_janbu.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Solutions for one-dimensional consolidation equation for different consolidation characteristics and stress distributions

    Reference - Janbu (1956).

    """

    try:

        if not kwargs['validated']:
            raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

        # Calculation statements
        time_factor = ((consolidation_coefficient / (365.0 * 24.0 * 3600.0)) * time) / (drainage_path_length ** 2.0)

        if drainage_type == "double":
            consolidation_degree = np.interp(np.log10(time_factor),
                                             [-3.02247191011236, -2.75280898876405, -2.48876404494382,
                                              -2.32022471910112, -2.13483146067416, -1.9438202247191, -1.76404494382023,
                                              -1.55056179775281, -1.32022471910112, -1.14044943820225,
                                              -0.966292134831463, -0.808988764044945, -0.691011235955056,
                                              -0.606741573033708, -0.516853932584271, -0.387640449438202,
                                              -0.280898876404495, -0.179775280898877, -7.86516853932586E-02,
                                              5.05617977528079E-02, 0.191011235955055, 0.348314606741571,
                                              0.494382022471909],
                                             [2.95554469956033, 4.91548607718612, 6.87445041524182, 8.81680508060576,
                                              10.4142647777235, 13.0561797752809, 15.696140693698, 19.9071812408402,
                                              25.3385442110405, 31.4567659990229, 38.2696629213483, 44.905715681485,
                                              51.7088422081094, 56.7669760625305, 62.8695652173913, 71.2398632144601,
                                              77.867122618466, 84.3194919394235, 89.9022960429897, 93.9247679531021,
                                              97.2535417684416, 99.3678553981436, 100.0])
        else:
            if stress_distribution == "constant":
                consolidation_degree = np.interp(np.log10(time_factor),
                                                 [-3.02247191011236, -2.75280898876405, -2.48876404494382,
                                                  -2.32022471910112, -2.13483146067416, -1.9438202247191,
                                                  -1.76404494382023,
                                                  -1.55056179775281, -1.32022471910112, -1.14044943820225,
                                                  -0.966292134831463, -0.808988764044945, -0.691011235955056,
                                                  -0.606741573033708, -0.516853932584271, -0.387640449438202,
                                                  -0.280898876404495, -0.179775280898877, -7.86516853932586E-02,
                                                  5.05617977528079E-02, 0.191011235955055, 0.348314606741571,
                                                  0.494382022471909],
                                                 [2.95554469956033, 4.91548607718612, 6.87445041524182,
                                                  8.81680508060576,
                                                  10.4142647777235, 13.0561797752809, 15.696140693698, 19.9071812408402,
                                                  25.3385442110405, 31.4567659990229, 38.2696629213483, 44.905715681485,
                                                  51.7088422081094, 56.7669760625305, 62.8695652173913,
                                                  71.2398632144601,
                                                  77.867122618466, 84.3194919394235, 89.9022960429897, 93.9247679531021,
                                                  97.2535417684416, 99.3678553981436])
            elif stress_distribution == "triangular increasing":
                consolidation_degree = np.interp(np.log10(time_factor),
                                                 [-2.07303370786517, -1.79213483146068, -1.52808988764045,
                                                  -1.33707865168539, -1.1685393258427, -1.01123595505618,
                                                  -0.876404494382024, -0.764044943820226, -0.679775280898877,
                                                  -0.601123595505619, -0.51123595505618, -0.432584269662921,
                                                  -0.342696629213483, -0.264044943820225, -0.179775280898877,
                                                  -0.106741573033708, 0, 0.117977528089886, 0.241573033707864,
                                                  0.365168539325842, 0.499999999999999],
                                                 [0.511968734733757, 3.34342940889106, 6.69369809477284,
                                                  10.3790913531998, 14.7562286272594, 20.6966292134831,
                                                  26.8070346849047, 32.9135319980459, 39.5368832437713,
                                                  45.4636052760136, 52.609672691744, 58.8842208109428, 66.3781143136297,
                                                  72.4787493893502, 78.9281875915974, 85.0278456277479,
                                                  90.7855398143624, 94.6321446018563, 97.2623351245725,
                                                  99.1968734733756, 100.0])
            elif stress_distribution == "triangular decreasing":
                consolidation_degree = np.interp(np.log10(time_factor),
                                                 [-3.01685393258427, -2.75280898876405, -2.53932584269663,
                                                  -2.3314606741573, -2.09550561797753, -1.89887640449438,
                                                  -1.62921348314607, -1.38202247191011, -1.13483146067416,
                                                  -0.955056179775282, -0.769662921348315, -0.629213483146068,
                                                  -0.48876404494382, -0.303370786516854, -0.185393258426966,
                                                  -6.17977528089892E-02, 0.056179775280898, 0.151685393258425,
                                                  0.264044943820223],
                                                 [9.56521739130434, 11.3502686858817, 13.648265754763, 16.2931118710307,
                                                  20.1602344894968, 24.3683439179286, 30.6761113825109,
                                                  38.0234489496824, 46.2403517342452, 53.923790913532, 61.4342940889105,
                                                  68.4152418172935, 75.04836345872, 83.0806057645334, 88.3185148998534,
                                                  93.0356619443087, 96.3605276013678, 98.8119198827552, 100.0])
            else:
                raise ValueError("Stress distribution not recognized, please check the documentation.")

        return {
            'consolidation_degree [%]': consolidation_degree,
            'time_factor [-]': time_factor,
        }

    except:
        if fail_silently or fail_silently is None:
            return {
                'consolidation_degree [%]': np.NaN,
                'time_factor [-]': np.NaN,
            }
        else:
            raise