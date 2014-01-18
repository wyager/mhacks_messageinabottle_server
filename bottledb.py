import spatialdb
# A bottle is a tuple (lat, lon, metadata)

class BottleDB():
	def __init__(self):
		self.spatialdb = SpatialDB()
		self.bottles = {}
	def remove_bottle(ID):
		if ID in bottles:
			lat, lon, data = bottles[ID]
			self.spatialdb.remove_at(lat, lon, ID)
			bottles.pop(ID)
	def add_bottle(ID, bottle):
		self.remove_bottle(ID) # If we're editing an existing bottle
		self.bottles[ID] = bottle
		lat, lon, data = bottle
		self.spatialdb.insert(lat, lon, ID)
	