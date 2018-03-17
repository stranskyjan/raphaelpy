# since the resulting is using external image, please open it in a web browser to see desired result

from raphaelpy import *

r = Raphael("reflection.svg",600,540,backgroundColor="#333")

src = "http://dmitrybaranovskiy.github.io/raphael/bd.jpg"
r.image(src, 140, 140, 320, 240)
r.image(src, 140, 380, 320, 240).attr(
	#transform = "s1-1",
	transform = "matrix(1,0,0,-1,0,1000)", # TODO
	opacity = .5,
)
r.rect(0, 380, 600, 160).attr(
	fill = "90-rgba(51,51,51,.5)-#333",
	stroke = "none",
)

r.save()
