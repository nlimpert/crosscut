# Academy

The Academy repository contains the training materials used in the ROS-I Academy
(https://ros-i.academy) and the ROS-I School (https://ros-i.school). All of this
material is written in the well readable reStructuredText format. In addition,
extensions for the Sphinx build system (https://www.sphinx-doc.org), which is
used for the output generation, are also developed directly in this repository.

## Getting Started

If you are already excited about how to use the contents of this repository, you
should keep reading. Here are some things you should know before you get
started.

### Install Sphinx

First of all you should install Python, Sphinx, and the ReadTheDocs theme, with
which you can generate other renderable formats out of our reStructuredText
contents, that are more readable for non-technical experienced people and also
suitable for distribution. Below, we have listed the necessary commands to
perform the installation on several operating systems. If your system is not
listed, be sure to use Python3 and the Sphinx version based on that.

#### Debian-based

```shell script
$ apt update && \
  apt install python3-sphinx python3-sphinx-rtd-theme
```

#### RedHat-based

```shell script
$ dnf install python3-sphinx python3-sphinx_rtd_theme
```

#### Arch-based

```shell script
$ pacman -Sy python-sphinx python-sphinx_rtd_theme
```

#### Gentoo-based

```shell script
$ emerge --sync && \
  emerge --ask dev-python/sphinx dev-python/sphinx_rtd_theme
```

#### Other Systems

Please follow the instructions on the following web pages:

- https://www.python.org/download/releases/3.0/
- http://www.sphinx-doc.org/en/master/usage/installation.html
- https://sphinx-rtd-theme.readthedocs.io/en/stable/installing.html

### Get the Code

Now that you have hopefully installed the dependencies successfully, you can
clone our code – if you haven't already done so. First change to the directory
where you want to put our code.

```shell script
$ cd ~/<path to your repos>
```

Then clone the repository, either via SSH…

```shell script
$ git clone git@git.fh-aachen.de:h2020rosin/academy.git
```

… or via HTTPS.

```shell script
$ git clone https://git.fh-aachen.de/h2020rosin/academy.git
```

Finally change to the freshly downloaded directory.

```shell script
$ cd academy
```

### Generate Output

In the simplest case you can generate a renderable format using `make`. For
example you can generate HTML web pages…

```shell script
$ make html
```
… or PDFs.

```shell script
$ make latexpdf
```

Type only `make` or `make help` to get the full list of available build targets.
For more advanced build configurations you might use the Python script
`course_generator.py` in the root directory. Pass `-h` to the script to get a
brief overview of the available options. For further details, please read the
guidelines (see [Contributing](#contributing)) on how to generate entire courses
with this script.

### Spawn a Local Web Server

To make the generated web page available in a local network, you can easily
spawn a web server on you computer. Please note that this does not imply any
builds, so you should make sure that `make html` has been executed before.

```shell script
$ make html
$ make server
```

# Contributing

Before you want to contribute anything to this project, read the guidelines in
the "internal" version first. It describes the work process, coding standards,
and the use of stylistic and didactic methods.

```shell script
$ make html SPHINXOPTS='-t internal'
$ xdg-open build/html/guideline.html
```

Just read carefully…

# Links

- [Acknowledgments](ACKNOWLEDGMENTS.md)
- [Changelog](CHANGELOG.md)
- [Contributors](CONTRIBUTORS.md)
- [License](LICENSE.md)
