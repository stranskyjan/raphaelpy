from .utils import SvgElement,_parsePath

class RaphaelElement(SvgElement):
	id = -1
	"""id of the element. Useful for :meth:`Paper.getById` method."""
	prev = None
	"""reference to the previous :class:`element <RaphaelElement>` in the hierarchy"""
	next = None
	"""reference to the next :class:`element <RaphaelElement>` in the hierarchy"""
	paper = None
	"""Internal reference to :class:`Paper` where object drawn."""
	def reset(self):
		self._resetCommon()
		self._resetSpecific()
		self._markerEnd = None
		self._markerStart = None
		self._gradient = None
	def _resetCommon(self):
		self.id = -1
		self.prev = None
		self.next = None
		self.paper = None
	def _resetSpecific(self):
		self.attrs = self._attrs = {
			"stroke": "black",
			"stroke-width": 1,
			"fill": None,
		}
	def clone(self):
		"""Creates clone of a given element.

		:return: clone of itself
		:rtype: RaphaelElement


		.. code-block:: python
			
			c1 = paper.circle(100,100,30).attr(fill="#f00",stroke="#00f",stroke_width=10)
			c2 = c1.clone().attr(cx=300,cy=300)
		"""
		ret = self.__class__()
		ret.attr(self.attr())
		if self.paper:
			self.paper._add(ret)
		return ret
	def getBBox(self):
		"""Not yet implemented ..."""
		raise NotImplementedError
	def hide(self):
		"""Not implemented yet ..."""
		raise NotImplementedError
		return self
	def remove(self):
		"""Removes element from the paper.

		.. code-block:: python

			paper = Raphael("element.remove.1.svg",640,480)
			r1 = paper.rect(100,100,400,300)
			r2 = paper.rect(200,200,100,100)
			paper.save()
			paper.fileName = "element.remove.2.svg"
			r2.remove()
			paper.save()
		"""
		if self.paper:
			self.paper._remove(self)
		self._resetCommon()
	def show(self):
		"""Not implemented yet"""
		raise NotImplementedError
		return self
	def _hasNoPrevNorNext(self):
		return self.next is None and self.prev is None
	def insertAfter(self,elem):
		"""Inserts current object after the given one.

		:param RaphaelElement elem: insert self after given elem
		:return: self

		.. code-block:: python

			e1 = paper.rect(100,100,100,100).attr(fill="red")
			e2 = paper.rect(110,110,100,100).attr(fill="orange")
			e3 = paper.rect(120,120,100,100).attr(fill="yellow")
			e4 = paper.rect(130,130,100,100).attr(fill="green")
			e5 = paper.rect(140,140,100,100).attr(fill="blue")
			e6 = paper.rect(150,150,100,100).attr(fill="blueviolet")
			e2.insertAfter(e4)
		"""
		self.paper._remove(self)
		self.paper._insertAfter(elem,self)
		return self
	def insertBefore(self,elem):
		"""Inserts current object before the given one.

		:param RaphaelElement elem: insert self before given elem
		:return: self

		.. code-block:: python

			e1 = paper.rect(100,100,100,100).attr(fill="red")
			e2 = paper.rect(110,110,100,100).attr(fill="orange")
			e3 = paper.rect(120,120,100,100).attr(fill="yellow")
			e4 = paper.rect(130,130,100,100).attr(fill="green")
			e5 = paper.rect(140,140,100,100).attr(fill="blue")
			e6 = paper.rect(150,150,100,100).attr(fill="blueviolet")
			e2.insertBefore(e4)
		"""
		self.paper._remove(self)
		self.paper._insertBefore(elem,self)
		return self
	def toBack(self):
		"""Moves the element so it is the furthest from the viewer's eyes, behind other elements.

		:return: self

		.. code-block:: python

			e1 = paper.rect(100,100,100,100).attr(fill="red")
			e2 = paper.rect(110,110,100,100).attr(fill="orange")
			e3 = paper.rect(120,120,100,100).attr(fill="yellow")
			e4 = paper.rect(130,130,100,100).attr(fill="green")
			e5 = paper.rect(140,140,100,100).attr(fill="blue")
			e6 = paper.rect(150,150,100,100).attr(fill="blueviolet")
			e2.toBack()
		"""
		self.insertBefore(self.paper.bottom)
		return self
	def toFront(self):
		"""Moves the element so it is the closest to the viewer's eyes, on top of other elements.

		:return: self

		.. code-block:: python

			e1 = paper.rect(100,100,100,100).attr(fill="red")
			e2 = paper.rect(110,110,100,100).attr(fill="orange")
			e3 = paper.rect(120,120,100,100).attr(fill="yellow")
			e4 = paper.rect(130,130,100,100).attr(fill="green")
			e5 = paper.rect(140,140,100,100).attr(fill="blue")
			e6 = paper.rect(150,150,100,100).attr(fill="blueviolet")
			e2.toFront()
		"""
		self.insertAfter(self.paper.top)
		return self
	def translate(self):
		"""Not implemented yet ..."""
		raise NotImplementedError
	def rotate(self):
		"""Not implemented yet ..."""
		raise NotImplementedError
	def scale(self):
		"""Not implemented yet ..."""
		raise NotImplementedError
	def transform(self):
		"""Not implemented yet ..."""
		raise NotImplementedError


class Rect(RaphaelElement):
	def __init__(self,x=0,y=0,width=0,height=0,r=0,id=None):
		RaphaelElement.__init__(self,x=x,y=y,width=width,height=height,rx=r,ry=r,id=id) # TODO r
	def _xmlTag(self):
		return "rect"

class Circle(RaphaelElement):
	def __init__(self,cx=0,cy=0,r=0,id=None):
		RaphaelElement.__init__(self,cx=cx,cy=cy,r=r,id=id)
	def _xmlTag(self):
		return "circle"

class Text(RaphaelElement):
	def __init__(self,x=0,y=0,text=0,id=None):
		RaphaelElement.__init__(self,x=x,y=y,text=text,id=id)
	def _xmlTag(self):
		return "text"
	def _resetSpecific(self):
		self.attrs = self._attrs = {
			"stroke": None,
			"fill": 'black',
			"font-family": "Arial",
			"text-anchor": "middle",
			"font-size": 10,
		}

class Path(RaphaelElement):
	def __init__(self,d="M0,0",id=None):
		d = _parsePath(d)
		RaphaelElement.__init__(self,d=d,id=id)
		self.attrs["path"] = d
	def _xmlTag(self):
		return "path"

class Ellipse(RaphaelElement):
	def __init__(self,cx=0,cy=0,rx=0,ry=0,id=None):
		RaphaelElement.__init__(self,cx=cx,cy=cy,rx=rx,ry=ry,id=id)
	def _xmlTag(self):
		return "ellipse"

class Image(RaphaelElement):
	def __init__(self,src="",x=0,y=0,width=0,height=0,preserveAspectRatio=None,id=None):
		RaphaelElement.__init__(self,src=src,x=x,y=y,width=width,height=height,preserveAspectRatio=preserveAspectRatio,id=id)
	def _xmlTag(self):
		return "image"
	def _resetSpecific(self):
		self.attrs = self._attrs = {
		}
