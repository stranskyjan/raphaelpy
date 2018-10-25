from math import pow,sqrt,cos,sin,radians,floor
import six
import re

def _underscoreToMinus(w):
	return w.replace("_","-")

def _packageRGB(r, g, b, o):
	from .raphael import Raphael
	r *= 255
	g *= 255
	b *= 255
	rgb = dict(
		r = r,
		g = g,
		b = b,
		hex = Raphael.rgb(r, g, b),
		opacity = o,
	)
	return rgb

_dasharrays = {
	"": [0],
	None: [0],
	"none": [0],
	"-": [3, 1],
	".": [1, 1],
	"-.": [3, 1, 1, 1],
	"-..": [3, 1, 1, 1, 1, 1],
	". ": [1, 3],
	"- ": [4, 3],
	"--": [8, 3],
	"- .": [4, 3, 1, 3],
	"--.": [8, 3, 1, 3],
	"--..": [8, 3, 1, 3, 1, 3]
}

_markers = dict(
	block = "M5,0 0,2.5 5,5z",
	classic = "M5,0 0,2.5 5,5 3.5,3 3.5,2z",
	diamond = "M2.5,0 5,2.5 2.5,5 0,2.5z",
	open = "M6,1 1,3.5 6,6",
	oval = "M2.5,0A2.5,2.5,0,0,1,2.5,5 2.5,2.5,0,0,1,2.5,0z",
)

def _parsePath(v):
	ret = v
	if isinstance(v,six.string_types):
		pass
	elif isinstance(v,(list,tuple)):
		ret = "" + v[0]
		prev = v[0]
		for e in v[1:]:
			if isinstance(e,six.string_types):
				ret += e
			elif isinstance(e,(int,float)):
				if isinstance(prev,(int,float)):
					ret += ","
				ret += str(e)
			else:
				raise RuntimeError
			prev = e
		# TODO
	else:
		raise RuntimeError("unsupported 'path' format: {}".format(v))
	return ret

def _parseColorAndOpacity(color):
	if color is None:
		return None,1
	color = color.strip()
	opacity = 1
	if color.startswith("#"):
		if len(color) == 7:
			r,g,b = [int(color[i:i+2],16) for i in (1,3,5)]
		elif len(color) == 4:
			r,g,b = [int(2*color[i],16) for i in (1,2,3)]
		else:
			raise RuntimeError
	elif color[-1] == ")":
		exp,lb,args = color.partition("(")
		args = args[:-1]
		args = [a.strip() for a in args.split(",")]
		a = "1"
		if exp in ("rgb","rgba"):
			if exp == "rgb":
				r,g,b = args
			elif exp == "rgba":
				r,g,b,a = args
			r,g,b = [(int(float(v[:-1])/100*255) if v.endswith("%") else int(v))for v in (r,g,b)]
		elif exp in ("hsb","hsba"):
			if exp == "hsb":
				h,s,v = args
			elif exp == "hsba":
				h,s,v,a = args
			if h.endswith("deg"):
				h = str(float(h[:-3]) / 360.)
			h,s,v = [(float(_[:-1])/100 if _.endswith("%") else float(_)) for _ in (h,s,v)]
			# https://gist.github.com/mathebox
			i = floor(h*6)
			f = h*6 - i
			p = v * (1-s)
			q = v * (1-f*s)
			t = v * (1-(1-f)*s)
			r, g, b = [
				(v, t, p),
				(q, v, p),
				(p, v, t),
				(p, q, v),
				(t, p, v),
				(v, p, q),
			][int(i%6)]
			r,g,b = [int(v*255) for v in (r,g,b)]
		elif exp in ("hsl","hsla"):
			if exp == "hsl":
				h,s,l = args
			elif exp == "hsla":
				h,s,l,a = args
			if h.endswith("deg"):
				h = str(float(h[:-3]) / 360.)
			h,s,l = [(float(v[:-1])/100 if v.endswith("%") else float(v)) for v in (h,s,l)]
			# https://gist.github.com/mathebox
			def hue_to_rgb(p, q, t):
				t += 1 if t < 0 else 0
				t -= 1 if t > 1 else 0
				if t < 1/6.: return p + (q - p) * 6 * t
				if t < 1/2.: return q
				if t < 2/3.: p + (q - p) * (2/3. - t) * 6
				return p
			if s == 0:
				r, g, b = l, l, l
			else:
				q = l * (1 + s) if l < 0.5 else l + s - l * s
				p = 2 * l - q
				r = hue_to_rgb(p, q, h + 1/3.)
				g = hue_to_rgb(p, q, h)
				b = hue_to_rgb(p, q, h - 1/3.)
			r,g,b = [int(v*255) for v in (r,g,b)]
		else:
			raise RuntimeError
		a = float(a[:-1])/100 if a.endswith("%") else float(a)
		opacity = a
	else:
		return color, 1
	#
	color = "#" + "".join(hex(v)[2:].rjust(2,"0") for v in (r,g,b))
	return color,opacity
