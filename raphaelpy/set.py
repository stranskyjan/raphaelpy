class Set(object):
	"""list-like object to keep and operate several elements at once

	forEach method is not implemented, use

	.. code-block:: python

		s = paper.set(...)
		for elem in s:
			...

	instead.

	:param \*items: elements to be contained, either passed as single arguments or in a list/tuple

	.. code-block:: python

		s1 = paper.set([e1,e2,e3])
		s2 = paper.set(e4,e5,e6)
	"""
	def __init__(self,*items):
		if len(items)==0:
			self.items = []
		elif isinstance(items[0],(list,tuple)):
			self.items = list(items[0])
		else:
			self.items = list(items)
		self.paper = None
	def __len__(self):
		"""Returns number of containing elements"""
		return len(self.items)
	def __iter__(self):
		return iter(self.items)
	def clear(self):
		"""Removes all elements from the set"""
		self.items = []
	def exclude(self,elem):
		"""Removes given element from the set

		:param RaphaelElement elem:
		:return:
		:rtype: bool
		"""
		try:
			self.items.remove(elem)
			return True
		except ValueError:
			return False
	def pop(self):
		"""Removes last element and returns it.
		
		:rtype: RaphaelElement
		"""
		return self.items.pop()
	def push(self,*items):
		"""Adds each argument to the current set.

		.. code-block:: python

			s = paper.set(...)
			s.push(e1)
			s.push(e2,e3,e4)
		"""
		self.items.extend(items)
	def splice(self,index,count,*insertion):
		"""Removes given element from the set

		.. code-block:: python

			s = paper.set(e1,e2,e3,e4,e5,e6)
			s.splice(1,3) # list(s) is [e1,e5,e6]
			s = paper.set(e1,e2,e3,e4)
			s.splice(1,2,e5,e6,e7) # list(s) is [e1,e5,e6,e7,e4]
		"""
		i1 = self.items[:index]
		i2 = self.items[index+count:]
		self.items = i1 + list(insertion) + i2
	def attr(self,*args,**kw):
		for o in self.items:
			o.attr(*args,**kw)
