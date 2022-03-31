import numpy as np
import PyFileIO as pf
from .. import Globals
import os

def ReadIndex():
	'''
	Read the index file
	
	Returns
	=======
	idx : numpy.recarray
		Record array with the field of view parameters.
	
	'''
	
	dtype = [	('Radar','object'),
				('Date','int32'),
				('frang','float32'),
				('rsep','float32'),
				('Model','object'),
				('fname','object') ] 
	
	idxfile = Globals.DataPath + 'fov.dat'		
		
	if not os.path.isfile(idxfile):
		return np.recarray(0,dtype=dtype)
		
	return pf.ReadASCIIData(idxfile,dtype=dtype)
