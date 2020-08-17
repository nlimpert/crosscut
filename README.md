# CROSSCUT

This repository supports the paper "Compiling ROS Schooling Curricula via
Contentual Taxonomies" by providing an exemplary set of training material on ROS
Basics. All of this material is written in the well readable reStructuredText
format. In addition, extensions for the Sphinx documentation generator
(https://www.sphinx-doc.org), which is used to build the output, are developed
directly in this repository.

## Getting Started

The following sections describe how to use the contents of this repository by
listing and explaining essential commands.

### Install Sphinx

First of all, Python, Sphinx, and the ReadTheDocs theme need to be installed to
generate various "renderable" formats out of reStructuredText which are easily
readable for non-technically experienced people and suitable for distribution.
Below, the necessary commands are listed to perform the installation on several
operating systems. If the target system is not listed, a recent version of
Python3 and the Sphinx version based on it have to be installed.

#### Debian and Ubuntu

```shell script
apt update && \
apt install python3-sphinx python3-sphinx-rtd-theme \
    python3-sphinxcontrib.svg2pdfconverter librsvg2-bin
```

(Debian 11 "Bullseye" or newer, Ubuntu 19.10 "Eoan Ermine" or newer with
universe repository enabled)

#### Fedora

```shell script
dnf install python3-sphinx python3-sphinx_rtd_theme \
    python3-sphinxcontrib-rsvgconverter librsvg2-tools
```

(Fedora 31 or newer)

#### Arch

```shell script
pacman -Sy python-sphinx python-sphinx_rtd_theme librsvg
pikaur -S python-sphinxcontrib-svg2pdfconverter
```

#### Using PIP

```shell script
pip3 install --user sphinx sphinx-rtd-theme sphinxcontrib-svg2pdfconverter
```

Make sure to add paths to locally installed Python packages and executables in
the user environment. In order to persist this, put the following commands in
designated files like `~/.profile` (sh, bash, ...) or `~/.zshenv` (zsh).

```shell script
export PATH=/home/<user>/.local/bin:$PATH
export PYTHONPATH=/home/<user>/.local/lib/python<ver>/site_packages:$PYTHONPATH
```

#### Other Systems

Please follow the instructions on the following web pages:

- https://www.python.org/download/releases/3.0/
- http://www.sphinx-doc.org/en/master/usage/installation.html
- https://sphinx-rtd-theme.readthedocs.io/en/stable/installing.html
- https://github.com/missinglinkelectronics/sphinxcontrib-svg2pdfconverter
- https://wiki.gnome.org/Projects/LibRsvg

### Get the Code

After the dependencies are successfully installed, this repository needs to be
cloned -- unless this has already been done. First change to the directory where
the repository should be located.

```shell script
cd ~/<path to your repos>
```

Then clone the repository, either via HTTPS:

```shell script
git clone https://github.com/nlimpert/crosscut.git
```

Finally change to the freshly downloaded directory.

```shell script
cd crosscut
```

### Generate Output

Usually a "renderable" format can be created using `make`. For example, this
could be an HTML web page...

```shell script
$ make html
```
... or a PDF.

```shell script
$ make latexpdf
```

Just type `make` or `make help` to get a list of available build targets. For
more advanced build configurations use the Python script `course_generator.py`
in the root directory. Pass `-h` to the script to get a brief overview of the
available options. For further details, please read the guidelines (see also
[Contributing](#contributing)) on how to generate entire courses with this
script.

An example is to generate the current set of the course `ros_basics` by issuing
the following command:

```shell script
_script/course_generator.py -e 'author' -s course/ros_basics.yaml --generate
```

### Spawn a Local Web Server

To make the generated web page available in a local network a simple web server
can be spawned on any computer. Please note that this does not imply any builds,
so `make html` has to be executed before.

```shell script
make html
make server
```

## Contributing

Before attempting to contribute to this project, please read the guidelines in
the author's edition first. It describes the workflow, the coding standards, and
the use of stylistic and didactic methods. Additionally, the linter script
`lint.py` helps to meet our standards.

```shell script
make html SPHINXOPTS='-t author'
xdg-open build/html/guideline.html
```

Just read it carefully...

## Links

- [Acknowledgments](ACKNOWLEDGEMENTS.md)
- [Changelog](CHANGELOG.md)
- [Contributors](CONTRIBUTORS.md)
- [License](LICENSE.md)
