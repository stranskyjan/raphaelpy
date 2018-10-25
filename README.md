# [RaphaëlPy](https://github.com/stranskyjan/raphaelpy)
A library for creating SVG drawings using Python.

## Overview
It's usage and most of the public API (and obviously it's name, too) is strongly inspired by [Raphaël JavaScript Library](http://dmitrybaranovskiy.github.io/raphael/).
Some examples and some of the implementation details are borrowed from the original project, too.

See [examples](examples) to examine how to it works and how to use it.

##### Compatibility
The package works with both Python 2 and 3 (tested on [Ubuntu 18.04 LTS](https://www.ubuntu.com/) and Python 2.7.15 and Python 3.6.6).

## Usage
as simple as:
```python
from raphaelpy import Raphael

# Creates canvas 320 x 200 at 10, 50
paper = Raphael("drawing.svg", 320, 200)

# Creates circle at x = 50, y = 40, with radius 10
circle = paper.circle(50, 40, 10)
# Sets the fill attribute of the circle to red (#f00)
circle.attr("fill", "#f00")

# Sets the stroke attribute of the circle to blue
circle.attr("stroke", "#00f")

# Saves the resulting drawing to the file
paper.save()
```

See [examples](examples) directory for more examples.

## Installation
1. Using `setup.py` file:

	`python setup.py install [options]`, e.g. `python setup.py --user`

2. Using `make` (calls `setup.py` internally):

	`make install [options]`, e.g. `make install USER=TRUE PYTHON=python3`

3. Using [`pip`](https://pypi.org/project/pip/)

	`[sudo] pip install [options] raphaelpy`, e.g. `pip install --user raphaelpy`

## What is here

| directory | content |
| --- | --- |
| [raphaelpy](raphaelpy) | source code |
| [examples](examples) | examples how RaphaëlPy works and how to use it |
| [Makefile](Makefile) | makefile for the project (with targets `help`, `install`, `doc`, `test`, `clean`, `dist`) |
| [docs](docs) | source codes to build HTML documentation |
| [tests](tests) | a few unit tests |
| [setup.py](setup.py) | python setup file for installation |

## Contribution
#### Pull Requests
Are welcome.

#### Bug reporting
In case of any question or problem, please leave an issue at the [githup page of the project](https://github.com/stranskyjan/raphaelpy).

#### Contributors
- [Jan Stránský](https://github.com/stranskyjan)


## License
This project is licensed under the LGPL License - see the [license file](LICENSE) for details.

## Acknowledgements
- to [Raphaël JavaScript Library](http://dmitrybaranovskiy.github.io/raphael/) for great job and inspiration.
