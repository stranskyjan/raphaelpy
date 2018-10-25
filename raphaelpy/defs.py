from .utils import SvgElement

class Def(SvgElement):
	def add(self,elem):
		elem.remove()
		self.children.append(elem)
	def _xmlTag(self):
		raise NotImplementedError

class Pattern(Def):
	def __init__(self,x,y,width,height,patternUnits="userSpaceOnUse",id=None):
		Def.__init__(self,id)
		self.attr(x=x,y=y,width=width,height=height,patternUnits=patternUnits)
	def _xmlTag(self):
		return "pattern"

class Marker(Def):
	def __init__(self,refX,refY,markerWidth,markerHeight,markerUnits="strokeWidth",orient="auto",id=None):
		Def.__init__(self,id)
		self.attr(refX=refX,refY=refY,markerWidth=markerWidth,markerHeight=markerHeight,markerUnits=markerUnits,orient=orient)
	def _xmlTag(self):
		return "marker"

class ClipPath(Def):
	def _xmlTag(self):
		return "clipPath"

class LinearGradient(Def):
	def __init__(self,x1,y1,x2,y2,id=None):
		Def.__init__(self,id)
		self.attr(x1=x1,y1=y1,x2=x2,y2=y2)
	def _xmlTag(self):
		return "linearGradient"

class RadialGradient(Def):
	def __init__(self,fx,fy,stops=[],id=None):
		Def.__init__(self,id)
		self.attr(fx=fx,fy=fy)
	def _xmlTag(self):
		return "radialGradient"

class Stop(SvgElement):
	def __init__(self,stop_color,offset,stop_opacity=1,id=None):
		SvgElement.__init__(self,id)
		self.attr(stop_color=stop_color,offset=offset,stop_opacity=stop_opacity)
	def _xmlTag(self):
		return "stop"
