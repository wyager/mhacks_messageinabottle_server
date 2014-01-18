# Spacial location server
# One BST for lat
# One BST for long

# The world is subdivided into 2^16 sections, for long and lat.

# Turn an int into a 16 bit bit array
switchify = lambda x : [(x >> (15-i)) & 1  for i in range(16)]
deg_to_sec = lambda x : x/360.0 * 65535

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
	def remove(self, switches, value):
		if len(switches) == 0:
			self.members = [i for i in self.members if i != value]
		else: # More switches left
			switch, *rest = switches
			if self.children[switch] != None:
				self.children[switch].remove(rest, value)

class SpacialTree():
	def __init__(self):
		self.root = Node()
	def find(self, x, y):
		latnodes = self.root.find(switchify(x)) # Note that find() returns a list, even though we only ever expect one item per longnode find()
		if len(latnodes) == 0:
			return []
		else:
			return latnodes[0].find(switchify(y))
	def insert(self, x, y, item):
		latnodes = self.root.find(switchify(x))
		if len(latnodes) == 0:
			latnode = Node()
			self.root.insert(switchify(x), latnode)
		else:
			latnode = latnodes[0]
		latnode.insert(switchify(y), item)
	def remove(self, x, y, item):
		latnodes = self.root.find(switchify(x))
		if len(latnodes) != 0:
			latnode = latnodes[0]
			latnode.remove(switchify(y), item)


