#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

from pyeng.general.validation import ValidationDecorator
import numpy as np

STRESSES_POINTLOAD_BOUSSINESQ = {
    'point_load': {'type': 'float', 'min_value': None, 'max_value': None},
    'x': {'type': 'float', 'min_value': None, 'max_value': None},
    'y': {'type': 'float', 'min_value': None, 'max_value': None},
    'z': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'poisson_coefficient': {'type': 'float', 'min_value': 0.0, 'max_value': 0.5},
}

@ValidationDecorator(STRESSES_POINTLOAD_BOUSSINESQ)
def stresses_pointload_boussinesq(point_load, x, y, z, poisson_coefficient=0.3, fail_silently=True, **kwargs):
    """
    Calculates stresses in a linear elastic half space due to a point load. Although most geotechnical material behave in a non-linear manner, these formulae can be applied provided that the hypothesis of linear elasticity is a reasonable approximation for the actual behaviour of the soil.

    :param point_load: Point load acting on the half-space (:math:`P`) [:math:`kPa`]
    :param x: x-coordinate of the point where stresses are calculated (:math:`x`) [:math:`m`]
    :param y: y-coordinate of the point where stresses are calculated (:math:`y`) [:math:`m`]
    :param z: z-coordinate of the point where stresses are calculated (:math:`z`) [:math:`m`]  - Suggested range: 0.0<=z
    :param poisson_coefficient: Poisson coefficient (:math:`\\nu`) [:math:`-`] (optional, default=0.3) - Suggested range: 0.0<=poisson_coefficient<=0.5

    .. math::
        \\sigma_z = \\frac{3P}{2 \\pi} \\cdot \\frac{z^3}{R^5}

        \\sigma_x = \\frac{3P}{2 \\pi} \\left[ \\frac{x^2 z}{R^5} + \\frac{1 - 2 \\nu}{3} \\left( - \\frac{1}{R (R + z)} - \\frac{x^2 (2R + z)}{R^3 (R +z)^2} - \\frac{z}{R^3} \\right) \\right]

        \\sigma_y = \\frac{3P}{2 \\pi} \\left[ \\frac{y^2 z}{R^5} + \\frac{1 - 2 \\nu}{3} \\left( - \\frac{1}{R (R + z)} - \\frac{y^2 (2R + z)}{R^3 (R +z)^2} - \\frac{z}{R^3} \\right) \\right]

        \\tau_{zx} = - \\frac{3 P}{2 \\pi} \\frac{x z^2}{R^5}

        \\tau_{yz} = - \\frac{3 P}{2 \\pi} \\frac{y z^2}{R^5}

        \\tau_{xy} = - \\frac{3 P}{2 \\pi} \\left( \\frac{x y z}{R^5} - \\frac{1 - 2 \\nu}{3} \\frac{x y (2R + z)}{R^3 (R + z)^2} \\right)

        r = \\sqrt{x^2 + y^2}

        R = \\sqrt{r^2 + z^2}

    :returns:   Normal stress in the z-direction (:math:`\\sigma_z`) [:math:`kPa`], Normal stress in the x-direction (:math:`\\sigma_x`) [:math:`kPa`], Normal stress in the y-direction (:math:`\\sigma_y`) [:math:`kPa`], Shear stress normal to the z-direction acting in the x-direction (:math:`\\tau_{zx}`) [:math:`kPa`], Shear stress normal to the y-direction acting in the z-direction (:math:`\\tau_{yz}`) [:math:`kPa`], Shear stress normal to the x-direction acting in the y-direction (:math:`\\tau_{xy}`) [:math:`kPa`], Distance from point load to point at which stresses are calculated (:math:`R`) [:math:`m`]

    :rtype: Python dictionary with keys ['sigma_z [kPa]','sigma_x [kPa]','sigma_y [kPa]','tau_zx [kPa]','tau_yz [kPa]','tau_xy [kPa]','radius [m]']

    .. figure:: images/stresses_pointload_boussinesq.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Coordinate system and sign convention for point load acting on an elastic half-space

    Reference - Boussinesq J. (1885). Application des potentiels a l'etude de l'equilibre et du mouvement des solides elastiques. Gauthier-Villar. Paris

    """

    try:

        if not kwargs['validated']:
            raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

        radius_xy = np.sqrt(x**2.0 + y**2.0)
        radius = np.sqrt(radius_xy**2.0 + z**2.0)

        sigma_z = ((3.0*point_load)/(2.0*np.pi))*((z**3.0)/(radius**5.0))
        sigma_x = ((3.0*point_load)/(2.0*np.pi)) * \
                  ((((x**2.0) * z)/(radius**5.0)) + ((1.0 - 2.0*poisson_coefficient)/3.0) *
                   (-(1.0/(radius * (radius + z))) -
                    (((x**2.0)*(2.0*radius + z))/((radius**3.0)*((radius + z)**2.0))) -
                    (z/(radius**3.0))))
        sigma_y = ((3.0 * point_load) / (2.0 * np.pi)) * \
                  ((((y ** 2.0) * z) / (radius ** 5.0)) + ((1.0 - 2.0 * poisson_coefficient) / 3.0) *
                   (-(1.0 / (radius * (radius + z))) -
                    (((y ** 2.0) * (2.0 * radius + z)) / ((radius ** 3.0) * ((radius + z) ** 2.0))) -
                    (z / (radius ** 3.0))))
        tau_zx = -((3.0 * point_load) / (2.0 * np.pi)) * \
                  ((x * (z ** 2.0))/(radius**5.0))
        tau_yz = -((3.0 * point_load) / (2.0 * np.pi)) * \
                  ((y * (z ** 2.0)) / (radius ** 5.0))
        tau_xy = ((3.0 * point_load) / (2.0 * np.pi)) * \
                 (((x*y*z) / (radius ** 5.0)) -
                  ((1.0 - 2.0 * poisson_coefficient)/3.0)*((x*y*(2.0*radius + z))/((radius**3.0)*((radius + z)**2.0))))

        return {
            'sigma_z [kPa]': sigma_z,
            'sigma_x [kPa]': sigma_x,
            'sigma_y [kPa]': sigma_y,
            'tau_zx [kPa]': tau_zx,
            'tau_yz [kPa]': tau_yz,
            'tau_xy [kPa]': tau_xy,
            'radius [m]': radius,
        }

    except:
        if fail_silently or fail_silently is None:
            return {
                'sigma_z [kPa]': np.NaN,
                'sigma_x [kPa]': np.NaN,
                'sigma_y [kPa]': np.NaN,
                'tau_zx [kPa]': np.NaN,
                'tau_yz [kPa]': np.NaN,
                'tau_xy [kPa]': np.NaN,
                'radius [m]': np.NaN,
            }
        else:
            raise

STRESSES_LINELOAD_BOUSSINESQ = {
    'line_load': {'type': 'float', 'min_value': None, 'max_value': None},
    'x': {'type': 'float', 'min_value': None, 'max_value': None},
    'z': {'type': 'float', 'min_value': 0.0, 'max_value': None},
}

