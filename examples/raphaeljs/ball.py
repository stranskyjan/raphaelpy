from raphaelpy import *

def ball(this,x,y,r,hue=0):
	return this.set(
		this.ellipse(x, y + r - r / 5., r, r / 2.).attr(fill = "rhsb({0}, 1, .25)-hsba({0}, 1, .25,0)".format(hue), stroke = "none", opacity = 0),
		this.ellipse(x, y, r, r).attr(fill = "r(.5,.9)hsb({0}, 1, .75)-hsb({0}, .5, .25)".format(hue), stroke = "none"),
		this.ellipse(x, y, r - r / 5., r - r / 20.).attr(stroke = "none", fill = "r(.5,.1)rgb(204,204,204)-rgba(204,204,204,0)"),
	)
Raphael.fn.ball = ball

paper = Raphael("ball.svg",360,360)
x,y,r = 180, 180, 150
h = .5 # random.random())
paper.ball(x, y, r, h)
paper.save()
