Getting started with python-engineering
=================================================

Getting started with python-engineering is not difficult. These basic example will show you how
you can unlock the full potential of the tool.

But first, a few notes on installation

Installation
---------------

python-engineering is written for Python 3.x. Downloading Anaconda3 is recommended for users not familiar with Python development.

With a valid installation of Python 3, you can simply install python-engineering using pip

.. code-block:: bash

    $ pip install python-engineering

You can import python-engineering into any project:

.. code-block:: python

    import pyeng

If you want to run the suite of unit tests for python-engineering, you will need to install the package nose.
With nose installed, simply run the unit tests as follows. Test failures will indicate whether there are still
missing dependencies in your installation. Please check the FAQ for further info or raise an issue via GitHub.

.. code-block:: bash

    $ python manage.py test


Basic function calls with python-engineering
----------------------------------------------

As an example, we will call the function which returns the pressure drop and Darcy
Weissback friction factor for given pipe properties. We can essentially create the Moody diagram
using this function.

We can start by importing the function from its module:

.. code-block:: python

    from pyeng.hydraulics.pipe_flow.pressure_calcs import pressuredrop_relativeroughness_moody

For most functions, python-engineering has a three-level hierarchy. The engineering discipline is the
top level (in this case hydraulics), next you have the function category (pipe_flow) and below that
is the function module (pressure_calcs). This three-tier model allows a fairly detailed classificiation
of engineering functions. Users can find the engineering discipline, function category and function module
by consulting the documentation.


Calling functions
___________________

python-engineering will always return dictionaries to allow returning multiple outputs from a single
function in a structured manner. To return an output value, the dictionary key will need to be specified.
This can either be done in the function call or afterwards as shown below.

.. code-block:: python

    from pyeng.hydraulics.pipe_flow.pressure_calcs import pressuredrop_relativeroughness_moody

    friction_factor = pressuredrop_relativeroughness_moody(1.0e6,
                                                           1.0,
                                                           "Water mains,old",
                                                           10.0,
                                                           5.0,
                                                           1050.0)['friction_factor [-]']

or

.. code-block:: python

    from pyeng.hydraulics.pipe_flow.pressure_calcs import pressuredrop_relativeroughness_moody

    output = pressuredrop_relativeroughness_moody(1.0e6,
                                                  1.0,
                                                  "Water mains,old",
                                                  10.0,
                                                  5.0,
                                                  1050.0)
    friction_factor = output['friction_factor [-]']

It is often more instructive for people reviewing your work to use keyword arguments for all function parameters.

.. code-block:: python

    from pyeng.hydraulics.pipe_flow.pressure_calcs import pressuredrop_relativeroughness_moody

    friction_factor = pressuredrop_relativeroughness_moody(reynolds_number=1.0e6,
                                                           pipe_diameter=1.0,
                                                           pipe_material="Water mains,old",
                                                           pipe_length=10.0,
                                                           average_velocity=5.0,
                                                           fluid_density=1050.0)['friction_factor [-]']

Several python-engineering functions have optional parameters. Defaults will be used when values are not specified.
Users can override the values of the default parameters by specifying them as keyword arguments in the function call.
In the example below we are overriding the value of acceleration of gravity from the default of 9.81,
rounding it to 10.0 m/s2. The function documentation clearly specifies which function arguments are optional together
with their default value.

.. code-block:: python

    from pyeng.hydraulics.pipe_flow.pressure_calcs import pressuredrop_relativeroughness_moody

    friction_factor = pressuredrop_relativeroughness_moody(reynolds_number=1.0e6,
                                                           pipe_diameter=1.0,
                                                           pipe_material="Water mains,old",
                                                           pipe_length=10.0,
                                                           average_velocity=5.0,
                                                           fluid_density=1050.0,
                                                           gravity_coefficient=10.0)['friction_factor [-]']

Function validation
____________________

python-engineering has parameter validation built in to its core. Using numerical parameters outside applicable ranges
or string parameters which are not in a predefined list, is prevented using the built-in validation logic.

If parameters are outside there applicable ranges, the calculation will not go ahead. By default,
python-engineering will fail silently, meaning that in case of a validation error, the code will return
NaN for numerical outputs and None for string outputs. If several function calls are made in a loop,
the function calls for which the validation executes correctly, will still complete as expected. As an example of
this, let's call the function for Reynolds numbers ranging from 1e2 to 1e9. The function below
will return values for all but the first and last Reynolds number, since these two are outside the validation ranges.

.. code-block:: python

    from pyeng.hydraulics.pipe_flow.pressure_calcs import pressuredrop_relativeroughness_moody
    import numpy as np

    reynolds_numbers = np.logspace(2,9,8) # [1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9]
    friction_factors = []

    for re in reynolds_numbers:

        friction_factor = pressuredrop_relativeroughness_moody(reynolds_number=re,
                                                               pipe_diameter=1.0,
                                                               pipe_material="Water mains,old",
                                                               pipe_length=10.0,
                                                               average_velocity=5.0,
                                                               fluid_density=1050.0)['friction_factor [-]']
        friction_factors.append(friction_factor)