@ValidationDecorator(STRESSES_LINELOAD_BOUSSINESQ)
def stresses_lineload_boussinesq(line_load, x, z, fail_silently=True, **kwargs):
    """
    Calculates stresses in an elastic half-space due to a line load acting at the surface.

    :param line_load: Magnitude of the line load (:math:`P`) [:math:`kN/m`]
    :param x: x-coordinate of the point where stresses are calculated (:math:`x`) [:math:`m`]
    :param z: z-coordinate of the point where stresses are calculated (:math:`z`) [:math:`m`]  - Suggested range: 0.0<=z

    .. math::
        \\sigma_z = \\frac{2 P z^3}{\\pi (x^2 + z^2)^2}

        \\sigma_x = \\frac{2 P x^2 z}{\\pi (x^2 + z^2)^2}

        \\tau_{zx} = \\frac{2 P x z^2}{\\pi (x^2 + z^2)^2}

    :returns:   Vertical normal stress (:math:`\\sigma_z`) [:math:`kPa`], Horizontal normal stress (:math:`\\sigma_x`) [:math:`kPa`], Shear stress normal to the z-direction acting in the x-direction (:math:`\\tau_{zx}`) [:math:`kPa`]

    :rtype: Python dictionary with keys ['sigma_z [kPa]','sigma_x [kPa]','tau_zx [kPa]']

    .. figure:: images/stresses_lineload_boussinesq.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Nomenclature and sign convention for stresses in an elastic half-space due to a line load

    Reference - Boussinesq J. (1885). Application des potentiels a l'etude de l'equilibre et du mouvement des solides elastiques. Gauthier-Villar. Paris

    """

    try:

        if not kwargs['validated']:
            raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

        sigma_z = (2.0 * line_load * z**3.0)/(np.pi * (x**2.0 + z**2.0)**2.0)
        sigma_x = (2.0 * line_load * (x**2.0) * z)/(np.pi * (x**2.0 + z**2.0)**2.0)
        tau_zx = (2.0 * line_load * x * (z ** 2.0)) / (np.pi * (x ** 2.0 + z ** 2.0) ** 2.0)

        return {
            'sigma_z [kPa]': sigma_z,
            'sigma_x [kPa]': sigma_x,
            'tau_zx [kPa]': tau_zx,
        }

    except:
        if fail_silently or fail_silently is None:
            return {
                'sigma_z [kPa]': np.NaN,
                'sigma_x [kPa]': np.NaN,
                'tau_zx [kPa]': np.NaN,
            }
        else:
            raise

STRESSES_STRIPLOADCONSTANT_BOUSSINESQ = {
    'strip_load': {'type': 'float', 'min_value': None, 'max_value': None},
    'load_width': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'x': {'type': 'float', 'min_value': None, 'max_value': None},
    'z': {'type': 'float', 'min_value': 0.0, 'max_value': None},
}

@ValidationDecorator(STRESSES_STRIPLOADCONSTANT_BOUSSINESQ)
def stresses_striploadconstant_boussinesq(strip_load, load_width, x, z, fail_silently=True, **kwargs):
    """
    Calculates the increase in stress at a point in an elastic halfspace due to a strip load of constant magnitude.

    :param strip_load: Magnitude of the constant strip load (:math:`q`) [:math:`kPa`]
    :param load_width: Width over which the strip load is acting (:math:`B`) [:math:`m`]  - Suggested range: 0.0<=load_width
    :param x: x-coordinate of the point where stresses are calculated (:math:`x`) [:math:`m`]
    :param z: z-coordinate of the point where stresses are calculated (:math:`z`) [:math:`m`]  - Suggested range: 0.0<=z

    .. math::
        \\sigma_z = \\frac{q}{\\pi} \\left[ \\alpha + \\sin \\alpha \\cos(\\alpha + 2 \\beta) \\right]

        \\sigma_x = \\frac{q}{\\pi} \\left[ \\alpha - \\sin \\alpha \\cos(\\alpha + 2 \\beta) \\right]

        \\tau_{zx} = \\frac{q}{\\pi} \\left[ \\sin \\alpha \\sin ( \\alpha + 2 \\beta) \\right]

    :returns:   Vertical normal stress (:math:`\\sigma_z`) [:math:`kPa`], Horizontal normal stress (:math:`\\sigma_x`) [:math:`kPa`], Shear stress (:math:`\\tau_{zx}`) [:math:`kPa`]

    :rtype: Python dictionary with keys ['sigma_z [kPa]','sigma_x [kPa]','tau_zx [kPa]']

    .. figure:: images/stresses_striploadconstant_boussinesq.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Nomenclature and sign convention for stress calculation

    Reference - Boussinesq J. (1885). Application des potentiels a l'etude de l'equilibre et du mouvement des solides elastiques. Gauthier-Villar. Paris

    """

    try:

        if not kwargs['validated']:
            raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

        beta = np.arctan((x - load_width) / z)
        alpha = np.arctan(x / z) - beta

        sigma_z = (strip_load/np.pi) * (alpha +
                                        np.sin(alpha)*np.cos(alpha + 2.0*beta))
        sigma_x = (strip_load / np.pi) * (alpha -
                                          np.sin(alpha) * np.cos(alpha + 2.0 * beta))
        tau_zx = (strip_load / np.pi) * (np.sin(alpha)*np.sin(alpha + 2.0*beta))

        return {
            'sigma_z [kPa]': sigma_z,
            'sigma_x [kPa]': sigma_x,
            'tau_zx [kPa]': tau_zx,
        }

    except:
        if fail_silently or fail_silently is None:
            return {
                'sigma_z [kPa]': np.NaN,
                'sigma_x [kPa]': np.NaN,
                'tau_zx [kPa]': np.NaN,
            }
        else:
            raise

STRESSES_STRIPLOADTRIANGULAR_BOUSSINESQ = {
    'strip_load_max': {'type': 'float', 'min_value': None, 'max_value': None},
    'load_width': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'x': {'type': 'float', 'min_value': None, 'max_value': None},
    'z': {'type': 'float', 'min_value': None, 'max_value': None},
}

@ValidationDecorator(STRESSES_STRIPLOADTRIANGULAR_BOUSSINESQ)
def stresses_striploadtriangular_boussinesq(strip_load_max, load_width, x, z, fail_silently=True, **kwargs):
    """
    Calculates the increase in stress at a point in an elastic halfspace due to a strip load with triangular stress distribution

    :param strip_load_max: Maximum value of the strip load acting on the halfspace (:math:`q`) [:math:`kPa`]
    :param load_width: Width over which the strip load is acting (:math:`B`) [:math:`m`]  - Suggested range: 0.0<=load_width
    :param x: x-coordinate of the point where stresses are calculated (:math:`x`) [:math:`m`]
    :param z: z-coordinate of the point where stresses are calculated (:math:`z`) [:math:`m`]

    .. math::
        \\sigma_z = \\frac{q}{\\pi} \\left( \\frac{x}{B} \\alpha - \\frac{1}{2} \\sin 2 \\beta \\right)

        \\sigma_x = \\frac{q}{\\pi} \\left( \\frac{x}{B} \\alpha  - \\frac{z}{B} \\ln{\\frac{R_1^2}{R_2^2}} + \\frac{1}{2} \\sin 2 \\beta \\right)

        \\tau_{zx} = \\frac{q}{2 \\pi} \\left( 1 + \\cos 2 \\beta - 2 \\frac{z}{B} \\alpha \\right)

    :returns:   Vertical normal stress (:math:`\\sigma_z`) [:math:`kPa`], Horizontal normal stress (:math:`\\sigma_x`) [:math:`kPa`], Shear stress (:math:`\\tau_{zx}`) [:math:`kPa`]

    :rtype: Python dictionary with keys ['sigma_z [kPa]','sigma_x [kPa]','tau_zx [kPa]']

    .. figure:: images/stresses_striploadtriangular_boussinesq.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Nomenclature and sign convention for stresses due to a triangular strip load

    Reference - Boussinesq J. (1885). Application des potentiels a l'etude de l'equilibre et du mouvement des solides elastiques. Gauthier-Villar. Paris

    """

    try:

        if not kwargs['validated']:
            raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

        beta = np.arctan((x - load_width) / z)
        alpha = np.arctan(x / z) - beta
        r1 = np.sqrt(x**2.0 + z**2.0)
        r2 = np.sqrt((x-load_width)**2.0 + z**2.0)
        sigma_z = (strip_load_max/np.pi) * ((x/load_width)*alpha - 0.5*np.sin(2.0*beta))
        sigma_x = (strip_load_max/np.pi) * ((x/load_width)*alpha -
                                            (z/load_width)*np.log((r1**2.0)/(r2**2.0)) +
                                            0.5*np.sin(2.0*beta))
        tau_zx = (strip_load_max/(2.0 * np.pi)) * (1.0 + np.cos(2.0*beta) - (2.0*alpha*z/load_width))

        return {
            'sigma_z [kPa]': sigma_z,
            'sigma_x [kPa]': sigma_x,
            'tau_zx [kPa]': tau_zx,
        }

    except:
        if fail_silently or fail_silently is None:
            return {
                'sigma_z [kPa]': np.NaN,
                'sigma_x [kPa]': np.NaN,
                'tau_zx [kPa]': np.NaN,
            }
        else:
            raise


