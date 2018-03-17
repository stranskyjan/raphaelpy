from raphaelpy import *

W = 640
H = 480

Raphael.el.fill = lambda this,v=None: this.attr("fill") if v is None else this.attr(fill=v)

paper = Raphael("colors.svg",W,H)

paper.rect(20, 20,100,20).fill(" 0-#f00-#00f")
paper.rect(20, 40,100,20).fill(" 0-#f00-#00f-#0f0")
paper.rect(20, 60,100,20).fill(" 0-#f00-#00f-#f0f-#0f0")
paper.rect(20, 80,100,20).fill(" 0-#f00-#00f:20-#f0f:80%-#0f0")
paper.rect(20,100,100,20).fill("45-#f00-#00f")

paper.circle(160,40,20).fill("r#f00-#00f")
paper.circle(200,40,20).fill("r#f00-#00f-#0f0")
paper.circle(240,40,20).fill("r#f00-#00f-#f0f-#0f0")
paper.circle(280,40,20).fill("r#f00-#00f:20-#f0f:80-#0f0")
paper.circle(320,40,20).fill("r(.3,.3)#f00-#00f")
c = paper.circle(360,40,20).fill("r(.3,.3)#f00-#00f")
c._gradient.attr(cx=.2,cy=.2)

paper.rect(20,140,100,20).fill("lightseagreen")
paper.rect(20,160,100,20).fill("#2ba")
paper.rect(20,180,100,20).fill("#20b2aa")
paper.rect(20,200,100,20).fill("rgb(32,178,170)")
paper.rect(20,220,100,20).fill("rgb(32,70%,170)")
paper.rect(20,240,100,20).fill("rgba(32,178,170,.5)")
paper.rect(20,260,100,20).fill("rgba(32,70%,170,50%)")
paper.rect(20,280,100,20).fill("hsb(.492,.82,.7)")
paper.rect(20,300,100,20).fill("hsb(177deg,.82,70%)")
paper.rect(20,320,100,20).fill("hsba(.492,.82,.7,.5)")
paper.rect(20,340,100,20).fill("hsba(177deg,.82,70%,.5)")
paper.rect(20,360,100,20).fill("hsl(.492,.7,.41)")
paper.rect(20,380,100,20).fill("hsl(177deg,.7,41%)")
paper.rect(20,400,100,20).fill("hsla(.492,.7,.41,.5)")
paper.rect(20,420,100,20).fill("hsla(177deg,.7,41%,.5)")

paper.save()
