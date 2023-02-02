import numpy as np
from .. import Globals
from ..Hardware.GetRadarHW import GetRadarHW
from ..Hardware.GetRadar import GetRadar
from .GetFOV import GetFOV

def PopulateFOV():
	'''
	Load all of the default fields of view into memory. If any of them
	don't exists yet, then this will attempt to calculate them and save
	them in $SUPERDARN_PATH/FOV/
	
	'''
	#get a list of the radars
	rads = GetRadar()
	nr = rads.size
	
	#load each one
	for i in range(0,nr):
		print('\rLoading Radar FOV {0} of {1}'.format(i+1,nr),end='')
		hw = GetRadarHW(rads.Code[i])
		for date in hw.StartDate:
			GetFOV(rads.Code[i],date)
	print()
	print('Done')
