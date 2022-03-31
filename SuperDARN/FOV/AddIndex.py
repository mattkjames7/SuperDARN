import numpy as np
from .. import Globals
from .ReadIndex import ReadIndex

def AddIndex(Radar,Date,frang,rsep,Model,fname):
	'''
	Add FOV to the index file
	
	'''

	#read current index
	idx = ReadFOVIndex()
	
	#check if it currently exists
	if fname in idx.fname:
		#do nothing
		pass
	else:
		#add it
		newidx = np.recarray(idx.size + 1,dtype=idx.dtype)
		newidx[:-1] = idx
		newidx[-1].Radar = Radar
		newidx[-1].Date = Date
		newidx[-1].frang = frang
		newidx[-1].rsep = rsep
		newidx[-1].Model = Model
		newidx[-1].fname = fname

		#save it
		idxfile = Globals.DataPath + 'fov.dat'	
		pf.WriteASCIIData(idxfile,newidx)
