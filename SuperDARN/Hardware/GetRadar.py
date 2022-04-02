import numpy as np
from .. import Globals


def GetRadar(Radar=None):
	'''
	Return the entry from radar.dat (or the whole thing if no radar is
	specified).
	
	Inputs
	======
	Radar : str|None
		Radar code.
		
	Returns
	=======
	out : numpy.recarray
		radar.dat entry
	
	'''
	
	if Radar is None:
		return Globals.Radars
	else: 
		try:
			use = np.where(Radar.lower() == Globals.Radars.Code)[0][0]
		except:
			print('Radar: {:s} not found'.format(Radar))
			return None
		
		return Globals.Radars[use]
	