STRESSES_CIRCLE_BOUSSINESQ = {
    'circle_stress': {'type': 'float', 'min_value': None, 'max_value': None},
    'circle_radius': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'z': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'radius': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'poisson_coefficient': {'type': 'float', 'min_value': 0.0, 'max_value': 0.5},
}


@ValidationDecorator(STRESSES_CIRCLE_BOUSSINESQ)
def stresses_circle_boussinesq(circle_stress, circle_radius, z, radius=0.0, poisson_coefficient=0.3, fail_silently=True,
                               **kwargs):
    """
    Calculates the increase in stress below a uniformy loaded circular area on elastic soil. For points below the center, a closed-form solution exists. For points off center, the vertical normal stress increase is obtained from a chart derived from finite element simulations.  The function does not return radial and tangential stresses for points off center. The interpolation is limited to :math:`z/R = 15` and :math:`r/R = 10`.

    :param circle_stress: Uniform stress acting on the circular area (:math:`q`) [:math:`kPa`]
    :param circle_radius: Radius of the circle (:math:`R`) [:math:`m`]  - Suggested range: 0.0<=circle_radius
    :param z: z-coordinate of the point where stresses are calculated (:math:`z`) [:math:`m`]  - Suggested range: 0.0<=z
    :param radius: Radial distance from circle center to point where stresses are calculated (:math:`r`) [:math:`m`] (optional, default=0.0) - Suggested range: 0.0<=radius
    :param poisson_coefficient: Poisson's coefficient (:math:`\\nu`) [:math:`-`] (optional, default=0.3) - Suggested range: 0.0<=poisson_coefficient<=0.5

    .. math::
        \\sigma_z = q \\left[ 1 - \\left( \\frac{1}{1 + (R/z)^2} \\right)^{3/2} \\right]

        \\sigma_r = \\sigma_{\\theta} = \\frac{q}{2} \\left[ (1 + 2 \\nu) - \\frac{4 (1 + \\nu)}{\\left[ 1 + (R/z)^2 \\right]^{1/2}} + \\frac{1}{\\left[ 1 + (R/z)^2 \\right]^{3/2}} \\right]

    :returns:   Vertical stress (:math:`\\sigma_z`) [:math:`kPa`], Radial stress (:math:`\\sigma_r`) [:math:`kPa`], Circumferential stress (:math:`\\sigma_{theta}`) [:math:`kPa`]

    :rtype: Python dictionary with keys ['sigma_z [kPa]','sigma_r [kPa]','sigma_theta [kPa]']

    .. figure:: images/stresses_circle_boussinesq.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Interpolation chart for points vertical normal stress below a uniformly loaded circular area

    Reference - Boussinesq J. (1885). Application des potentiels a l'etude de l'equilibre et du mouvement des solides elastiques. Gauthier-Villar. Paris

    """

    try:

        if not kwargs['validated']:
            raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

        if radius==0.0:
            sigma_z = circle_stress * (1.0 - ((1.0 / (1.0 + (circle_radius / z) ** 2.0)) ** 1.5))
            sigma_r = 0.5 * circle_stress * ((1.0 + 2.0 * poisson_coefficient) -
                                             ((4.0 * (1.0 + poisson_coefficient)) / (
                                             (1.0 + (circle_radius / z) ** 2.0) ** 0.5)) +
                                             (1.0 / ((1.0 + (circle_radius / z) ** 2.0) ** 1.5)))
            sigma_theta = sigma_r
        else:
            sigma_r = np.NaN
            sigma_theta = np.NaN
            z_dimless = z/circle_radius
            r_dimless = radius/circle_radius
            if r_dimless > 10.0 or z_dimless > 15.0:
                raise ValueError("Radius or depth coordinate outside interpolation limits")
            if 0.0 < r_dimless <= 0.5:
                mult_1 = 10.0**(np.interp(z_dimless,
                                          [0.0, 0.457145182849504, 0.770761216026322, 1.11255869349144, 1.68192411831236,
                                           2.25156801590293, 2.87835452582513, 3.70491740069232, 4.56049713815676,
                                           5.67299585289783, 6.58605237001748, 7.6419654179662, 8.92639322068753,
                                           10.6391678376803, 11.6099239126709, 12.7234251293827, 13.9226402645919,
                                           14.9791102580799],
                                          [0.0, -2.05641429894007E-04, -7.05221578640714E-02, -0.181787024025774,
                                           -0.398417417829113, -0.585808170819483, -0.773224628988589,
                                           -0.98412276793365, -1.14825033416732, -1.33588528635569, -1.46495098879254,
                                           -1.59408095417623, -1.72916166843747, -1.8878268841896, -1.95843901017925,
                                           -2.04081125544093, -2.12322205847071, -2.19387274222847]))
                mult_2 = 10**(np.interp(z_dimless,
                                        [0.0, 0.200003427357164, 0.827179799156869, 1.28264986119203, 1.73823131233505,
                                         2.73549799499605, 3.33410306062994, 3.87584398670185, 4.53170305377523,
                                         4.93103300544949, 5.44464818178702, 6.07232580457209, 6.87137556979812,
                                         7.44213335846728, 8.46964218391198, 9.2117721150221, 9.95395774068615,
                                         10.6104851424066, 11.438496075676, 12.86611457655, 13.6370385920416,
                                         14.2366461596462, 14.9504275628063],
                                        [0.0, -8.99681255790168E-05, -0.146570929156528, -0.322214415464236,
                                         -0.486162045446757, -0.773160366041748, -0.919628474483328, -1.0368312369332,
                                         -1.17162919422833, -1.24198426843061, -1.31239075299037, -1.40624036055797,
                                         -1.50601501182438, -1.57644720156288, -1.68802052986942, -1.76437776330672,
                                         -1.83488706858142, -1.89950988792542, -1.95836189464304, -2.05841930287555,
                                         -2.11139767625184, -2.15260307776673, -2.20555574596429]))
                mult = np.interp(r_dimless,[0.0,0.5],[mult_1,mult_2])
            elif 0.5 < radius/circle_radius <= 1.0:
                mult_1 = 10.0 ** (np.interp(z_dimless,
                                            [0, 0.200003427357164, 0.827179799156869, 1.28264986119203,
                                             1.73823131233505, 2.73549799499605, 3.33410306062994, 3.87584398670185,
                                             4.53170305377523, 4.93103300544949, 5.44464818178702, 6.07232580457209,
                                             6.87137556979812, 7.44213335846728, 8.46964218391198, 9.2117721150221,
                                             9.95395774068615, 10.6104851424066, 11.438496075676, 12.86611457655,
                                             13.6370385920416, 14.2366461596462, 14.9504275628063],
                                            [0, -8.99681255790168E-05, -0.146570929156528, -0.322214415464236,
                                             -0.486162045446757, -0.773160366041748, -0.919628474483328,
                                             -1.0368312369332, -1.17162919422833, -1.24198426843061, -1.31239075299037,
                                             -1.40624036055797, -1.50601501182438, -1.57644720156288, -1.68802052986942,
                                             -1.76437776330672, -1.83488706858142, -1.89950988792542, -1.95836189464304,
                                             -2.05841930287555, -2.11139767625184, -2.15260307776673, -2.20555574596429]
                                            ))
                mult_2 = 10 ** (np.interp(z_dimless,
                                          [0, 0.596270178565308, 1.33773177502827, 1.96496384138191, 2.64911574185145,
                                           3.27645919731295, 3.90385834732837, 4.55988449806354, 5.10190389690509,
                                           5.78672413202179, 6.21473677896973, 7.21356290914076, 8.18398481680776,
                                           9.24017633752613, 10.0679644925797, 10.8673484251293, 12.0379922541728,
                                           13.0373753298831, 13.7797837337628, 14.4936208314768, 14.979054563526],
                                          [-0.298257188881654, -0.392081091270522, -0.538613462658945,
                                           -0.679246495527301, -0.843296946224767, -0.972234122767934,
                                           -1.09532337114851, -1.21257754395586, -1.30054066559276, -1.3944159783391,
                                           -1.45308804880557, -1.57634438084793, -1.68204407581314, -1.78193440038387,
                                           -1.86417811975186, -1.92886520204271, -2.01126315248312, -2.07604020289954,
                                           -2.12315779552387, -2.17026253555883, -2.19972067039106]
                                          ))
                mult = np.interp(r_dimless, [0.5, 1.0], [mult_1, mult_2])
            elif 1.0 < radius / circle_radius <= 1.25:
                mult_1 = 10.0 ** (np.interp(z_dimless,
                                            [0, 0.596270178565308, 1.33773177502827, 1.96496384138191, 2.64911574185145,
                                             3.27645919731295, 3.90385834732837, 4.55988449806354, 5.10190389690509,
                                             5.78672413202179, 6.21473677896973, 7.21356290914076, 8.18398481680776,
                                             9.24017633752613, 10.0679644925797, 10.8673484251293, 12.0379922541728,
                                             13.0373753298831, 13.7797837337628, 14.4936208314768, 14.979054563526],
                                            [-0.298257188881654, -0.392081091270522, -0.538613462658945,
                                             -0.679246495527301, -0.843296946224767, -0.972234122767934,
                                             -1.09532337114851, -1.21257754395586, -1.30054066559276, -1.3944159783391,
                                             -1.45308804880557, -1.57634438084793, -1.68204407581314, -1.78193440038387,
                                             -1.86417811975186, -1.92886520204271, -2.01126315248312, -2.07604020289954,
                                             -2.12315779552387, -2.17026253555883, -2.19972067039106]
                                            ))
                mult_2 = 10 ** (np.interp(z_dimless,
                                          [3.79879699763512E-02, 0.126765088939918, 0.214651095040614,
                                           0.447677108681495, 0.706879562669225, 0.879087123419131, 1.19353857490489,
                                           1.56463138773691, 1.99247695102306, 2.30626006786167, 2.9051436062652,
                                           3.36150478116324, 3.87495287383898, 4.38845666106865, 4.84492922507454,
                                           5.55826507180313, 6.35725914247523, 7.21334013092504, 8.29793587414744,
                                           9.15446241902868, 9.8965923501388, 10.5532311409672, 11.6667880522329,
                                           12.4377120677245, 13.1229778592727, 14.0081870994276, 14.979054563526],
                                          [-2.01171299311101, -1.69011550193646, -1.4620848613634, -0.994353429070844,
                                           -0.778095760359188, -0.696301881619084, -0.678899475614355,
                                           -0.714154128251706, -0.790369983205952, -0.843142715152349,
                                           -0.960371182780961, -1.04244781848716, -1.1303980875347, -1.21250042841965,
                                           -1.28288120780067, -1.38261730129897, -1.48823988072797, -1.5997360934983,
                                           -1.71718305514618, -1.78189584261576, -1.85825307605306, -1.91118003907187,
                                           -1.98770435617096, -2.04068272954725, -2.08777461699284, -2.1408044007266,
                                           -2.19972067039106]
                                          ))
                mult = np.interp(r_dimless, [1.0, 1.25], [mult_1, mult_2])
            elif 1.25 < radius / circle_radius <= 1.5:
                mult_1 = 10.0 ** (np.interp(z_dimless,
                                            [3.79879699763512E-02, 0.126765088939918, 0.214651095040614,
                                             0.447677108681495, 0.706879562669225, 0.879087123419131, 1.19353857490489,
                                             1.56463138773691, 1.99247695102306, 2.30626006786167, 2.9051436062652,
                                             3.36150478116324, 3.87495287383898, 4.38845666106865, 4.84492922507454,
                                             5.55826507180313, 6.35725914247523, 7.21334013092504, 8.29793587414744,
                                             9.15446241902868, 9.8965923501388, 10.5532311409672, 11.6667880522329,
                                             12.4377120677245, 13.1229778592727, 14.0081870994276, 14.979054563526],
                                            [-2.01171299311101, -1.69011550193646, -1.4620848613634, -0.994353429070844,
                                             -0.778095760359188, -0.696301881619084, -0.678899475614355,
                                             -0.714154128251706, -0.790369983205952, -0.843142715152349,
                                             -0.960371182780961, -1.04244781848716, -1.1303980875347, -1.21250042841965,
                                             -1.28288120780067, -1.38261730129897, -1.48823988072797, -1.5997360934983,
                                             -1.71718305514618, -1.78189584261576, -1.85825307605306, -1.91118003907187,
                                             -1.98770435617096, -2.04068272954725, -2.08777461699284, -2.1408044007266,
                                             -2.19972067039106]
                                            ))
                mult_2 = 10 ** (np.interp(z_dimless,
                                          [1.71367858244453E-04, 0.119023545943722, 0.179062275079686,
                                           0.210028447064468, 0.29830431504267, 0.444224046337868, 0.588807108338759,
                                           0.876525173938376, 1.0771369571923, 1.39164410323199, 1.79164238955341,
                                           2.27674195427905, 2.76178582445076, 3.16122716523288, 3.67478664701648,
                                           4.24543304657778, 4.81607944613908, 5.3296946224766, 5.90039671659183,
                                           6.41406758748329, 6.89922284676286, 7.61283716626109, 8.35502279192514,
                                           8.92594766425609, 9.55401514891867, 10.039281797306, 10.5246598348013,
                                           11.3240994619049, 11.8951914178976, 12.4662276793364, 13.5227533673784,
                                           14.293733077424, 14.979054563526],
                                          [-2.98245621551222, -2.502977516537, -2.19891095726086, -1.94746289885869,
                                           -1.67849676114748, -1.35692497515166, -1.17570346505809, -0.965306577098402,
                                           -0.901069335435448, -0.877819001268123, -0.87799893751928,
                                           -0.942544641327074, -1.01293827329746, -1.07159749117455, -1.1478519038969,
                                           -1.22997994996059, -1.31210799602427, -1.38251448058402, -1.45879459848511,
                                           -1.52335315488227, -1.58205093052747, -1.65254738321281, -1.72305668848751,
                                           -1.77594509373822, -1.82885920416767, -1.87586112348768, -1.91116718648251,
                                           -1.97000634061076, -2.00535096137368, -2.04654351029921, -2.11134626589437,
                                           -2.15847671110806, -2.19972067039106]
                                          ))
                mult = np.interp(r_dimless, [1.25, 1.5], [mult_1, mult_2])
            elif 1.5 < radius / circle_radius <= 2.0:
                mult_1 = 10.0 ** (np.interp(z_dimless,
                                            [1.71367858244453E-04, 0.119023545943722, 0.179062275079686,
                                             0.210028447064468, 0.29830431504267, 0.444224046337868, 0.588807108338759,
                                             0.876525173938376, 1.0771369571923, 1.39164410323199, 1.79164238955341,
                                             2.27674195427905, 2.76178582445076, 3.16122716523288, 3.67478664701648,
                                             4.24543304657778, 4.81607944613908, 5.3296946224766, 5.90039671659183,
                                             6.41406758748329, 6.89922284676286, 7.61283716626109, 8.35502279192514,
                                             8.92594766425609, 9.55401514891867, 10.039281797306, 10.5246598348013,
                                             11.3240994619049, 11.8951914178976, 12.4662276793364, 13.5227533673784,
                                             14.293733077424, 14.979054563526],
                                            [-2.98245621551222, -2.502977516537, -2.19891095726086, -1.94746289885869,
                                             -1.67849676114748, -1.35692497515166, -1.17570346505809,
                                             -0.965306577098402, -0.901069335435448, -0.877819001268123,
                                             -0.87799893751928, -0.942544641327074, -1.01293827329746,
                                             -1.07159749117455, -1.1478519038969, -1.22997994996059, -1.31210799602427,
                                             -1.38251448058402, -1.45879459848511, -1.52335315488227, -1.58205093052747,
                                             -1.65254738321281, -1.72305668848751, -1.77594509373822, -1.82885920416767,
                                             -1.87586112348768, -1.91116718648251, -1.97000634061076, -2.00535096137368,
                                             -2.04654351029921, -2.11134626589437, -2.15847671110806, -2.19972067039106]
                                            ))
                mult_2 = 10 ** (np.interp(z_dimless,
                                          [0.171487815745278, 0.17343712513281, 0.232361963190184, 0.349710388319566,
                                           0.437262227096685, 0.524646982212016, 0.611530486341981, 0.755946464681084,
                                           0.928710970970284, 1.18730078486479, 1.64577835281214, 2.18902303184014,
                                           2.8174246838263, 3.33131833293347, 3.95927442848819, 4.58717482948898,
                                           5.10090139493436, 5.72880179593515, 6.24252836138054, 6.87042876238132,
                                           7.41278232854645, 8.0978810364328, 8.69737721492956, 9.38253161736984,
                                           10.7529518113582, 11.6380496624053, 12.6374327381156, 13.3227542242177,
                                           14.1793921582068, 14.9789988689721],
                                          [-2.99422918737362, -2.78955170168283, -2.60244370565857, -2.28085906707338,
                                           -2.08791599547589, -1.91251670836618, -1.78974877471981, -1.62607104911403,
                                           -1.48579788874799, -1.33386742982486, -1.1937227953525, -1.15303149741235,
                                           -1.17085803886623, -1.21202488261302, -1.27663484936765, -1.34709274428488,
                                           -1.40580337251945, -1.47626126743668, -1.53497189567125, -1.60542979058848,
                                           -1.65830534324982, -1.72294101518319, -1.77584227302327, -1.83463001679405,
                                           -1.94050964801042, -2.00523528806937, -2.07001233848579, -2.11125629776879,
                                           -2.16427322891319, -2.20556859855366]
                                          ))
                mult = np.interp(r_dimless, [1.5, 2.0], [mult_1, mult_2])
            elif 2.0 < radius / circle_radius <= 2.5:
                mult_1 = 10.0 ** (np.interp(z_dimless,
                                            [0.171487815745278, 0.17343712513281, 0.232361963190184, 0.349710388319566,
                                             0.437262227096685, 0.524646982212016, 0.611530486341981, 0.755946464681084,
                                             0.928710970970284, 1.18730078486479, 1.64577835281214, 2.18902303184014,
                                             2.8174246838263, 3.33131833293347, 3.95927442848819, 4.58717482948898,
                                             5.10090139493436, 5.72880179593515, 6.24252836138054, 6.87042876238132,
                                             7.41278232854645, 8.0978810364328, 8.69737721492956, 9.38253161736984,
                                             10.7529518113582, 11.6380496624053, 12.6374327381156, 13.3227542242177,
                                             14.1793921582068, 14.9789988689721],
                                            [-2.99422918737362, -2.78955170168283, -2.60244370565857, -2.28085906707338,
                                             -2.08791599547589, -1.91251670836618, -1.78974877471981, -1.62607104911403,
                                             -1.48579788874799, -1.33386742982486, -1.1937227953525, -1.15303149741235,
                                             -1.17085803886623, -1.21202488261302, -1.27663484936765, -1.34709274428488,
                                             -1.40580337251945, -1.47626126743668, -1.53497189567125, -1.60542979058848,
                                             -1.65830534324982, -1.72294101518319, -1.77584227302327, -1.83463001679405,
                                             -1.94050964801042, -2.00523528806937, -2.07001233848579, -2.11125629776879,
                                             -2.16427322891319, -2.20556859855366]
                                            ))
                mult_2 = 10 ** (np.interp(z_dimless,
                                          [0.314288652020427, 0.343918154710902, 0.402731603660417, 0.461433663502073,
                                           0.519912945128011, 0.57833653220002, 0.751992151352092, 0.867502656201802,
                                           1.15488655447784, 1.44221475819995, 1.814867018542, 2.41553278267128,
                                           3.04421290742708, 3.84387531274634, 4.64331493984988, 5.44264317784556,
                                           6.09928196867395, 6.72723806422867, 7.32678993727936, 8.38309284710559,
                                           9.43945145148575, 10.2388353840353, 10.8384429516399, 11.4665661308564,
                                           12.4945205127326, 13.3512141412756, 14.3505972169859, 14.9788874798642],
                                          [-3.00014137848305, -2.88904359598314, -2.71363145628406, -2.54991517291017,
                                           -2.40959060218665, -2.27511395962573, -2.04127394865819, -1.9126709394386,
                                           -1.73736162045447, -1.56790022963293, -1.43941289371765, -1.36950766014326,
                                           -1.35809456078418, -1.39354200226206, -1.45238115639031, -1.52291616684375,
                                           -1.57584312986256, -1.6404530966172, -1.68750642629468, -1.77570089454022,
                                           -1.85804743462316, -1.92273451691401, -1.9639399184289, -2.01100610069575,
                                           -2.07579600370155, -2.12296500668335, -2.18774205709977, -2.21726445487884]))
                mult = np.interp(r_dimless, [2.0, 2.5], [mult_1, mult_2])
            elif 2.5 < radius / circle_radius <= 3.0:
                mult_1 = 10.0 ** (np.interp(z_dimless,
                                            [0.314288652020427, 0.343918154710902, 0.402731603660417, 0.461433663502073,
                                             0.519912945128011, 0.57833653220002, 0.751992151352092, 0.867502656201802,
                                             1.15488655447784, 1.44221475819995, 1.814867018542, 2.41553278267128,
                                             3.04421290742708, 3.84387531274634, 4.64331493984988, 5.44264317784556,
                                             6.09928196867395, 6.72723806422867, 7.32678993727936, 8.38309284710559,
                                             9.43945145148575, 10.2388353840353, 10.8384429516399, 11.4665661308564,
                                             12.4945205127326, 13.3512141412756, 14.3505972169859, 14.9788874798642],
                                            [-3.00014137848305, -2.88904359598314, -2.71363145628406, -2.54991517291017,
                                             -2.40959060218665, -2.27511395962573, -2.04127394865819, -1.9126709394386,
                                             -1.73736162045447, -1.56790022963293, -1.43941289371765, -1.36950766014326,
                                             -1.35809456078418, -1.39354200226206, -1.45238115639031, -1.52291616684375,
                                             -1.57584312986256, -1.6404530966172, -1.68750642629468, -1.77570089454022,
                                             -1.85804743462316, -1.92273451691401, -1.9639399184289, -2.01100610069575,
                                             -2.07579600370155, -2.12296500668335, -2.18774205709977, -2.21726445487884]
                                            ))
                mult_2 = 10 ** (np.interp(z_dimless,
                                          [0.457145182849504, 0.602897830482914, 0.71890958631799, 0.863325564657092,
                                           1.03653562737772, 1.23803852349453, 1.46794564211536, 1.72614559413236,
                                           1.98412276793364, 2.384956472564, 2.95688384686568, 3.67133358467285,
                                           4.24270401343524, 5.21357147753367, 5.75603643280666, 6.38415961202316,
                                           7.55474774651266, 8.4112742913939, 9.21071391849744, 9.78169448538232,
                                           10.5811898070397, 11.1808530691983, 12.2088074510744, 13.0655010796175,
                                           14.4075727456558, 14.9786647016485],
                                          [-3.00020564142989, -2.69617763992186, -2.51494327723892, -2.35126555163314,
                                           -2.16420896596634, -2.00640487370189, -1.86615741851458, -1.75516245672962,
                                           -1.66755920759503, -1.58002022140727, -1.5276459197313, -1.51042344997772,
                                           -1.51652842992768, -1.57544469959214, -1.6166243959283, -1.66369057819515,
                                           -1.75193645679816, -1.81664924426775, -1.875488398396, -1.92252887548412,
                                           -1.97552010144977, -2.01087757480207, -2.07566747780786, -2.12283648078966,
                                           -2.20531154676629, -2.24065616752922]
                                          ))
                mult = np.interp(r_dimless, [2.5, 3.0], [mult_1, mult_2])
            elif 3.0 < radius / circle_radius <= 4.0:
                mult_1 = 10.0 ** (np.interp(z_dimless,
                                            [0.457145182849504, 0.602897830482914, 0.71890958631799, 0.863325564657092,
                                             1.03653562737772, 1.23803852349453, 1.46794564211536, 1.72614559413236,
                                             1.98412276793364, 2.384956472564, 2.95688384686568, 3.67133358467285,
                                             4.24270401343524, 5.21357147753367, 5.75603643280666, 6.38415961202316,
                                             7.55474774651266, 8.4112742913939, 9.21071391849744, 9.78169448538232,
                                             10.5811898070397, 11.1808530691983, 12.2088074510744, 13.0655010796175,
                                             14.4075727456558, 14.9786647016485],
                                            [-3.00020564142989, -2.69617763992186, -2.51494327723892, -2.35126555163314,
                                             -2.16420896596634, -2.00640487370189, -1.86615741851458, -1.75516245672962,
                                             -1.66755920759503, -1.58002022140727, -1.5276459197313, -1.51042344997772,
                                             -1.51652842992768, -1.57544469959214, -1.6166243959283, -1.66369057819515,
                                             -1.75193645679816, -1.81664924426775, -1.875488398396, -1.92252887548412,
                                             -1.97552010144977, -2.01087757480207, -2.07566747780786, -2.12283648078966,
                                             -2.20531154676629, -2.24065616752922]
                                            ))
                mult_2 = 10 ** (np.interp(z_dimless,
                                          [0.80000085683929, 0.886940055523186, 1.0886657298557, 1.26154162525276,
                                           1.52040991191692, 1.75020564142989, 2.03703259416663, 2.55276416355348,
                                           3.03936748123521, 3.69723155225006, 4.44030829077698, 5.12601963875655,
                                           5.69739006751893, 6.52567947355794, 7.32534187887719, 8.18214689652808,
                                           9.1815299722384, 10.1523417417829, 11.8371576927031, 12.5509947904171,
                                           13.5504892552352, 14.4071828837783, 15.0069018404907],
                                          [-3.00035987250231, -2.87174401069336, -2.69054820577852, -2.5385791890873,
                                           -2.3574090893512, -2.22885749048908, -2.11202745313089, -1.96021266751208,
                                           -1.86686431092984, -1.79113685437159, -1.7680793090448, -1.76838777118964,
                                           -1.7744927511396, -1.80410511704425, -1.83955255852212, -1.87502570517874,
                                           -1.93980275559516, -2.00456695342222, -2.09889210679645, -2.14599684683141,
                                           -2.19907804092264, -2.24624704390445, -2.27575658909415]
                                          ))
                mult = np.interp(r_dimless, [3.0, 4.0], [mult_1, mult_2])
            elif 4.0 < radius / circle_radius <= 5.0:
                mult_1 = 10.0 ** (np.interp(z_dimless,
                                            [0.80000085683929, 0.886940055523186, 1.0886657298557, 1.26154162525276,
                                             1.52040991191692, 1.75020564142989, 2.03703259416663, 2.55276416355348,
                                             3.03936748123521, 3.69723155225006, 4.44030829077698, 5.12601963875655,
                                             5.69739006751893, 6.52567947355794, 7.32534187887719, 8.18214689652808,
                                             9.1815299722384, 10.1523417417829, 11.8371576927031, 12.5509947904171,
                                             13.5504892552352, 14.4071828837783, 15.0069018404907],
                                            [-3.00035987250231, -2.87174401069336, -2.69054820577852, -2.5385791890873,
                                             -2.3574090893512, -2.22885749048908, -2.11202745313089, -1.96021266751208,
                                             -1.86686431092984, -1.79113685437159, -1.7680793090448, -1.76838777118964,
                                             -1.7744927511396, -1.80410511704425, -1.83955255852212, -1.87502570517874,
                                             -1.93980275559516, -2.00456695342222, -2.09889210679645, -2.14599684683141,
                                             -2.19907804092264, -2.24624704390445, -2.27575658909415]
                                            ))
                mult_2 = 10 ** (np.interp(z_dimless,
                                          [1.22857044932652, 1.43012903999725, 1.66009185317201, 1.97582427939815,
                                           2.29144531651643, 2.57821657469924, 3.03641566987695, 3.58010590533639,
                                           4.29511258868286, 5.0096737155979, 5.66698084107344, 6.38126349521883,
                                           7.00977653631284, 7.83812163690578, 8.92355279843712, 9.72315950920245,
                                           10.4943063029098, 11.4367695445042, 12.4363197038763, 13.4644968639681,
                                           14.3498174932309, 14.9780520615553],
                                          [-3.00055266134284, -2.83690064091579, -2.69080525756589, -2.5389005038215,
                                           -2.3986916064023, -2.2877094972067, -2.17680450354731, -2.08932978030641,
                                           -2.01362802892689, -1.98470970284813, -1.96746152791582, -1.96778284265003,
                                           -1.97391352777873, -1.99767796552079, -2.02740600472975, -2.06870137437022,
                                           -2.09828803509614, -2.13964766768345, -2.18688093361209, -2.22827912396751,
                                           -2.26961305137608, -2.30498337731775]
                                          ))
                mult = np.interp(r_dimless, [4.0, 5.0], [mult_1, mult_2])
            elif 5.0 < radius / circle_radius <= 6.0:
                mult_1 = 10.0 ** (np.interp(z_dimless,
                                            [1.22857044932652, 1.43012903999725, 1.66009185317201, 1.97582427939815,
                                             2.29144531651643, 2.57821657469924, 3.03641566987695, 3.58010590533639,
                                             4.29511258868286, 5.0096737155979, 5.66698084107344, 6.38126349521883,
                                             7.00977653631284, 7.83812163690578, 8.92355279843712, 9.72315950920245,
                                             10.4943063029098, 11.4367695445042, 12.4363197038763, 13.4644968639681,
                                             14.3498174932309, 14.9780520615553],
                                            [-3.00055266134284, -2.83690064091579, -2.69080525756589, -2.5389005038215,
                                             -2.3986916064023, -2.2877094972067, -2.17680450354731, -2.08932978030641,
                                             -2.01362802892689, -1.98470970284813, -1.96746152791582, -1.96778284265003,
                                             -1.97391352777873, -1.99767796552079, -2.02740600472975, -2.06870137437022,
                                             -2.09828803509614, -2.13964766768345, -2.18688093361209, -2.22827912396751,
                                             -2.26961305137608, -2.30498337731775]
                                            ))
                mult_2 = 10 ** (np.interp(z_dimless,
                                          [1.79999657264283, 2.03007077492545, 2.28838211605031, 2.68982846077389,
                                           3.20539294649895, 3.77787726633992, 4.40728142029681, 5.20789063303286,
                                           5.86530914761627, 6.63701288686294, 7.35129554100832, 8.06552250059978,
                                           8.86546337868869, 9.97941015183192, 10.8077552524248, 11.8931307194022,
                                           12.8356496555506, 14.0637145696953, 15.0061221167357],
                                          [-3.0008097131302, -2.84301847345512, -2.72032765534496, -2.56846145936868,
                                           -2.43419045823765, -2.32333687493574, -2.23590070946293, -2.17193337217671,
                                           -2.14298934091922, -2.11409672001919, -2.1144180347534, -2.1205872776502,
                                           -2.12679507831511, -2.16238389827604, -2.1861483360181, -2.22172430338966,
                                           -2.25723600781437, -2.31042002262056, -2.35762758337046]
                                          ))
                mult = np.interp(r_dimless, [5.0, 6.0], [mult_1, mult_2])
            elif 6.0 < radius / circle_radius <= 7.0:
                mult_1 = 10.0 ** (np.interp(z_dimless,
                                            [1.79999657264283, 2.03007077492545, 2.28838211605031, 2.68982846077389,
                                             3.20539294649895, 3.77787726633992, 4.40728142029681, 5.20789063303286,
                                             5.86530914761627, 6.63701288686294, 7.35129554100832, 8.06552250059978,
                                             8.86546337868869, 9.97941015183192, 10.8077552524248, 11.8931307194022,
                                             12.8356496555506, 14.0637145696953, 15.0061221167357],
                                            [-3.0008097131302, -2.84301847345512, -2.72032765534496, -2.56846145936868,
                                             -2.43419045823765, -2.32333687493574, -2.23590070946293, -2.17193337217671,
                                             -2.14298934091922, -2.11409672001919, -2.1144180347534, -2.1205872776502,
                                             -2.12679507831511, -2.16238389827604, -2.1861483360181, -2.22172430338966,
                                             -2.25723600781437, -2.31042002262056, -2.35762758337046]
                                            ))
                mult_2 = 10 ** (np.interp(z_dimless,
                                          [2.37142269595914, 2.62984542619186, 2.85925129382732, 3.28887908283922,
                                           3.77553809507488, 4.34785533125407, 4.92000548377146, 5.52061555334681,
                                           6.37814460019878, 7.14984833944545, 7.95001199575007, 8.63572334372965,
                                           9.40709291565274, 11.4065830962744, 12.4634986461939, 13.7202462556122,
                                           14.9769938650306],
                                          [-3.00106676491757, -2.86668009048223, -2.77906398875827, -2.66814614250951,
                                           -2.56894985776468, -2.47564005895054, -2.39987404462419, -2.33581673921239,
                                           -2.29526681975529, -2.26637419885526, -2.24919028686979, -2.24949874901463,
                                           -2.25569369709017, -2.3092247318093, -2.33309199026631, -2.37459300133667,
                                           -2.41609401240703]
                                          ))
                mult = np.interp(r_dimless, [6.0, 7.0], [mult_1, mult_2])
            elif 7.0 < radius / circle_radius <= 8.0:
                mult_1 = 10.0 ** (np.interp(z_dimless,
                                            [2.37142269595914, 2.62984542619186, 2.85925129382732, 3.28887908283922,
                                             3.77553809507488, 4.34785533125407, 4.92000548377146, 5.52061555334681,
                                             6.37814460019878, 7.14984833944545, 7.95001199575007, 8.63572334372965,
                                             9.40709291565274, 11.4065830962744, 12.4634986461939, 13.7202462556122,
                                             14.9769938650306],
                                            [-3.00106676491757, -2.86668009048223, -2.77906398875827, -2.66814614250951,
                                             -2.56894985776468, -2.47564005895054, -2.39987404462419, -2.33581673921239,
                                             -2.29526681975529, -2.26637419885526, -2.24919028686979, -2.24949874901463,
                                             -2.25569369709017, -2.3092247318093, -2.33309199026631, -2.37459300133667,
                                             -2.41609401240703]
                                            ))
                mult_2 = 10 ** (np.interp(z_dimless,
                                          [3.25713318709942, 3.54412722349796, 4.00243770778352, 4.71800133666929,
                                           5.26146879391301, 5.97641978270555, 6.63394968639682, 7.23428128320252,
                                           7.86296140795832, 8.69169637042876, 9.52037563834527, 10.2918009048222,
                                           11.0917417829111, 11.8630556602803, 13.0057408232511, 13.7484276999006,
                                           14.4054006580525, 14.9765483085992],
                                          [-3.00146519518799, -2.86709137334202, -2.74449052335744, -2.61030949035199,
                                           -2.54622647976146, -2.47637265654454, -2.43573276896185, -2.40091510436303,
                                           -2.38950200500394, -2.37233094560784, -2.36100781437434, -2.36135483428728,
                                           -2.36756263495219, -2.37960551119032, -2.39766339925284, -2.41554135106419,
                                           -2.43338074510745, -2.46287743770778]
                                          ))
                mult = np.interp(r_dimless, [7.0, 8.0], [mult_1, mult_2])
            elif 8.0 < radius / circle_radius <= 9.0:
                mult_1 = 10.0 ** (np.interp(z_dimless,
                                            [3.25713318709942, 3.54412722349796, 4.00243770778352, 4.71800133666929,
                                             5.26146879391301, 5.97641978270555, 6.63394968639682, 7.23428128320252,
                                             7.86296140795832, 8.69169637042876, 9.52037563834527, 10.2918009048222,
                                             11.0917417829111, 11.8630556602803, 13.0057408232511, 13.7484276999006,
                                             14.4054006580525, 14.9765483085992],
                                            [-3.00146519518799, -2.86709137334202, -2.74449052335744, -2.61030949035199,
                                             -2.54622647976146, -2.47637265654454, -2.43573276896185, -2.40091510436303,
                                             -2.38950200500394, -2.37233094560784, -2.36100781437434, -2.36135483428728,
                                             -2.36756263495219, -2.37960551119032, -2.39766339925284, -2.41554135106419,
                                             -2.43338074510745, -2.46287743770778]
                                            ))
                mult_2 = 10 ** (np.interp(z_dimless,
                                          [3.82855931041573, 4.31544110086712, 4.85924272543441, 5.43139287795181,
                                           6.0606299482469, 6.74689824176577, 7.46157075778867, 8.26190149775508,
                                           8.86206601089899, 9.66222966720362, 10.4337106282345, 11.433762038592,
                                           12.2337029166809, 13.176444631045, 14.0047897316379, 14.9759913630599],
                                          [-3.00172224697536, -2.87913424958015, -2.77996367001405, -2.7041976556877,
                                           -2.63430527470268, -2.57613445522158, -2.53552027281763, -2.50079257634438,
                                           -2.48351869623333, -2.46633478424787, -2.46083387599822, -2.45543578846352,
                                           -2.46164358912842, -2.47376358090277, -2.49752801864482, -2.52135671933372]

                                          ))
                mult = np.interp(r_dimless, [8.0, 9.0], [mult_1, mult_2])
            elif 9.0 < radius / circle_radius <= 10.0:
                mult_1 = 10.0 ** (np.interp(z_dimless,
                                            [3.82855931041573, 4.31544110086712, 4.85924272543441, 5.43139287795181,
                                             6.0606299482469, 6.74689824176577, 7.46157075778867, 8.26190149775508,
                                             8.86206601089899, 9.66222966720362, 10.4337106282345, 11.433762038592,
                                             12.2337029166809, 13.176444631045, 14.0047897316379, 14.9759913630599],
                                            [-3.00172224697536, -2.87913424958015, -2.77996367001405, -2.7041976556877,
                                             -2.63430527470268, -2.57613445522158, -2.53552027281763, -2.50079257634438,
                                             -2.48351869623333, -2.46633478424787, -2.46083387599822, -2.45543578846352,
                                             -2.46164358912842, -2.47376358090277, -2.49752801864482, -2.52135671933372]
                                            ))
                mult_2 = 10 ** (np.interp(z_dimless,
                                          [4.77141241388765, 5.20081742468382, 5.74445196558933, 6.23072111594749,
                                           7.00281471707166, 7.71748723309456, 8.74661120060321, 9.4325453267985,
                                           10.1184237584398, 11.0328169448538, 11.7185839873873, 12.9186345409055,
                                           13.804177948384, 14.5754918257531, 14.9753787229667],
                                          [-3.00214638242451, -2.91462024882613, -2.83299345374782, -2.77473266614114,
                                           -2.70490454810296, -2.66429036569901, -2.60627377729033, -2.5831905267848,
                                           -2.56595520444186, -2.55467063097645, -2.5491311649587, -2.54382304554958,
                                           -2.56176526030778, -2.57380813654591, -2.58568392912225]
                                          ))
                mult = np.interp(r_dimless, [9.0, 10.0], [mult_1, mult_2])

            sigma_z = mult * circle_stress

        return {
            'sigma_z [kPa]': sigma_z,
            'sigma_r [kPa]': sigma_r,
            'sigma_theta [kPa]': sigma_theta,
        }

    except:
        if fail_silently or fail_silently is None:
            return {
                'sigma_z [kPa]': np.NaN,
                'sigma_r [kPa]': np.NaN,
                'sigma_theta [kPa]': np.NaN,
            }
        else:
            raise

