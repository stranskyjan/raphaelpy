"""
Raphaelpy is a library for creating SVG drawings using Python.
It's usage and most of the public API (and obviously it's name, too) is strongly inspired by `Raphael JavaScript Library <http://dmitrybaranovskiy.github.io/raphael/>`_.
Some examples and some of the implementation details are borrowed from the original project, too.

See examples to examine how to it works and how to use it.

.. code-block:: python

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
"""
from .raphael import *
from .raphael import _Raphael # for the documentation purposes

null = "none"
"""for more JavaScript consistency"""

version = "0.1.1"
