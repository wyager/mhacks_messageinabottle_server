from math import sin, cos, sqrt, atan2, radians

# Returns distance between coords in km
def distance(c1, c2):
	R = 6373.0 # Earth radius, km
	lat1, lon1 = c1
	lat2, lon2 = c2
	lat1, lon1 = radians(lat1), radians(lon1)
	lat2, lon2 = radians(lat2), radians(lon2)
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
	c = 2 * atan2(sqrt(a), sqrt(1-a))
	distance = R * c
	return distance