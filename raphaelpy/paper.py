import codecs
from .utils import _addArrow,_addClipRect
from .element import *
from .defs import *
from .set import *

class Paper(object):
	"""Paper class, used to create and manage :class:`Raphael element <RaphaelElement>` and to save final drawing.
	
	See :meth:`Raphael <_Raphael.__call__>` for possible arguments.
	
	``forEach`` is not implemented, use
	
	.. code-block:: python
	
		for elem in paper:
		   ...
	
	instead.
	"""
	def __init__(self,fileName,*args,**kw):
		self.fileName = fileName
		#: Points to the bottom :class:`element <RaphaelElement>` on the paper
		self.bottom = None
		#: Points to the topmost :class:`element <RaphaelElement>` on the paper
		self.top = None
		self._reset()
		funcs = []
		if len(args) == 2 and all(isinstance(a,(int,float)) for a in args):
			w,h = args
		elif kw.get("width") is not None and kw.get("height") is not None:
			w = kw["width"]
			h = kw["height"]
		elif len(args)==1 and isinstance(args[0],(tuple,list)):
			a = args[0]
			x,y,w,h = a[:4]
			a = a[4:]
			for e in a:
				assert isinstance(e,dict)
				type = e.pop("type")
				func = getattr(self,type)
				funcs.append((func,e))
		else:
			raise RuntimeError
		self.setSize(w,h)
		self._processElemsByDescription(funcs)
		self.backgroundColor = kw.get("backgroundColor","white")
	def _processElemsByDescription(self,funcs):
		for func,kw in funcs:
			func().attr(**kw)
	def _reset(self):
		self.bottom = None
		self.top = None
		self._oid = 0
		self._defs = {}
	def _addArrow(self,o,value,isEnd):
		_addArrow(self,o,value,isEnd)
	def _addClipRect(self,o,value):
		_addClipRect(self,o,value)
	def setSize(self,width,height):
		self.width = width
		self.height = height
	def __iter__(self):
		return _PaperIterator(self)
	def clear(self):
		"""Clears the paper, i.e. removes all the elements."""
		while self.top:
			self.top.remove()
	def getById(self,id):
		"""Returns you element by its internal ID.
		
		:param int id: id
		:return: Raphael element object or None
		:rtype: RaphaelElement
		"""
		for elem in self:
			if elem.id == id:
				return elem
		return None
	def setViewBox(self):
		raise NotImplementedError
	def _toFileLines(self,indentChar="\t"):
		ret = [
			'<?xml version="1.0" encoding="utf-8" ?>\n',
			'<svg height="{height}" version="1.1" width="{width}" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">\n'.format(width=self.width,height=self.height),
		]
		#
		ks = sorted(self._defs.keys())
		defs = SvgElement()
		defs._xmlTag = lambda: "defs"
		defs.children = [self._defs[k] for k in ks]
		ret.append(defs._toXmlString(indentN=1,indentChar=indentChar))
		#
		ret.extend(elem._toXmlString(indentN=1,indentChar=indentChar) for elem in self)
		#
		ret.append("</svg>\n")
		return ret
	def _preSave(self):
		for elem in self:
			color = elem.attr("stroke")
			markers = filter(None, (elem._markerStart, elem._markerEnd))
			for m in markers:
				for e in m.children:
					if e.attr("stroke"):
						e.attr(stroke=color)
					if e.attr("fill"):
						e.attr(fill=color)
	def save(self,indentChar="\t"):
		"""Saves current content into file"""
		self._preSave()
		bg = None
		if self.backgroundColor:
			bg = self.rect(0,0,self.width,self.height).attr(stroke=None,fill=self.backgroundColor).toBack()
			bg.id = 0
		if not self.fileName:
			raise RuntimeError
		lines = self._toFileLines(indentChar=indentChar)
		with codecs.open(self.fileName,'w',encoding='utf-8') as f:
			f.writelines(lines)
		if bg:
			bg.remove()
	def __len__(self):
		"""Returns number of containing elements"""
		ret = 0
		for elem in self:
			ret += 1
		return ret
	def _add(self,elem):
		assert elem._hasNoPrevNorNext()
		if self.bottom is None:
			self.bottom = self.top = elem
		else:
			elem.prev = self.top
			self.top.next = elem
			self.top = elem
	def _remove(self,elem):
		if elem is self.bottom and elem is self.top:
			self.bottom = self.top = None
		elif elem is self.bottom:
			self.bottom = elem.next
			self.bottom.prev = None
		elif elem is self.top:
			self.top = elem.prev
			self.top.next = None
		else:
			elem.prev.next = elem.next
			elem.next.prev = elem.prev
		elem.next = elem.prev = None
	def _insert(self,prev,elem,next):
		assert elem._hasNoPrevNorNext()
		next.prev = elem
		prev.next = elem
		elem.prev = prev
		elem.next = next
	def _insertAfter(self,prev,elem):
		assert elem._hasNoPrevNorNext()
		if prev is self.top:
			self._add(elem)
			return
		self._insert(prev,elem,prev.next)
	def _insertBefore(self,next,elem):
		assert elem._hasNoPrevNorNext()
		if self.bottom is None:
			self._add(elem)
		elif next is self.bottom:
			elem.next = next
			next.prev = elem
			self.bottom = elem
		else:
			self._insert(next.prev,elem,next)
	def _create(self,Type,*args,**kw):
		ret = Type(*args,**kw)
		ret.id = self._oid + 1
		self._oid += 1
		ret.paper = self
		self._add(ret)
		return ret
