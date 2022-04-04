import numpy as np
from ._FOVstr import _FOVstr
from .ReadIndex import ReadIndex

def CheckIndex(Radar,Date,frang=180.0,rsep=45.0,Model='chisham08'):
	'''
	Check whether a radar config already exists in the index.
	
	Inputs
	======
	======
	Radar : str
		Radar code
	Date : int
		Date in format yyyymmdd 	
	frang : float
		Distance to first range (km)
	rsep : float
		Range separation
	Model : str
		Virtual height model: 'chisham08'|'old'	
			
	Returns
	=======
	exists : bool
		True if the config already exists
	fname : str
		File name
	'''
	
	#get the fname
	s = _FOVstr(Radar,Date,frang,rsep,Model)
	fname = s + '.bin'
	
	#check if it is in the index already
	idx = ReadIndex()
	
	exists = fname in idx.fname
	return exists,fname
