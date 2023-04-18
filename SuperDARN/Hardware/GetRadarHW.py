import numpy as np
from .. import Globals
from .LoadHDW import LoadHDW

def GetRadarHW(Radar,Date=None):
	'''
	Return the hardware data for a radar.
	
	Inputs
	======
	Radar : str
		Radar code
	Date : int
		Date in format yyyymmdd (optional)
		
	Returns
	=======
	hw : numpy.recarray
		Hardware info
	
		
	'''
	Rad = Radar.lower()
	
	#check that it is loaded
	if Globals.Hardware is None:
		LoadHDW()
		
	#check that the radar is a key
	if not Rad in Globals.Hardware:
		return None
	
	hw = Globals.Hardware[Rad]
	
	#select by date
	if not Date is None:
		use = np.where(hw.StartDate <= np.max(Date))[0]
		
		if use.size > 0:
			hw = hw[use[-1]]
		else:
			hw = hw[use]
			
	return hw
		

