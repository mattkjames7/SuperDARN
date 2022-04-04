import numpy as np
from .GetFOV import GetFOV

def LatitudinalCellArray(Radar,Lon,dLon=0.4,Date=None,Mag=True,LatRange=None):
	'''
	Get a list of radar cells which approximately follow a line of
	constant longitude.
	
	Inputs
	======
	Radar : str
		Radar code
	Lon : float
		Desired longitude (degrees)
	dLon : float
		Acceptable longitude deviation of centre of the cell from Lon
		(degrees)
	Date : int
		Date in the format yyyymmdd - if None then today's date is used.
	Mag : bool
		If True (default) then magnetic coordinates are used, geographic
		otherwise.
	LatRange : float
		2 element array indicating the minimum and maximum latitudes
		to use.
		
	Returns
	=======
	beams : int
		Array of beam numbers
	gates : int
		Array of range gates
	lats : float
		Array of latitudes (magnetic if Mag=True)
	
	'''
		
	
	#get the fov
	fov = GetFOV(Radar,Date=Date)
	
	#get the fov coordinates
	lon,lat = fov.GetFOV(Center=True,Mag=Mag,Date=Date)
	
	#find all of the cells
	beams,gates = np.where((lon >= Lon-dLon) & (lon <= Lon+dLon))
	
	#get their longitudes
	lats = lat[beams,gates]
	
	#sort
	srt = np.argsort(lats)
	lats = lats[srt]
	beams = beams[srt]
	gates = gates[srt]
	
	#limit to longitude range
	if not LatRange is None:
		use = np.where((lats >= LatRange[0]) & (lats <= LatRange[1]))[0]
		lats = lats[use]
		beams = beams[use]
		gates = gates[use]
	
	return beams,gates,lats
	
