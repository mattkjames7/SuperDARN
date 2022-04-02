import numpy as np
from .GetBeamData import GetBeamData
from ..Hardware.GetRadarHW import GetRadarHW

def GetRadarData(Radar,Date,ut):
	'''
	Get the data from a single beam of radar data
	
	Inputs
	======
	Radar : str
		Radar code
	Date : int
		Date in format yyyymmdd (can be a 2-element range)
	ut : float
		UT range in hours since the start of the day.
	
	Returns
	=======
	out : dict
		Data from each beam
	
	'''

	#get the number of beams for the radar
	hw = GetRadarHW(Radar,Date)
	nBeams = hw.nBeams
	
		
	#otuput dict
	out = {}
	for i in range(0,nBeams):
		out[i] = GetBeamData(Radar,Date,ut,i)
		
	return out
