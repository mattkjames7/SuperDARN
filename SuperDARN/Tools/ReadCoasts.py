import numpy as np
from .. import Globals


def ReadCoasts():
	'''
	Read in the coordinates of the coasts
	
	Returns
	=======
	lon : float
		coastline longitudes
	lat : float
		coastline latitudes
	
	'''
	#read the file
	fname = Globals.ModulePath + 'Coasts.dat'
	f = open(fname,'r')
	lines = f.readlines()
	f.close()
	
	#extract the coordinates
	nl = np.size(lines)
	ints = np.int32(lines[0].split()) 
	nBlock = ints[0]
	BlockLen = ints[1:]
	lats,lons = np.float32(''.join(lines[1:]).split()).reshape((2,np.sum(BlockLen)),order='F')
	
	return lons,lats
