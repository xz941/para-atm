Command line interface
======================

para-atm includes a command-line utility that can be used to quickly perform certain tasks.  Currently, the command-line program has functions for plotting trajectory data and executing NATS simulation files, but it is expected that new capabilities will be added in the future.

The command-line program is accessed by running :code:`para-atm` on the command-line.  To show information about the available commands, run:

.. code:: shell

   para-atm -h

Help information specific to individual sub-commands can be obtained using:

.. code:: shell

   para-atm <sub-command> -h

where :code:`<sub-command>` is a sub-command, such as :code:`plot`.

Plotting
--------

The :code:`plot` sub-command is used to create a trajectory plot from an existing data file, which may be an IFF file, a GNATS output file, or a CSV file created by para-atm:

.. code:: shell

   para-atm plot <data_file>

Try testing :code:`para-atm plot` on the sample data files in the `sample_data` directory.

GNATS simulation
----------------

The :code:`gnats` and :code:`nats` sub-commands are used to run a GNATS or NATS simulation that has been specified in a Python module using the para-atm interface.  Refer to :ref:`gnats` and :ref:`nats` for the details on specifying a GNATS or NATS simulation in para-atm.  The user-defined simulation can then be executed using:

.. code:: shell

   para-atm gnats <simulation_file> --output <output_file>

where :code:`<simulation_file>` names the Python file in which the GNATS simulation class is stored, and :code:`<output_file>` specifies the file to store the GNATS results.  In addition, the :code:`--plot` option can also be given, in which case a trajectory plot is created from the simulation results.

Note that the help message for the :code:`gnats` sub-command can be obtained using:

.. code:: shell

   para-atm gnats -h
