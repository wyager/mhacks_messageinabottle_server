# Spacial location server
# One BST for lat
# One BST for long

# The world is subdivided into 2^16 sections, for long and lat.

# Turn an int into a 16 bit bit array
switchify = lambda x : [(x >> (15-i)) & 1  for i in range(16)]
deg_to_sec = lambda x : round(x/360.0 * 65535)


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

class SpacialDB():
	def __init__(self):
		self.tree = SpacialTree()
	def insert(self, lat, lon, ID):
		self.tree.insert(deg_to_sec(lon), deg_to_sec(lat), ID)
	def get_at(self, lat, lon):
		return self.tree.find(deg_to_sec(lon), deg_to_sec(lat))
	def get_all(self, lat, lon):
		"Gets all bottles in the nearest 9 squares"
		xc = deg_to_sec(lon)
		yc = deg_to_sec(lat)
		bottles = []
		for x in range(xc-1, xc+1):
			x = x % 65536
			for y in range(yc-1, yc+1):
				y = y % 65536
				for bottle in self.tree.find(x, y):
					bottles.append(bottle)
		return bottles
	def remove_at(self, lat, lon, ID):
		self.tree.remove(deg_to_sec(lon), deg_to_sec(lat), ID)

if __name__ == '__main__':
	root = SpacialTree()
	print(root)
	print(root.find(100, 0))
	root.insert(100,0,"hello")
	root.insert(100,0,"hello2")
	root.insert(200,1,"hello")
	print(root.find(100, 0))
	print(root.find(100, 1))
	print(root.find(101, 0))
	print(root.find(200, 1))
	root.remove(100,0,"hello")



	db = SpacialDB()
	db.insert(100.0, 100.0, "test")
	print(db.get_all(100.0,100.0))
	db.insert(359.999, 0, "a")
	db.insert(0.001, 0, "b")
	print(db.get_all(0.0,0))
	db.remove_at(0.001, 0, "a")
	print(db.get_all(0.0,0))
	db.remove_at(359.999, 0, "a")
	print(db.get_all(0.0,0))
