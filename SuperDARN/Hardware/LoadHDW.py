import numpy as np
from .. import Globals
from ._ReadRadarDat import _ReadRadarDat
from ._CheckHardware import _CheckHardware
from ._DownloadHDW import _DownloadHDW
from ._ReadHDWFiles import _ReadHDWFiles

def LoadHDW(Reload=False):
	'''
	Attempt to load the hardware files into memory.
	
	Inputs
	======
	Reload : bool
		Force reloading even if it is already in memory.
	
	'''
	
	#check if we have the hardware info
	exists,update = _CheckHardware()
	
	if not exists:
		print('Hardware info not found, attempting to download...')
		exists = _DownloadHDW()
		if not exists:
			print('Download failed')
		else:
			print('Download success!')
	elif update:
		print('Hardware files may need to be updated, run ')
		print('SuperDARN.Hardware.Update() to get the latest files')
		
	if exists:
		# read the radars file
		if Globals.Radars is None or Reload:
			Globals.Radars = _ReadRadarDat()
			
		# hdw
		if Globals.Hardware is None:
			Globals.Hardware = _ReadHDWFiles()
			
		
