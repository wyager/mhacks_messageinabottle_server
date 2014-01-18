# Spacial location server
# One BST for lat
# One BST for long

# The world is subdivided into 2^16 sections, for long and lat.

# Turn an int into a 16 bit bit array
switchify = lambda x : [(x >> (15-i)) & 1  for i in range(16)]


# Bottle for tree lookups
class Bottle():
	__slots__ = ("x", "y", "ID")
	def __init__(self, coords, ID):
		self.x, self.y = coords
		self.id = ID


class Node():
	def __init__(self):
		self.children = None, None
		self.members = []
	def find(self, switches):
		if len(switches) == 0:
			return self.members
		else: # more switches to be made
			switch, *rest = switches
			if self.children[switch] == None:
				return []
			else:
				return self.children[switch].find(rest)
	def insert(self, switches, item):
		if len(switches) == 0:
			self.members.append(item)
		else: # More switches left
			switch, *rest = switches
			if self.children[switch] == None:
				if switch:
					self.children = self.children[0], Node()
				else:
					self.children = Node(), self.children[1]
			self.children[switch].insert(rest, item)

class SpacialTree():
	def __init__(self):
		self.root = Node()
	def find(self, x, y):
		return self.root.find(switchify(x))
	def insert(self, x, y, item):
		self.root.insert(switchify(x), item)