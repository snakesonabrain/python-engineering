Getting started with python-engineering
=================================================

Getting started with python-engineering is not difficult. These basic example will show you how
you can unlock the full potential of the tool.

But first, a few notes on installation

Installation
---------------

python-engineering is written for Python 3.x. Downloading Anaconda3 is recommended for users not familiar with Python development.

With a valid installation of Python 3, you can simply install python-engineering using pip.

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

python-engineering functions are called like any other Python function. The documentation provide extensive
guidance on each function argument, the allowed range or options and units.

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
this, let's call the function for Reynolds numbers ranging from 1e2 to 1e9 and plot the results. The function below
will return values for all but the first and last Reynolds number, since these two are outside the validation ranges,
this is clearly observed in the plot. Even though validation errors occur, the plot is still generated without problems
but no values are calculated where the input parameters are out of bounds.

.. code-block:: python

    from pyeng.hydraulics.pipe_flow.pressure_calcs import pressuredrop_relativeroughness_moody
    import numpy as np
    import matplotlib.pyplot as plt

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

    plt.plot(reynolds_numbers, friction_factors)
    plt.xscale('log')
    plt.show()

When numerical results are needed for parameters outside validation ranges, the user has two choices:

    - Switch of validation completely (not recommended)
    - Expand the validation ranges by specifying additional keyword arguments

For the first option, the function call would look like this:

.. code-block:: python

    from pyeng.hydraulics.pipe_flow.pressure_calcs import pressuredrop_relativeroughness_moody

    pressuredrop_relativeroughness_moody(reynolds_number=1e2,
                                         pipe_diameter=1.0,
                                         pipe_material="Water mains,old",
                                         pipe_length=10.0,
                                         average_velocity=5.0,
                                         fluid_density=1050.0,
                                         validate=False)['friction_factor [-]']

In this case, no validation whatsoever is carried out by adding validate as a keyword argument and setting it to ``False``.

For the second (recommended) option, the code from the validation example would need to look as follows:

.. code-block:: python

    from pyeng.hydraulics.pipe_flow.pressure_calcs import pressuredrop_relativeroughness_moody
    import numpy as np
    import matplotlib.pyplot as plt

    reynolds_numbers = np.logspace(2,9,8) # [1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9]
    friction_factors = []

    for re in reynolds_numbers:

        friction_factor = pressuredrop_relativeroughness_moody(reynolds_number=re,
                                                               pipe_diameter=1.0,
                                                               pipe_material="Water mains,old",
                                                               pipe_length=10.0,
                                                               average_velocity=5.0,
                                                               fluid_density=1050.0,
                                                               reynolds_number__min=1e2,
                                                               reynolds_number__max=1e9)['friction_factor [-]']
        friction_factors.append(friction_factor)

    plt.plot(reynolds_numbers, friction_factors)
    plt.xscale('log')
    plt.show()

The code above will generate a plot containing all reynolds numbers, from 1e2 to 1e9. Adding keyword arguments
``__min`` and/or ``__max`` to a function argument overrides the validation ranges. Note that overriding of validation ranges
is only possible for the given function call. Calling the function again without the override would again result in
the default behaviour.

The behaviour of the function in case of overriding of validation ranges depends on how it is coded.
The function above works with interpolation and follows the logic of numpy's interp function.


Error handling
____________________

Since python-engineering fails silently by default, the user might not know what is actualy going wrong when a value
is not returned. After all, not all errors will be validation errors, errors could also be raised during the
execution of the function itself.

If you want to see what is actually going when a value is not returned and get more details on where the error
is happening, you can override the default error handling behaviour. You can do this by specifying ``fail_silently=False``
as an additional keywords argument. This will cause the function to fail with a full traceback of the error.

.. code-block:: python

    from pyeng.hydraulics.pipe_flow.pressure_calcs import pressuredrop_relativeroughness_moody

    pressuredrop_relativeroughness_moody(reynolds_number=1e2,
                                         pipe_diameter=1.0,
                                         pipe_material="Water mains,old",
                                         pipe_length=10.0,
                                         average_velocity=5.0,
                                         fluid_density=1050.0,
                                         fail_silently=False)['friction_factor [-]']

The code above will raise a ValueError indicating the ``reynolds_number=1e2`` is outside allowable bounds. It will also
say what the allowable minimum is. The function documentation will also provide this information for each input
parameter.


python-engineering class methods
---------------------------------

For certain calculations, it is more meaningful to uses classes than functions. Sometimes, calculation entities
need to be persistent throughout the execution of a program. A typical example of this are geometrical shapes.
Geometrical shapes have multiple atributes which need to be calculated such as area, centroid location, ...
Creating the geometric shapes as objects allows the necessary flexibility.

Object creation
________________

When objects are created, the necessary properties need to be specified. As an example, we can create a circle with
a radius of 1m. When the circle object is created, the derived properties such as area will immediately be calculated.
We can go ahead and print the circle area.

.. code-block:: python

    from pyeng.general.geometry.geom_2d import Circle
    my_circle = Circle(radius=1.0)
    print("Circle area = %.2fm2" % my_circle.centroid['area [m2]'])

Modification of object attributes
__________________________________

Now that the object my_circle of the Circle class exists, we can change its attributes. This will trigger recalculation.
If we change the radius of the circle to 2m, we should see the effect on the area.

.. code-block:: python

    from pyeng.general.geometry.geom_2d import Circle
    my_circle = Circle(radius=1.0)
    print("Circle area = %.2fm2" % my_circle.centroid['area [m2]'])
    my_circle.radius = 2.0
    print("Updated circle area = %.2fm2" % my_circle.centroid['area [m2]'])

Validation and error handling
_______________________________

The documentation highlights which validation ranges or options are applicable for class attributes. When values are
outside allowable ranges, the calculation will fail silently, unless ``fail_silently=False`` is specified as an
additional keyword argument. This is illustrated in the example below:

.. code-block:: python

    # Silent failure, returning np.nan
    from pyeng.general.geometry.geom_2d import Circle
    my_circle = Circle(radius=-1.0)
    print("Circle area = %.2fm2" % my_circle.centroid['area [m2]'])

.. code-block:: python

    # Failure with error traceback
    from pyeng.general.geometry.geom_2d import Circle
    my_circle = Circle(radius=-1.0,fail_silently=False)
