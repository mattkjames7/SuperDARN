import numpy as np
from .ConvertGeo import ConvertGeo

def ConvertGeoCart(lon,lat,Date=None,ut=None,Mag=False,Lon=False,Method='aacgm',Hemisphere='north'):
	'''
	Converts geographic longitudes and latitudes to whatever coordinates
	are required for the Cartesian polar axis plot.
	
	Inputs
	======
	lon : float
		longitude(s) in degrees
	lat : float
		latitude(s) in degrees
	Date : int
		Date in format yyyymmdd
	ut : float
		UT in hours since the start of the day
	Mag : bool
		If True, magnet coordinates are returned
	Lon : 
		If True, azimuthal coordinate is longitude, if False then it is
		local time.
	Method : str
		'aacgm'|'igrf'
		
	Returns
	=======
	x : float
		x-coordinate on the plot axes
	y : float
		y-coordinate on the plot axes
	
	'''
	#get the coordinates for the matplotlib polar plot
	t,r = ConvertGeo(lon,lat,Date=Date,ut=ut,Mag=Mag,Lon=Lon,Method=Method)
	if Hemisphere.lower() in ['south','s']:
		r = -r
		
	#convert those to Cartesians
	R = 90 - r
	y = -R*np.cos(t)
	x = R*np.sin(t)
	
	return x,y
