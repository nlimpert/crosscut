.. meta::
   :keywords lang=en: Linux navigation
   :description lang=en: This goes into the meta tags of the HTML page.
   :unit-type: tutorial
   :unit-interaction: practice
   :unit-duration: all/20, beginner/30

.. sidebar:: Document Info

   .. sectionauthor::
      :term:`Limpert, Nicolas`;
      :term:`Meeßen, Marcus`;
      :term:`Schiffer, Stefan`

**************************
Navigation in Linux
**************************

Introduction
==============

This tutorial will help you become familiar with the basic Linux
navigation commands needed for the subsequent tutorials.

-  Lines beginning with $ are terminal commands.

   -  To open a new terminal → use the shortcut ``Ctrl + Alt + T``.

   -  To open a new tab inside an existing terminal → use the shortcut
      ``Ctrl + Shift + T``.

   -  To kill a process in a terminal → use the shortcut ``Ctrl + C``.

-  Lines beginning with # indicate the syntax of the commands.

-  Code is separated in boxes.

-  Code is case sensitive.

Filesystem: Organisation and Navigation
==========================================

The files on a Linux system are arranged in a single
hierarchical(tree-like) directory structure, the first directory being
called the root directory. This root directory contains all the other
files and subdirectories.

Print Working Directory
--------------------------

This command returns your current working directory with respect to the
root directory.

.. code-block:: bash

    $ pwd

List directory contents
-------------------------

.. code-block:: bash

    $ ls -l /etc

    # ls <options> <location>

This command allows to print the contents of the directory specified.
The arguments to this command are optional. Hence, adding no arguments
to this command lists the contents of the current directory.

Paths
---------

There are 2 types of paths that can be used to specify a location:
absolute and relative.

Absolute paths specify the location of a file or directory in relation
to the root directory. These begin with a forward slash (/).

Relative paths specify the location of the file or directory in relation
to current location in the system. These do not have a leading slash.

Hence, for example, the absolute path

.. code-block:: bash

    $ ls /home/up/Desktop

would give the same result as the relative path

.. code-block:: bash

    $ ls Desktop

Additionally, the following can be used while typing in the absolute or
relative paths as per the requirement:

-  ~ (tilde): shortcut to denote the path of the home directory.

-  . (dot): a reference to the current directory.

-  \.. (dotdot): a reference to the parent directory relative to current directory.

Change Directory
--------------------

This command is used to navigate in the filesystem:

.. code-block:: bash

    # cd <location>

The <location> is an optional argument that can contain an absolute or
relative path where one wishes to navigate to. Using cd without any
arguments changes the directory directly to the home directory.

Tab completion
--------------------

While typing in a command, pressing the tab key will auto complete the
path as per the currently keyed in value. This is particularly useful to
avoid misspelling and incomplete path entries. However, when multiple
cases match, the field is not completed automatically and instead a
double tab lists all the possibilities.

Create a directory
------------------------

.. code-block:: bash

    $ mkdir test

    # mkdir <option> <directory name>

This creates an empty directory at the current location while the
following creates all required directories and subdirectories.

.. code-block:: bash

    $ mkdir -p test/subdirectory

Create a file
------------------

.. code-block:: bash

    $ touch /home/up/test/subdirectory/examplefile

    # touch <path><filename>

This command creates a new empty file in the specified path. If the file
already exists ``touch`` updates the timestamps of last access and
modification.
