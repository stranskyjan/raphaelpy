# examples from documentation (to test if it really works as is documented)

from raphaelpy import *

######################################################################
# README.md
######################################################################
# Creates canvas 320 x 200 at 10, 50
paper = Raphael("readme.svg", 320, 200)
# Creates circle at x = 50, y = 40, with radius 10
circle = paper.circle(50, 40, 10)
# Sets the fill attribute of the circle to red (#f00)
circle.attr("fill", "#f00")
# Sets the stroke attribute of the circle to blue
circle.attr("stroke", "#00f")
# Saves the resulting drawing to the file
paper.save()

######################################################################
# Raphael.el
######################################################################
Raphael.el.red = lambda this: this.attr(fill="#f00")
# Raphael.el has to be defined before calling Raphael **(!)**
paper = Raphael("el.svg",200,200)
# then use it
paper.circle(100, 100, 20).red()
paper.save()

######################################################################
# Raphael.fn
######################################################################
Raphael.fn.arrow = lambda this, x1, y1, x2, y2, size: this.path(["M",x1,y1,"L",x2,y2]).attr(stroke_width=size,arrow_end="classic")
# Raphael.fn has to be defined before calling Raphael **(!)**
paper = Raphael("fn.svg", 640, 480)
# then use it
paper.arrow(50, 50, 100, 200, 5).attr(fill="#f00")
paper.save()

######################################################################
# Raphael
######################################################################
paper = Raphael("raphael1.svg",640,480)
paper.rect(100,100,200,300)
paper.save()
paper = Raphael("raphael2.svg",640,480,backgroundColor='cyan')
paper.rect(100,100,200,300)
paper.save()
paper = Raphael("raphael3.svg",width=640,height=480)
paper.rect(100,100,200,300)
paper.save()
paper = Raphael("raphael4.svg",[0,0,640,480,
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
paper.save()

######################################################################
# Element.attr
######################################################################
paper = Raphael("element.attr.svg",640,480)
r1 = paper.rect(10,10,100,50)
# key-value pair arguments
r1.attr("fill","red")
# kwargs key=value
r1.attr(stroke="blue")
# dict {"key": value}
r1.attr({"stroke-width": 10})
# retrieve an attr value
print(r1.attr("fill"))
r2 = paper.rect(10,90,100,50)
# multiple fields at once as kwargs. Note using underscore in stroke_width instead of stroke-width
r2.attr(fill="red",stroke="blue",stroke_width=10)
r3 = paper.rect(10,170,100,50)
# multiple fields at once as dict
r3.attr({"fill":"red","stroke":"blue","stroke-width":10})
paper.save()

######################################################################
# Element.clone
######################################################################
paper = Raphael("element.clone.svg",640,480)
c1 = paper.circle(100,100,30).attr(fill="#f00",stroke="#00f",stroke_width=10)
c2 = c1.clone().attr(cx=300,cy=300)
paper.save()

######################################################################
# Element.remove
######################################################################
paper = Raphael("element.remove.1.svg",640,480)
r1 = paper.rect(100,100,400,300)
r2 = paper.rect(200,200,100,100)
paper.save()
paper.fileName = "element.remove.2.svg"
r2.remove()
paper.save()

######################################################################
# Element.insertAfter, insertBefore, toFront, toBack
######################################################################
def content(paper):
	e1 = paper.rect(100,100,100,100).attr(fill="red")
	e2 = paper.rect(110,110,100,100).attr(fill="orange")
	e3 = paper.rect(120,120,100,100).attr(fill="yellow")
	e4 = paper.rect(130,130,100,100).attr(fill="green")
	e5 = paper.rect(140,140,100,100).attr(fill="blue")
	e6 = paper.rect(150,150,100,100).attr(fill="blueviolet")
	return e1,e2,e3,e4,e5,e6
#
paper = Raphael("element.insertAfter.svg",640,480)
e1,e2,e3,e4,e5,e6 = content(paper)
e2.insertAfter(e4)
paper.save()
#
paper = Raphael("element.insertBefore.svg",640,480)
e1,e2,e3,e4,e5,e6 = content(paper)
e2.insertBefore(e4)
paper.save()
#
paper = Raphael("element.toFront.svg",640,480)
e1,e2,e3,e4,e5,e6 = content(paper)
e2.toFront()
paper.save()
#
paper = Raphael("element.toBack.svg",640,480)
e1,e2,e3,e4,e5,e6 = content(paper)
e2.toBack()
paper.save()

######################################################################
# defs
######################################################################
paper = Raphael("defs.svg",640,480)
#
path = paper.path(["M",0,50,"h",100,"l",-50,50,"h",100,"l",-50,150,"h",-50,"Z"])
clip = paper.clipPath("clip1")
clip.add(paper.path().attr(path=path.attr("path")))
paper.rect(20,20,100,200).attr(stroke_width=5,stroke="#f00",fill="#00f",clip_path="url(#clip1)")
#
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
#
m1 = paper.marker(5,5,10,10,"end1",orient="auto")
m1.add(paper.rect(0,0,10,10).attr(fill='black'))
m2 = paper.marker(5,5,10,10,"start1",orient="10deg")
m2.add(paper.rect(0,0,10,10).attr(fill='black'))
paper.path(["M",150,350,"l",50,-50,"l",50,25]).attr(marker_end="url(#end1)",marker_start="url(#start1)")
#
paper.save()

######################################################################
# defs
######################################################################
paper = Raphael("set.svg",640,480)
st = paper.set()
st.push(
    paper.circle(10, 10, 5),
    paper.circle(30, 10, 5)
)
st.attr({"fill": "red"})
paper.save()
