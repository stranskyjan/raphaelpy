from raphaelpy import *

W = 1200
H = 200

Raphael.el.fill = lambda this,v=None: this.attr("fill") if v is None else this.attr(fill=v)
Raphael.el.stroke = lambda this,v=None: this.attr("stroke") if v is None else this.attr(stroke=v)
Raphael.el.thick = lambda this: this.attr(stroke_width=5)

paper = Raphael("arrows.svg",W,H)

def path(x,y,i):
	return "M{},{}h40".format(x+i*60,y)
types = (
	"none",
	"classic",
	"block",
	"open",
	"oval",
	"diamond",
)
exts = (
	"",
	"long",
	"short",
	"narrow",
	"wide",
	"long-wide",
	"long-narrow",
	"short-wide",
	"short-narrow",
)
x,y0 = 20, 20
for type in types:
	y = y0
	for ext in exts:
		arrow = "{}-{}".format(type,ext) if ext else type
		attrss = (
			dict(arrow_end=arrow),
			dict(arrow_start=arrow),
			dict(arrow_end=arrow,arrow_start=arrow),
		)
		for i,attrs in enumerate(attrss):
			paper.path(path(x,y,i).format(y)).attr(stroke_width=4).attr(**attrs)
		y += 20
	x += 200

paper.save()
