import numpy as np
from .GetFOV import GetFOV

def LongitudinalCellArray(Radar,Lat,dLat=0.4,Date=None,Mag=True,LonRange=None):
	'''
	Get a list of radar cells which approximately follow a line of
	constant latitude.
	
	Inputs
	======
	Radar : str
		Radar code
	Lat : float
		Desired latitude (degrees)
	dLat : float
		Acceptable latitude deviation of centre of the cell from Lat
		(degrees)
	Date : int
		Date in the format yyyymmdd - if None then today's date is used.
	Mag : bool
		If True (default) then magnetic coordinates are used, geographic
		otherwise.
	LonRange : float
		2 element array indicating the minimum and maximum longitudes
		to use.
		
	Returns
	=======
	beams : int
		Array of beam numbers
	gates : int
		Array of range gates
	lons : float
		Array of longitudes (magnetic if Mag=True)
	
	'''
	
	#get the fov
	fov = GetFOV(Radar,Date=Date)
	
	#get the fov coordinates
	lon,lat = fov.GetFOV(Center=True,Mag=Mag,Date=Date)
	
	#find all of the cells
	beams,gates = np.where((lat >= Lat-dLat) & (lat <= Lat+dLat))
	
	#get their longitudes
	lons = lon[beams,gates]
	
	#sort
	srt = np.argsort(lons)
	lons = lons[srt]
	beams = beams[srt]
	gates = gates[srt]
	
	#limit to longitude range
	if not LonRange is None:
		use = np.where((lons >= LonRange[0]) & (lons <= LonRange[1]))[0]
		lons = lons[use]
		beams = beams[use]
		gates = gates[use]
	
	return beams,gates,lons
	