STRESSES_RECTANGLE_BOUSSINESQ = {
    'rectangle_stress': {'type': 'float', 'min_value': None, 'max_value': None},
    'rectangle_length': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'rectangle_width': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'z': {'type': 'float', 'min_value': 0.0, 'max_value': None},
}

@ValidationDecorator(STRESSES_RECTANGLE_BOUSSINESQ)
def stresses_rectangle_boussinesq(rectangle_stress, rectangle_length, rectangle_width, z, fail_silently=True, **kwargs):
    """
    Calculates the increase in stress below the corner of a uniformly loaded rectangular area.

    :param rectangle_stress: Stress acting on the uniformly loaded rectangle (:math:`q`) [:math:`kPa`]
    :param rectangle_length: Length of the longest side of the rectangle (:math:`L`) [:math:`m`]  - Suggested range: 0.0<=rectangle_length
    :param rectangle_width: Width of the rectangle (:math:`B`) [:math:`m`]  - Suggested range: 0.0<=rectangle_width
    :param z: z-coordinate of the point where stresses are calculated (:math:`z`) [:math:`m`]  - Suggested range: 0.0<=z

    .. math::
        \\sigma_z = \\frac{q}{2 \\pi} \\left[ \\tan^{-1} \\frac{L B}{z R_3} + \\frac{L B z}{R_3} \\left( \\frac{1}{R_1^2} + \\frac{1}{R_2^2} \\right) \\right]

        \\sigma_x = \\frac{q}{2 \\pi} \\left[ \\tan^{-1} \\frac{L B}{z R_3} - \\frac{L B z}{R_1^2 R_3} \\right]

        \\sigma_y = \\frac{q}{2 \\pi} \\left[ \\tan^{-1} \\frac{L B}{z R_3} - \\frac{L B z}{R_2^2 R_3} \\right]

        \\tau_{zx} = \\frac{q}{2 \\pi} \\left[\\frac{B}{R_2} - \\frac{z^2 B}{R_1^2 R_3} \\right]

        R_1 = (L^2 + z^2)^{1/2}

        R_2 = (B^2 + z^2)^{1/2}

        R_3 = (L^2 + B^2 +z^2)^{1/2}

    :returns:   Vertical normal stress (:math:`\\sigma_z`) [:math:`kPa`], Normal stress in the horizontal x-direction (:math:`\\sigma_x`) [:math:`kPa`], Normal stress in the horizontal y-direction (:math:`\\sigma_y`) [:math:`kPa`], Shear stress in the xy-plane (:math:`\\tau_{zx}`) [:math:`kPa`]

    :rtype: Python dictionary with keys ['sigma_z [kPa]','sigma_x [kPa]','sigma_y [kPa]','tau_zx [kPa]']

    .. figure:: images/stresses_rectangle_boussinesq.PNG
        :figwidth: 500
        :width: 400
        :align: center

        Stresses below the corner of a uniformly loaded rectangle, nomenclature and sign convention

    Reference - Boussinesq J. (1885). Application des potentiels a l'etude de l'equilibre et du mouvement des solides elastiques. Gauthier-Villar. Paris




    """

    try:

        if not kwargs['validated']:
            raise ValueError("Error during function validation, %s" % kwargs['errorstring'])

        if rectangle_width > rectangle_length:
            raise ValueError("Rectangle length must be greater than rectangle width")

        r1 = np.sqrt(rectangle_length**2.0 + z**2.0)
        r2 = np.sqrt(rectangle_width**2.0 + z**2.0)
        r3 = np.sqrt(rectangle_length**2.0 + rectangle_width**2.0 + z**2.0)

        sigma_z = (rectangle_stress/(2.0*np.pi))*(np.arctan((rectangle_length*rectangle_width)/(z*r3)) +
                                                  ((rectangle_length*rectangle_width*z)/r3) *
                                                  ((1.0/(r1**2.0))+(1.0/(r2**2.0))))
        sigma_x = (rectangle_stress/(2.0*np.pi))*(np.arctan((rectangle_length*rectangle_width)/(z*r3)) -
                                                  ((rectangle_length*rectangle_width*z)/((r1**2.0) * r3)))
        sigma_y = (rectangle_stress / (2.0 * np.pi)) * (np.arctan((rectangle_length * rectangle_width) / (z * r3)) -
                                                        ((rectangle_length * rectangle_width * z) / ((r2 ** 2.0) * r3)))
        tau_zx = (rectangle_stress / (2.0 * np.pi)) * ((rectangle_width/r2) -
                                                       (((z**2.0 * rectangle_width))/((r1**2.0) * r3)))

        return {
            'sigma_z [kPa]': sigma_z,
            'sigma_x [kPa]': sigma_x,
            'sigma_y [kPa]': sigma_y,
            'tau_zx [kPa]': tau_zx,
        }

    except:
        if fail_silently or fail_silently is None:
            return {
                'sigma_z [kPa]': np.NaN,
                'sigma_x [kPa]': np.NaN,
                'sigma_y [kPa]': np.NaN,
                'tau_zx [kPa]': np.NaN,
            }
        else:
            raise



