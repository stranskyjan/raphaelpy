from math import pi,sin,cos
from raphaelpy import *

W = 640
H = 480

Raphael.el.fill = lambda this,v=None: this.attr("fill") if v is None else this.attr(fill=v)
Raphael.el.stroke = lambda this,v=None: this.attr("stroke") if v is None else this.attr(stroke=v)
Raphael.el.thick = lambda this: this.attr(stroke_width=5)
Raphael.el.mediumThick = lambda this: this.attr(stroke_width=3)

def star(this,cx,cy,r,n=4):
	r0 = .4*r
	a,da = 0, pi/n
	p = []
	for i in xrange(n):
		for rr in (r,r0):
			x = cx + rr*sin(a)
			y = cy - rr*cos(a)
			p.extend(("L",x,y))
			a += da
	p.append("Z")
	p[0] = "M"
	return this.path(p)
Raphael.fn.star = star

paper = Raphael("1.svg",W,H)
paper.rect(0,0,W,H).stroke(null).fill('white')
paper.rect(10,20,100,200).stroke('red').fill('blue').thick()
paper.circle().stroke('magenta').fill('cyan').attr(cx=300,cy=300,r=30).mediumThick()
paper.text(50,50,"abcd").attr(font_size=30,fill='green')
paper.star(300,300,100)
paper.star(400,400,50,5).fill('blue')
paper.save()
