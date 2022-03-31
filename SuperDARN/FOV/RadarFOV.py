import numpy as np
from ..Tools.Today import Today
from ..Hardware.GetRadarHW import GetRadarHW
from .FOVCoords import FOVCoords

def RadarFOV(Radar,Date=None,frang=180.0,rsep=45.0,
				Altitude=400.0,Model='chisham08'):
	'''
	Calculate the geographic coordinates for a radar's field of view.

	Inputs
	======
	Radar : str
		Radar code.
	Date : int
		Date in format yyyymmdd - if none is provided, then today's date
		will be used.
	frang : float
		Distance to first range (km)
	rsep : float
		Range separation
	rxrise : float
		Rx rise time (us)
	Altitude : float
		Altitude for old virtual height model
	Model : str
		Virtual height model: 'chisham08'|'old'
	
	Returns
	=======
	out : dict 
		Dictionary containing the following fields:
	
		glon : float
			Longitudes at the corners of each cell (nBeams+1,nGates+1)
		glat : float
			Latitudes at the corners of each cell (nBeams+1,nGates+1)
		glonc : float
			Longitudes at the centres of each cell (nBeams,nGates)
		glatc : float
			Latitudes at the centres of each cell (nBeams,nGates)
		gsglon : float
			Longitudes at the corners of each cell (nBeams+1,nGates+1)
			for ground scatter.
		gsglat : float
			Latitudes at the corners of each cell (nBeams+1,nGates+1)
			for ground scatter.
		gsglonc : float
			Longitudes at the centres of each cell (nBeams,nGates)
			for ground scatter.
		gsglatc : float
			Latitudes at the centres of each cell (nBeams,nGates)
			for ground scatter.	
	'''

	#check we have a valid date
	if Date is None:
		Date = Today()

	#get the hardware
	hw = GetRadarHW(Radar,Date)
	
	#output dict
	out = {}
	
	#fill it with a FOV
	tmp = FOVCoords(hw.Glon,hw.Glat,hw.Boresight,hw.nBeams,hw.nGates,hw.BeamSep,
					frang,rsep,hw.RxRiseT,Altitude,Model)
	fields = ['glon','glat','glonc','glatc','gsglon','gsglat','gsglonc','gsglatc']
	for f,t in zip(fields,tmp):
		out[f] = t
		
	return out
					
	
