import numpy as np
from .GetFOV import GetFOV

def LatitudinalCellArray(Radar,Lon,dLon=0.4,Date=None,Mag=True,LatRange=None):
	
	
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
	
