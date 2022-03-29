import numpy as np
from .. import Globals
from ._ListHDW import _ListHDW
from ._ReadHDW import _ReadHDW

def _ReadHDWFiles():
	'''
	Find and read all of the radar hardware files.
	
	Returns
	=======
	out : dict
		Hardware info for each radar
	
	'''
	
	#find the files
	files,rads = _ListHDW()
	
	#read them all
	hwpath = Globals.HardwarePath + 'hdw/'
	out = {}
	for f,r in zip(files,rads):
		out[r] = _ReadHDW(hwpath + f)
		try:
			out[r] = _ReadHDW(hwpath + f)
		except:
			print('Reading {:s} failed'.format(f))
			out[r] = 'missing'
			
			
	return out
