import numpy as np
from .. import Globals
import os
from ..Tools.FileSearch import FileSearch
from ..Tools.Today import Today
from ._ListHDW import _ListHDW
import DateTimeTools as TT

def _CheckHardware():
	'''
	Check if we have the hardware files/radar.dat. If we do, then check 
	when we last updated them.
	
	Returns
	=======
	exists : bool
		True if the files exist
	update : bool
		True if the files have been there for a while without checking
		for updates.
	
	'''
	
	#check for the hw directory
	hwpath = Globals.HardwarePath
	if not os.path.isdir(hwpath):
		exists = False
		update = True
		os.system('mkdir -pv '+hwpath)
		return exists,update
		
	#check if radar.dat exists
	rad = os.path.isfile(hwpath + 'radar.dat')
	hdw,_ = _ListHDW()
	if not rad or hdw.size == 0:
		#something missing, update
		exists = False
		update = True
	else:
		#it exists, but does it need updating?
		exists = True
		
		#check for 'lastupdate' file
		lu = hwpath + 'lastupdate'
		if os.path.isfile(lu):
			f = open(lu,'r')
			l = f.readline()
			f.close()
			udate = np.int32(l)
			cdate = Today()
			d = TT.DateDifference(udate,cdate)
			if d > 180:
				update = True
			else:
				update = False
		else:
			update = True
	
	return exists,update
			
	
	