#
	def rect(self,*args,**kw):
		"""Draws a rectangle.
		
		:param number x: x coordinate of the top left corner
		:param number y: y coordinate of the top left corner
		:param number width: width
		:param number height: height
		:param number r: radius for rounded corners, default is 0
		:return: new Raphael element object of type "Rect"
		:rtype: RaphaelElement
		"""
		return self._create(Rect,*args,**kw)
	def circle(self,*args,**kw):
		"""Draws a circle
		
		:param number cx: x coordinate of the center
		:param number cy: y coordinate of the center
		:param number r: radius
		:return: new Raphael element object of type "Circle"
		:rtype: RaphaelElement	
		"""
		return self._create(Circle,*args,**kw)
	def text(self,*args,**kw):
		"""Draws a text string.
		
		:param number x: x coordinate position
		:param number y: y coordinate position
		:param str text: the text string to draw
		:return: new Raphael element object of type "Text"
		:rtype: RaphaelElement
		"""
		return self._create(Text,*args,**kw)
	def path(self,*args,**kw):
		"""Creates a path element by given path data string.
		
		:param str|list d: SVG path string or corresponding list
		:return: new Raphael element object of type "Path"
		:rtype: RaphaelElement
		"""
		return self._create(Path,*args,**kw)
	def ellipse(self,*args,**kw):
		"""Draws an ellipse
		
		:param number x: x coordinate of the center
		:param number y: y coordinate of the center
		:param number rx: horizontal radius
		:param number ry: vertical radius
		:return: new Raphael element object of type "Ellipse"
		:rtype: RaphaelElement
		"""
		return self._create(Ellipse,*args,**kw)
	def image(self,*args,**kw):
		"""Embeds an image.
		
		:param str src: URI of the source image
		:param number x: x coordinate position
		:param number y: y coordinate position
		:param number width: width of the image
		:param number height: height of the image
		:return: new Raphael element object of type "Image"
		:rtype: RaphaelElement
		"""
		return self._create(Image,*args,**kw)
# TODO
#
	def _addDef(self,ret):
		ret.paper = self
		self._defs[ret.id] = ret
		return ret
	def pattern(self,x,y,width,height,id=None,**kw):
		"""Creates a SVG pattern, used e.g. as a hatching fill
		
		:param str id: unique id for reference
		:return: new Pattern element
		
		.. code-block:: python
		
			w = h = 30
			r = 4
			pattern = paper.pattern(0,0,w,h,"dotted")
			pattern.add(paper.rect(0,0,w,h).attr(fill='white',stroke=null))
			pattern.add(paper.circle(.15*w,.25*h,r).attr(fill='black',stroke=null))
			pattern.add(paper.circle(.65*w,.25*h,r).attr(fill='black',stroke=null))
			pattern.add(paper.circle(-.1*w,.75*h,r).attr(fill='black',stroke=null))
			pattern.add(paper.circle( .4*w,.75*h,r).attr(fill='black',stroke=null))
			pattern.add(paper.circle( .9*w,.75*h,r).attr(fill='black',stroke=null))
			paper.rect(200,50,200,100).attr(fill="url(#dotted)")
		"""
		return self._addDef(Pattern(x,y,width,height,id=id,**kw))
	def marker(self,refX,refY,markerWidth,markerHeight,id=None,**kw):
		"""Creates a SVG marker, used e.g. as a line ending
		
		.. code-block:: python
		
			m1 = paper.marker(5,5,10,10,"end1",orient="auto")
			m1.add(paper.rect(0,0,10,10).attr(fill='black'))
			m2 = paper.marker(5,5,10,10,"start1",orient="10deg")
			m2.add(paper.rect(0,0,10,10).attr(fill='black'))
			paper.path(["M",150,350,"l",50,-50,"l",50,25]).attr(marker_end="url(#end1)",marker_start="url(#start1)")
		"""
		return self._addDef(Marker(refX,refY,markerWidth,markerHeight,id=id,**kw))
	def clipPath(self,id=None):
		"""Creates clip path to clip an element
		
		:param str id: unique id for reference
		:return: new ClipPath element
		
		.. code-block:: python
		
			path = paper.path(["M",0,50,"h",100,"l",-50,50,"h",100,"l",-50,150,"h",-50,"Z"])
			clip = paper.clipPath("clip1")
			clip.add(paper.path().attr(path=path.attr("path")))
			paper.rect(20,20,100,200).attr(stroke_width=5,stroke="#f00",fill="#00f",clip_path="url(#clip1)")
		"""
		return self._addDef(ClipPath(id=id))
#
	def set(self,*elems):
		"""Creates :class:`list-like object <Set>` to keep and operate several elements at once.
		
		.. code-block:: python
		
			st = paper.set()
			st.push(
			   paper.circle(10, 10, 5),
			   paper.circle(30, 10, 5)
			)
			st.attr({"fill": "red"})
		"""
		ret = Set(*elems)
		ret.paper = self
		return ret
	def setStart(self):
		"""Not implemented yet ..."""
		raise NotImplementedError
	def setFinish(self):
		"""Not implemented yet ..."""
		raise NotImplementedError


class _PaperIterator(object):
	def __init__(self,paper):
		self.paper = paper
		self.current = paper.bottom
	def __next__(self):
		ret = self.current
		if ret is None:
			raise StopIteration
		self.current = self.current.next
		return ret
	def next(self):
		return self.__next__()
