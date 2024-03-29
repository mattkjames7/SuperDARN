import numpy as np
from .. import Globals
from ._FOVstr import _FOVstr
from .CheckIndex import CheckIndex
import PyFileIO as pf
from .RadarFOV import RadarFOV
import os
from .AddIndex import AddIndex

def SaveFOV(Radar,Date,frang=180.0,rsep=45.0,
				Altitude=400.0,Model='chisham08'):
	'''
	Save a field of view
	
	A file with a name based on all of the following input parameters
	will be created in $SUPERDARN_PATH/FOV/ which will be used in other
	functions.
	
	Inputs
	======
	Radar : str
		Radar code
	Date : int
		Date in format yyyymmdd 	
	frang : float
		Distance to first range (km)
	rsep : float
		Range separation
	Altitude : float
		Altitude for old virtual height model
	Model : str
		Virtual height model: 'chisham08'|'old'	
		
	
	'''
	#get the file name
#	s = _FOVstr(Radar,Date,frang,rsep,Model)
#	fname = s + '.bin'
	
	if not os.path.isdir(Globals.FOVPath):
		print()
		os.system('mkdir -pv '+Globals.FOVPath)
		
	
	#check the index file
	inidx,fname = CheckIndex(Radar,Date,frang,rsep,Model)
	
	#get the fov!
	fov = RadarFOV(Radar,Date,frang,rsep,Altitude,Model)
	
	#save it
	pf.SaveObject(fov,Globals.FOVPath + fname)
	#add to the index
	if not inidx:
		AddIndex(Radar,Date,frang,rsep,Model,fname)
	
	
