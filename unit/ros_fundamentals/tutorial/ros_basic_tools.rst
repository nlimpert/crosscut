.. meta::
   :keywords lang=en: robots, bees, birds
   :description lang=en: This goes into the meta tags of the HTML page.
   :unit-type: tutorial
   :unit-interaction: practice
   :unit-duration: all/20
   :unit-requires: unit/linux/tutorial/linux_navigation

.. sidebar:: Document Info

   .. sectionauthor::
      :term:`Limpert, Nicolas`;
      :term:`Meeßen, Marcus`;
      :term:`Schiffer, Stefan`

****************
ROS: Basic Tools
****************

Introduction
============

During this tutorial, you will get to learn about the basics of the ROS
parameter server. Further more, a brief introduction Transforms (TF) is
given. Finally the most important visualization tool in ROS, *RVIZ*, and
a composition of analyse/introspection/debugging tools called *RQt*, are
introduced

-  Lines beginning with :code:`$` are terminal commands

-  Lines beginning with :code:`#` indicate the syntax of the commands

Terminal Usage
==============

-  opening a new terminal: :kbd:`Ctrl-Alt-t`

-  opening a new tab inside an existing terminal: :kbd:`Ctrl-Shift-t`

-  killing an active process inside a terminal: :kbd:`Ctrl-c`

Parameter Server
================

The parameter server stores and retrieves parameters of ROS nodes at runtime.
It is suitable for static data. The parameter server is accessible via:

-  command line

-  launch file

-  ROS node

Set your :code:`ROS_MASTER_URI` to the IP of the robot. This way, you tell
your system, that the :code:`roscore` is running on a different machine.

.. code-block:: bash

   $ export $ROS_MASTER_URI=http://<ip-of-robot>:11311

.. hint:: This can also be added to :file:`~/.bashrc` for auto-set.

Access via Command Line
-----------------------

List all active parameters within the ROS Parameter Server:

.. code-block:: bash

   $ rosparam list

By executing this command, a list of the current parameters on the
parameter server is displayed. The former part is a namespace and
depends on the name of the running process. Hint: You can change the
default name of a running process using a launch file.

Get the actual value of a specific parameter:

.. code-block:: bash

   # rosparam get <param_name>

Store a value to the ROS Parameter Server:

.. code-block:: bash

   # rosparam set <param_name> <value>

Access via Launch File
----------------------

Parameters can also automatically on startup in combination with launch-files.
We are going to need that later.

:Example:
   .. code-block:: xml

      <launch>
          <node name="node_name" pkg="package_name" type="node" output="screen">
              <param name="parameterA" value="somevalue"/>
              <param name="parameterB" value="anothervalue"/>
          </node>
      </launch>

RViz
====

RViz is a powerful visualization tool, that should already be installed in your
ROS environment. Start RViz by typing:

.. code-block:: bash

   $ rosrun rviz rviz

or just

.. code-block:: bash

   $ rviz

The first thing to do after startup is setting the fixed-frame in the global
options to a frame, that actually exists, otherwise no data can be displayed!

After the fixed frame is correctly set, use the :guilabel:`add` button to
visualize the sensor data of the robot:

-  Grid

-  Transforms

-  Odometry

-  IMU

-  LaserScan

Ask our team to let you drive around with the robot to see how the data changes
in RViz when the robot moves.

RQt
===

RQt is a collection of tools for introspection/debugging/analysing/visualizing
robot data. RQt can be started by typing

.. code-block:: bash

   $ rosrun rqt rqt

or just

.. code-block:: bash

   $ rqt

Since we cannot cover all its functionality, here are two very useful tools
within the suite:

RQt plot
--------

RQt plot allows easy plotting of sensor data for fast analysis, even if there
is no visualization plugin available for RViz.

RQt plot can be started by clicking on :guilabel:`Plugins` :math:`\rightarrow`
:guilabel:`Visualization` :math:`\rightarrow` :guilabel:`Plot` within the RQt
suite or by typing:

.. code-block:: bash

   $ rosrun rqt_plot rqt_plot

or just

.. code-block:: bash

   $ rqt_plot

Use :code:`rostopic list` to identify some sensor data that you would like to
be plotted and then view in in :code:`rqt_plot`!

.. hint:: Some sensor messages consist of several sub-messages, that can be
   accessed by a :code:`/` in rqt_plot.

:Example:
   The topic :code:`/imu/data/` is of type :code:`sensor_msgs/Imu`, which
   consists ob sub-messages and cannot be plotted directly. To access e.g.
   the linear acceleration on the x-axis you have to use
   :code:`/imu/data/linear_acceleration/x` in rqt_plot.

RQt TF tree
-----------

A tool that comes in very handy when trying to figure out what might be wrong
with your transformations is :code:`rqt_tf_tree`. It subscribes to the
:code:`/tf` topic and generates a PDF displaying the currently active TF Tree.
It is also a nice tool to see which node is broadcasting which transform.

RQt TF Tree can be started by clicking on :guilabel:`Plugins`
:math:`\rightarrow` :guilabel:`Visualization` :math:`\rightarrow`
:guilabel:`TF Tree` within the RQt suite or by typing:

.. code-block:: bash

   $ rosrun rqt_tf_tree rqt_tf_tree

or just

.. code-block:: bash

   $ rqt_tf_tree

RQt Graph
---------

A Tool similar to RQt TF Tree, but this one visualizes the nodes that
are currently active and the topics they are using to communicate.

RQt Graph can be started by clicking on :guilabel:`Plugins` :math:`\rightarrow`
:guilabel:`Visualization` :math:`\rightarrow` :guilabel:`Node Graph` within the
RQt suite or by typing:

.. code-block:: bash

   $ rosrun rqt_graph rqt_graph

or just

.. code-block:: bash

   $ rqt_graph