def _parseColor(color):
	return _parseColorAndOpacity(color)[0]

def _parseTransform(transform):
	return transform # TODO

def _getGradient(v):
	if v is None:
		return None
	from .defs import LinearGradient, RadialGradient, Stop
	v = v.strip()
	if not "-" in v:
		return None
	t = "l" if v[0] in "0123456789" else "r" if v[0]=="r" else None
	items = v.split("-")
	colorL,opacityL = _parseColorAndOpacity(items[-1])
	if t == "l":
		angle = float(items[0])
		color0,opacity0 = _parseColorAndOpacity(items[1])
		colors = items[2:-1]
		vector = [0, 0, cos(radians(angle)), sin(radians(angle))]
		d = max(abs(vector[2]), abs(vector[3]))
		if d == 0:
			d = 1
		m = 1. / d
		vector[2] *= m
		vector[3] *= m
		if vector[2] < 0:
			vector[0] = -vector[2]
			vector[2] = 0;
		if vector[3] < 0:
			vector[1] = -vector[3]
			vector[3] = 0
		x1,y1,x2,y2 = vector
		ret = LinearGradient(x1,y1,x2,y2)
	elif t == "r":
		i0 = items[0]
		i0 = i0[1:]
		fx = fy = .5
		if i0.startswith("("):
			fxfy,rb,color0 = i0.partition(")")
			fxfy = fxfy[1:].split(",")
			fx,fy = [float(v) for v in fxfy]
		else:
			color0 = i0
		color0,opacity0 = _parseColorAndOpacity(color0)
		colors = items[1:-1]
		d = ((fy > .5) * 2 - 1)
		if pow(fx - .5, 2) + pow(fy - .5, 2) > .25:
			fy = sqrt(.25 - pow(fx - .5, 2)) * d + .5
			if fy != .5:
				fy = round(fy*10000)/10000. - 1e-5 * d
		ret = RadialGradient(fx,fy)
	else:
		raise RuntimeError
	stops = [Stop(color0,0,opacity0)]
	n = len(colors)+1
	for i,color in enumerate(colors):
		color,colon,offset = color.partition(":")
		if not offset:
			offset = (i+1)*100/n
		color,opacity = _parseColorAndOpacity(color)
		stops.append(Stop(color,offset,opacity))
	stops.append(Stop(colorL,100,opacityL))
	ret.children = stops
	return ret

def _addArrow(self,o,value,isEnd):
	from .element import Path
	if not isinstance(o,Path):
		return
	values = value.lower().split("-")
	paper = o.paper
	se = "end" if isEnd else "start"
	attr = o.attrs
	stroke = o.attr("stroke-width")
	i = len(values)
	type = "classic"
	w = 3
	h = 3
	t = 5
	for v in reversed(values):
		if v in ("block","classic","oval","diamond","open","none"):
			type = v
		if v == "wide":
			h = 5
		if v == "narrow":
			h = 2
		if v == "long":
			w = 5
		if v == "short":
			w = 2
	if type == "none":
		return
	elif type == "open":
		w += 2
		h += 2
		t += 2
		dx = 1
		refX = 4 if isEnd else 1
		attr = dict(
			fill = None,
			stroke = o.attr("stroke"),
		)
	else:
		refX = dx = .5*w
		attr = dict(
			fill = o.attr("stroke"),
			stroke = None,
		)
	pathId = "raphael-marker-arrow-path-{}-{}-obj{}".format(se,value,o.id)
	markerId = "raphael-marker-arrow-{}-obj{}".format(se,o.id)
	marker = paper.marker(refX,.5*h,w,h,markerId,orient="auto")
	t = float(t)
	p = Path(_markers.get(type,"M0,0")).attr(**attr).attr(
		stroke_linecap = "round",
		transform = ("rotate(180 {} {})".format(.5*w,.5*h) if isEnd else "") + "scale({},{})".format(w/t,h/t),
		stroke_width = 1. / ((w / t + h / t) / 2.),
	)
	marker.add(p)
	p.id = pathId
	if isEnd:
		o._markerEnd = marker
	else:
		o._markerStart = marker

def _addClipRect(self,o,value):
	from .element import Rect
	x,w,y,h = value
	paper = o.paper
	clipId = "clip-rect-{}".format(o.id)
	clip = paper.clipPath(id=clipId)
	clip.add(paper.rect(x,w,y,h))

