from raphaelpy import Raphael

def init(fName):
	paper = Raphael(fName, 640, 480)
	circle = paper.circle(50,  50,  50)
	circle = paper.circle(590, 430, 50)
	return paper

# defualt
paper = init("viewbox1.svg")
paper.save()

# "zoomed" view, only top-left quarter is visible
paper = init("viewbox2.svg")
paper.setViewBox(w=320,h=240)
paper.save()

# "scaled" picture, displayed with half size
paper = init("viewbox3.svg")
paper.setSize(320,240)
paper.setViewBox(w=640,h=480) # not needed, default value from init()
paper.save()

# "scaled" picture, displayed with double size
paper = init("viewbox4.svg")
paper.setSize(1280,960)
paper.setViewBox(w=640,h=480) # not needed, default value from init()
paper.save()

# paper size is larger than viewbox, aligned to top-left
paper = init("viewbox5.svg")
paper.backgroundColor = None
paper.setViewBox(w=320,h=100,fit=False)
paper.save()

# same as previous, but centered
paper = init("viewbox6.svg")
paper.backgroundColor = None
paper.setViewBox(w=320,h=100,fit=True)
paper.save()

# same as previous two, now with h
paper = init("viewbox7.svg")
paper.backgroundColor = None
paper.setViewBox(w=100,h=240,fit=False)
paper.save()
#
paper = init("viewbox8.svg")
paper.backgroundColor = None
paper.setViewBox(w=100,h=240,fit=True)
paper.save()
