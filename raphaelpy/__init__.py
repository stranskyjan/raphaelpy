"""
Raphaelpy is a library for creating SVG drawings using Python.
It's usage and most of the public API (and obviously it's name, too) is strongly inspired by `Raphael JavaScript Library <http://dmitrybaranovskiy.github.io/raphael/>`_.
Some examples and some of the implementation details are borrowed from the original project, too.

See examples to examine how to it works and how to use it.
"""

from .raphael import *
from .raphael import _Raphael # for the documentation purposes

null = "none"
"""for more JavaScript consistency"""

version = "0.1.0"
