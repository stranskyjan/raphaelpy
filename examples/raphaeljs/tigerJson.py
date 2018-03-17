import json
from raphaelpy import *

with open('tiger.json') as f:
	tiger = json.load(f)
paper = Raphael("tiger2.svg",tiger)
for elem in paper:
	elem.attr(transform="translate(200,200)")
paper.save()
