from math import floor
from .paper import Paper
from .element import *
from .set import Set
from .utils import _packageRGB

class _El(object):
	pass

class _Fn(object):
	pass

class _Raphael(object):
	"""Auxiliary class for initialization :class:`Paper` and custom functions and methods defined in :attr:`el <_Raphael.el>` and :attr:`fn <_Raphael.fn>`.
	"""
	def __init__(self):
		self.el = _El()
		"""You can add your own method to elements.
		This is usefull when you want to hack default functionality or want to wrap some common transformation or attributes in one method.
		You should alter the el object before calling Raphael(...), otherwise it will take no effect.
		
		Usage:
		
		.. code-block:: python
		
			Raphael.el.red = lambda this: this.attr(fill="#f00")
			# Raphael.el has to be defined before calling Raphael **(!)**
			paper = Raphael(...)
			# then use it
			paper.circle(100, 100, 20).red()
		"""
		self.fn = _Fn()
		"""You can add your own method to the canvas. For example if you want to draw a pie chart, you can create your own pie chart function and ship it as a Raphael plugin. To do this you need to extend the Raphael.fn object.
		You should alter the el object before calling Raphael(...), otherwise it will take no effect.
		
		Usage:
		
		.. code-block:: python
		
			Raphael.fn.arrow = lambda this, x1, y1, x2, y2, size: this.path(["M",x1,y1,"L",x2,y2]).attr(stroke_width=size,arrow_end="classic")
			# Raphael.fn has to be defined before calling Raphael **(!)**
			paper = Raphael("fn.svg", 640, 480)
			# then use it
			paper.arrow(50, 50, 100, 200, 5).attr(fill="#f00")
		"""
		self._getColorStart = None
	def __call__(self,fileName,*args,**kw):
		"""Initializes :attr:`el <_Raphael.el>` and :attr:`fn <_Raphael.fn>` objects and creates :class:`Paper` instance to draw on.
		
		Parameters might be:
		
		:param str fileName: file name for saving
		:param width: width of the canvas
		:param height: width of the canvas
		:return: new :class:`Paper` instance
		
		.. code-block:: python
		
			paper = Drawing("fname1.svg",640,480)
			paper = Drawing("fname2.svg",640,480,backgroundColor='cyan')
			paper = Drawing("fname3.svg",width=640,height=480)
		
		or
		
		:param str fileName: file name for saving
		:param list|tuple attrs: first 4 elements in the list are equal to [x, y, width, height]. The rest are element descriptions in format {"type": type, <attributes>}
		:return: new :class:`Paper` instance
		
		.. code-block:: python
		
			paper = Drawing("fname4.svg",[0,0,640,480,
				{
					"type": "path",
					"path": "M100,200 l50,100",
					"stroke-width": 5,
					"stroke": "blue",
				},
				{
					"type": "rect",
					"x": 100,
					"y": 300,
					"width": 300,
					"height": 50,
					"fill": "red",
					"stroke": "cyan",
				},
			])
		"""
		for k,v in self.el.__dict__.items():
			setattr(RaphaelElement,k,v)
		for k,v in self.fn.__dict__.items():
			setattr(Paper,k,v)
		return Paper(fileName,*args,**kw)
	@staticmethod
	def rgb(r, g, b):
		r,g,b = [int(v) for v in (r,g,b)]
		return "#" + hex(b | (g << 8) | (r << 16))[2:].rjust(6,"0")
	@staticmethod
	def hsb2rgb(h,s,b,o=1):
		v = b
		if (isinstance(h,dict) and "h" in h and "s" in h and "b" in h):
			v = h.b
			s = h.s
			o = h.o
			h = h.h
		h *= 360
		h = (h % 360) / 60.
		C = v * s
		X = C * (1 - abs(h % 2 - 1))
		R = G = B = v - C
		h = int(h)
		R += [C, X, 0, 0, X, C][h]
		G += [X, C, C, X, 0, 0][h]
		B += [0, 0, X, C, C, X][h]
		return _packageRGB(R, G, B, o)
	def getColor(self, value=None):
		if value is None:
			value = .75
		start = self._getColorStart = self._getColorStart if self._getColorStart else dict(h = 0, s = 1, b = value)
		rgb = _Raphael.hsb2rgb(start["h"], start["s"], start["b"])
		start["h"] += .075
		if (start["h"] > 1):
			start["h"] = 0
			start["s"] -= .2
		if start["s"] <= 0:
			self._getColorStart = dict(h = 0, s = 1, b = start.b)
		return rgb["hex"]

Raphael = _Raphael()
"""
Predefined instance of :class:`_Raphael` class.
:meth:`Calling Raphael(...) <_Raphael.__call__>` creates a :class:`Paper` instance to draw on.

.. code-block:: python

	paper = Raphael("raphael.py",640,480)
	paper.rect(100,100,200,300)
	paper.save()
"""
