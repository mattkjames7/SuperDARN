import numpy as np
from .. import Globals
from ..Tools.Today import Today
from .FOVObj import FOVObj
from ._FOVstr import _FOVstr
from ..Hardware.GetRadarHW import GetRadarHW

def GetFOV(Radar,Date=None,frang=180.0,rsep=45.0,
				Altitude=400.0,Model='chisham08'):

	'''
	Get a FOV object either from memory or file.
	
	'''
	#get hardware
	if Date is None:
		Date = Today()
	hw = GetRadarHW(Radar,Date)
	rDate = hw.EndDate
	
	#get the string 
	s = _FOVstr(Radar,rDate,frang,rsep,Model)
	
	#check if it exists in memory
	if not s in Globals.FOV:
		#no - so load it into memory
		Globals.FOV[s] = FOVObj(Radar,rDate,frang,rsep,Altitude,Model)
	
	
	return Globals.FOV[s]

	
