import numpy as np

'''
The equations used to work this out come from the "Finding way-points"
section of:
https://en.wikipedia.org/wiki/Great-circle_navigation


'''

def _RangeCoords(rlon,rlat,rang,bs):
	'''
	Work out the geographic coordinates of a range beam based on the
	radar position, boresight and ground ranges. The equations used to 
	work this out come from the "Finding way-points" section of:
	https://en.wikipedia.org/wiki/Great-circle_navigation
	
	Inputs
	======
	rlon : float
		radar longitude (deg)
	rlat : float
		radar latitude (deg)
	rang : float
		Angular distance(s) from the radar (deg)
	bs : float
		boresight of the beam (deg) - angle is positive clockwise of
		north
	
	Returns
	=======
	lon : float
		Longitudes along the beam (deg)
	lat : float
		Latitudes along the beam (deg)
			
	'''
	#convert to radians
	dtr = np.pi/180.0
	alpha1 = bs*dtr
	lat1 = rlat*dtr
	lon1 = rlon*dtr
	sigma12 = rang*dtr
	
	#calculate the equatorial node
	lon0,alpha0,sigma01 = _EquatorNode(lon1,lat1,alpha1)
	
	#now work out the positions along the beam
	lon2r,lat2r = _RangeAngleCoords(sigma12,lon0,alpha0,sigma01)
	
	#convert to degrees
	lon = lon2r/dtr % 360.0
	lat = lat2r/dtr
	
	return lon,lat

def _EquatorNode(lon1,lat1,alpha1):
	'''
	Work out the position of the equatorial node given the position and
	boresight of the radar beam (calculate the beam boresight based on
	that of the radar and the beam separation)
	
	Inputs
	======
	lon1 : float
		radar longitude (rad)
	lat : float
		radar latitude (rad)
	alpha1 : float
		boresight of the beam (rad) - angle is positive clockwise of
		north
	
	Returns
	=======
	lon0 : float
		longitude of equatorial node crossing (rad)
	alpha0 : float
		course at the equator (rad)
	sigma01 : float
		angular distance between equatorial node and the radar (rad)
	'''


	
	#some trig
	sinalpha1 = np.sin(alpha1)
	cosalpha1 = np.cos(alpha1)
	coslat1 = np.cos(lat1)
	sinlat1 = np.sin(lat1)
	tanlat1 = np.tan(lat1)
	sin2alpha1 = sinalpha1*sinalpha1
	cos2alpha1 = cosalpha1*cosalpha1
	sin2lat1 = sinlat1*sinlat1
	
	#calculate alpha0 (course at the equator)
	alpha0 = np.arctan2(sinalpha1*coslat1,np.sqrt(cos2alpha1 + sin2alpha1*sin2lat1))

	#work out the angular distance between equatorial node and the radar
	sigma01 = np.arctan2(tanlat1,cosalpha1)
	
	#work out the longitude
	sinalpha0 = np.sin(alpha0)
	sinsigma01 = np.sin(sigma01)
	cossigma01 = np.cos(sigma01)
	
	lambda01 = np.arctan2(sinalpha0*sinsigma01,cossigma01)
	lon0 = (lon1 - lambda01) % (2*np.pi)
	
	return lon0,alpha0,sigma01


def _RangeAngleCoords(sigma12,lon0,alpha0,sigma01):
	'''
	Calculate the geographic coordinates of a range gate (or array of)
	
	Inputs
	======
	sigma12 : float
		Angular distance from the radar to the range gate (rad)
	lon0 : float
		longitude of equatorial node crossing (rad)
	alpha0 : float
		course at the equator (rad)
	sigma01 : float
		angular distance between equatorial node and the radar (rad)
	
	Returns
	=======
	lon2 : float
		longitudes of ranges
	lat2 : float
		latitudes of ranges
	
	'''
	#calculate angular distance from node to new point
	sigma02 = sigma01 + sigma12
		
	#calculate the new latitude
	cosalpha0 = np.cos(alpha0)
	sinalpha0 = np.sin(alpha0)
	sin2alpha0 = sinalpha0*sinalpha0
	cossigma02 = np.cos(sigma02)
	sinsigma02 = np.sin(sigma02)
	cos2sigma02 = cossigma02*cossigma02
	sin2sigma02 = sinsigma02*sinsigma02
	lat2 = np.arctan(cosalpha0*sinsigma02/np.sqrt(cos2sigma02 + sin2alpha0*sin2sigma02))
	
	#new longitude
	dlambda02 = np.arctan2(sinalpha0*sinsigma02,cossigma02)
	lon2 = dlambda02 + lon0
	
	return lon2,lat2
