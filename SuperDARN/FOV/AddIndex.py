import numpy as np
from .. import Globals
from .ReadIndex import ReadIndex
import PyFileIO as pf

def AddIndex(Radar,Date,frang,rsep,Model,fname):
	'''
	Add FOV to the index file

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

	#read current index
	idx = ReadIndex()
	
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