class SvgElement(object):
	def __init__(self,id=None,**kw):
		self.id = id
		self.children = []
		self.reset()
		self.attr(**kw)
	def _xmlTag(self):
		raise NotImplementedError
	def attr(self,*args,**kw):
		"""Sets the attributes of the element.
		See `RaphaelJS attr <http://dmitrybaranovskiy.github.io/raphael/reference.html#Element.attr>`_ for more information.

		Parameters might be:

		:param str key: key to be set
		:param value: value to be set
		:return: self

		.. code-block:: python

			r1 = paper.rect(10,10,100,50)
			r1.attr("fill","red")

		or

		:param \**kw: key=value keywords argumennts
		:return: self

		.. code-block:: python

			r1.attr(stroke="blue")
			r2.attr(fill="red",stroke="blue",stroke_width=10)

		or

		:param dict attrs: {"key":value,...} attrs as dict (JavaScript compatible)
		:return: self

		.. code-block:: python

			r1.attr({"stroke-width": 10})
			r3.attr({"fill":"red","stroke":"blue","stroke-width":10})

		or

		:param str key: retrieves attr value of given name
		:return: required attr

		.. code-block:: python

			fill = r1.attr("fill")
		"""
		if len(args)==0 and len(kw)==0:
			ret = {}
			ret.update(self.attrs)
			return ret
		if len(args)==1 and len(kw)==0:
			a = args[0]
			if isinstance(a,str):
				a = _underscoreToMinus(a)
				return self.attrs.get(a)
			if isinstance(a,dict):
				a = dict((_underscoreToMinus(k),v) for k,v in a.items())
				return self.attr(**a)
			raise RuntimeError
		if len(args)==2 and len(kw)==0:
			k,v = args
			k = _underscoreToMinus(k)
			return self.attr(**{k:v})
		if len(args)==0:
			for k,v in kw.items():
				k = _underscoreToMinus(k)
				self._attr(k,v)
			return self
		raise NotImplementedError
	def _attr(self,k,v):
		self.attrs[k] = v
		if k == "text":
			return
		elif k == "path":
			k = "d"
			v = _parsePath(v)
		elif k == "arrow-end":
			k = "marker-end"
			self.paper._addArrow(self,v,True)
			v = "url(#raphael-marker-arrow-end-obj{})".format(self.id)
		elif k == "arrow-start":
			k = "marker-start"
			self.paper._addArrow(self,v,False)
			v = "url(#raphael-marker-arrow-start-obj{})".format(self.id)
		elif k == "stroke-dasharray":
			w = self.attr("stroke-width")
			v = ",".join(map(lambda _: str(w*_), _dasharrays.get(v,v)))
		elif k == "clip-rect":
			k = "clip-path"
			self.paper._addClipRect(self,v)
			v = "url(#clip-rect-{})".format(self.id)
		elif k == "fill":
			grad = _getGradient(v)
			if isinstance(v,six.string_types) and v.startswith("url("):
				pass
			elif grad:
				i = grad.id = "gradient-obj{}".format(self.id)
				self.paper._defs[i] = grad
				v = "url(#{})".format(i)
				self._gradient = grad
			else:
				v,o = _parseColorAndOpacity(v)
				self._attr("fill-opacity",o)
		elif k == "stroke":
			v,o = _parseColorAndOpacity(v)
			self._attr("stroke-opacity",o)
		elif k == "stop-color":
			v = _parseColor(v)
		elif k == "offset":
			v = str(v)
			if not v.endswith("%"):
				v += "%"
		elif k == "src":
			k = "href"
		elif k == "transform":
			v = _parseTransform(v)
		#
		self._attrs[k] = v
	def reset(self):
		self.attrs = self._attrs = {}
	def _toXmlString(self,indentN=0,indentChar="\t"):
		tag = self._xmlTag()
		text = self._attrs.get("text","")
		attrs = {} if self.id == None else dict(id=self.id)
		attrs.update(self._attrs)
		if "text" in attrs:
			del attrs["text"]
		attrs = dict((k,"none" if v is None else v) for k,v in attrs.items())
		ks = sorted(attrs.keys())
		attrs = [u'{}="{}"'.format(k,attrs[k]) for k in ks]
		attrs = u" ".join(attrs)
		indent = indentN*indentChar
		if not text and not self.children:
			return u'{}<{} {}/>\n'.format(indent,tag,attrs)
		if text:
			fontSize = self._attrs["font-size"]
			lines = text.split("\n")
			n = len(lines)
			dy0 = .275*fontSize - (n-1)*.6*fontSize
			dy1 = 1.2*fontSize
			indent1 = (indentN+1)*indentChar
			lines2 = []
			for i,line in enumerate(lines):
				x = self._attrs["x"]
				dy = dy0 if i==0 else dy1
				line = '{}<tspan x="{}" dy="{}">{}</tspan>'.format(indent1,x,dy,line)
				lines2.append(line)
			lines = "\n".join(lines2)
			return u'{indent}<text {attrs}>\n{lines}\n{indent}</text>\n'.format(indent=indent,attrs=attrs,lines=lines)
		indent2 = (indentN+1)*indentChar
		children = "".format(indent2).join(ch._toXmlString(indentN=indentN+1,indentChar=indentChar) for ch in self.children)
		return u'{}<{} {}>\n{}{}</{}>\n'.format(indent,tag,attrs,children,indent,tag)
