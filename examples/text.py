from raphaelpy import *

paper = Raphael("text.svg",640,480)
#
x,y = 200,100
paper.path(["M",x-100,y,"h",200,"M",x,y-50,"v",100])
paper.text(x,y,"ABCDEFGH").attr(font_size=40)
#
x,y = 200,300
paper.path(["M",x-100,y,"h",200,"M",x,y-50,"v",100])
paper.text(x,y,"ABCDEF\nGHIJK").attr(font_size=40)
#
x,y = 450,100
paper.path(["M",x-100,y,"h",200,"M",x,y-50,"v",100])
paper.text(x,y,"ABCD\nEF\nGHIJK").attr(font_size=40,text_anchor="start")
#
x,y = 450,300
paper.path(["M",x-100,y,"h",200,"M",x,y-50,"v",100])
paper.text(x,y,"AB\nCDEF\nGHI\nJK").attr(font_size=40,text_anchor="end")
paper.save()
