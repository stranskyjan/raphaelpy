import os
import unittest
import tempfile
from raphaelpy import Paper,Rect,Circle,Text,Image,Path,Set

tmp = tempfile.gettempdir()
tmpf = os.path.join(tmp,"raphaelpytest.svg")
W = 640
H = 480

class TestPaper(unittest.TestCase):
	def setUp(self):
		self.p = Paper(tmpf,W,H)
	def paperAdd(self,i=1):
		if i >= 1:
			self.p.rect(10,20,100,200)
		if i >= 2:
			self.p.circle(60,70,20)
		if i >= 3:
			self.p.text(150,160,"abc")
	def test_none(self):
		self.assertEqual(None, self.p.bottom)
		self.assertEqual(None, self.p.bottom)
	def test_setSize(self):
		self.p.setSize(1,2)
		self.assertEqual((1,2),(self.p.width,self.p.height))
	def test_len(self):
		self.assertEqual(0, len(self.p))
		#
		self.paperAdd(2)
		self.assertEqual(2, len(self.p))
	def test_iter(self):
		elems = [e for e in self.p]
		self.assertEqual(0, len(elems))
		#
		self.paperAdd(2)
		elems = [e for e in self.p]
		self.assertEqual(2, len(elems))
		self.assertTrue(isinstance(elems[0],Rect))
		self.assertTrue(isinstance(elems[1],Circle))
	def test_clear(self):
		self.paperAdd(2)
		es = [e for e in self.p]
		self.p.clear()
		self.assertEqual(0, len(self.p))
		self.assertEqual(None, self.p.bottom)
		self.assertEqual(None, self.p.top)
		for e in es:
			for v in (e.next, e.prev, e.paper):
				self.assertEqual(None, v)
			self.assertEqual(-1, e.id)
	def test_getById(self):
		self.paperAdd(3)
		self.assertTrue(isinstance(self.p.getById(1), Rect))
		self.assertTrue(isinstance(self.p.getById(2), Circle))
		self.assertTrue(isinstance(self.p.getById(3), Text))
		self.assertEqual(None, self.p.getById(-1))
		self.assertEqual(None, self.p.getById(4))
		self.assertEqual(None, self.p.getById(123))
	def test_save(self):	
		self.paperAdd(3)
		self.p.save()
		with open(tmpf) as f:
			olines = f.readlines()
		olines = [l.rstrip() for l in olines]
		elines = [
			'<?xml version="1.0" encoding="utf-8" ?>',
			'<svg height="480" version="1.1" width="640" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">',
			'	<defs />',
			'	<rect fill="white" fill-opacity="1" height="480" id="0" rx="0" ry="0" stroke="none" stroke-opacity="1" stroke-width="1" width="640" x="0" y="0"/>',
			'	<rect fill="none" height="200" id="1" rx="0" ry="0" stroke="black" stroke-width="1" width="100" x="10" y="20"/>',
			'	<circle cx="60" cy="70" fill="none" id="2" r="20" stroke="black" stroke-width="1"/>',
			'	<text fill="black" font-family="Arial" id="3" stroke="none" text="abc" text-anchor="middle" x="150" y="160">abc</text>',
			'</svg>',
		]
		self.assertEqual(elines, olines)

class TestElement(unittest.TestCase):
	def setUp(self):
		self.p = paper = Paper("",640,480)
		self.r = paper.rect(10,20,30,40)
		self.c = paper.circle(20,30,40)
		self.t = paper.text(30,40,"abc")
		self.i = paper.image("",10,20)
		self.e = paper.ellipse(10,20,30,40)
		self.l = [self.r,self.c,self.t,self.i,self.e]
	def test_attr(self):
		self.assertEqual(None, self.r.attr("nothing"))
		self.assertEqual(10, self.r.attr("x"))
		self.assertEqual(40, self.r.attr("height"))
		#
		self.r.attr("x",42)
		self.assertEqual(42, self.r.attr("x"))
		#
		self.r.attr(x=1,y=2)
		self.assertEqual(1, self.r.attr("x"))
		self.assertEqual(2, self.r.attr("y"))
		#
		self.r.attr({"x":3, "y":4})
		self.assertEqual(3, self.r.attr("x"))
		self.assertEqual(4, self.r.attr("y"))
		#
		self.r.attr(dict(x=5,y=6))
		self.assertEqual(5, self.r.attr("x"))
		self.assertEqual(6, self.r.attr("y"))
		#
		e = dict(
			x = 5,
			y = 6,
			rx = 0,
			ry = 0,
			width = 30,
			height = 40,
			fill = None,
			stroke = 'black',
		)
		e["stroke-width"] = 1
		self.assertEqual(e, self.r.attr())
	def test_remove(self):
		r,c,t,i,e = self.l
		i.remove()
		self.assertEqual(None,i.next)
		self.assertEqual(None,i.prev)
		self.assertEqual(None,i.paper)
		self.assertEqual(list(self.p),[r,c,t,e])
	def test_insertAfterBefore(self):
		r,c,t,i,e = self.l
		i.insertAfter(c)
		self.assertEqual(list(self.p),[r,c,i,t,e])
		t.insertBefore(c)
		self.assertEqual(list(self.p),[r,t,c,i,e])
	def test_toBackFront(self):
		r,c,t,i,e = self.l
		c.toFront()
		self.assertEqual(self.p.top,c)
		i.toBack()
		self.assertEqual(self.p.bottom,i)
	# TODO


class TestSet(unittest.TestCase):
	def setUp(self):
		self.l = [Rect(),Circle(),Path(),Image()]
		self.s = Set(*self.l)
	def test_init(self):
		r,c,p,i = self.l
		s = Set()
		self.assertEqual(s.items,[])
		s = Set(r,c,p,i)
		self.assertEqual(s.items,self.l)
		s = Set([r,c,p,i])
		self.assertEqual(s.items,self.l)
	def test_len(self):
		self.assertEqual(len(self.s),4)
	def test_iter(self):
		self.assertEqual([e for e in self.s],self.l)
	def test_list(self):
		self.assertEqual(list(self.s),self.l)
	def test_clear(self):
		self.s.clear()
		self.assertEqual(self.s.items,[])
	def test_exclude(self):
		r,c,p,i = self.l
		self.s.exclude(p)
		self.assertEqual(self.s.items,[r,c,i])
		self.s.exclude(r)
		self.assertEqual(self.s.items,[c,i])
	def test_pop(self):
		r,c,p,i = self.l
		e = self.s.pop()
		self.assertEqual(e,i)
		self.assertEqual(self.s.items,[r,c,p])
	def test_push(self):
		r2,r3,r4 = [Rect() for _ in (0,1,2)]
		r,c,p,i = self.l
		self.s.push(r2)
		self.assertEqual(self.s.items,[r,c,p,i,r2])
		self.s.push(r3,r4)
		self.assertEqual(self.s.items,[r,c,p,i,r2,r3,r4])
	def test_splice(self):
		r2,r3,r4 = [Rect() for _ in (0,1,2)]
		r,c,p,i = self.l
		#
		self.s.splice(1,2)
		self.assertEqual(self.s.items,[r,i])
		#
		self.s.items = list(self.l)
		self.s.splice(1,2,r2)
		self.assertEqual(self.s.items,[r,r2,i])
		#
		self.s.items = list(self.l)
		self.s.splice(1,2,r2,r3,r4)
		self.assertEqual(self.s.items,[r,r2,r3,r4,i])
	def test_attr(self):
		self.s.attr(stroke='black')
		self.assertTrue(all(e.attr("stroke")=='black' for e in self.s))
