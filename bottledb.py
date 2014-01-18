import spatialdb
# A bottle is a tuple (lat, lon, metadata)

class BottleDB():
	def __init__(self):
		self.spatialdb = spatialdb.SpatialDB()
		self.bottles = {}
	def remove_bottle(self, ID):
		if ID in self.bottles:
			lat, lon, data = self.bottles[ID]
			self.spatialdb.remove_at(lat, lon, ID)
			self.bottles.pop(ID)
	def add_bottle(self, ID, bottle):
		self.remove_bottle(ID) # If we're editing an existing bottle
		self.bottles[ID] = bottle
		lat, lon, data = bottle
		self.spatialdb.insert(lat, lon, ID)
