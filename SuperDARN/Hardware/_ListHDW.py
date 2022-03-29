from ..Tools.FileSearch import FileSearch
from .. import Globals
import numpy as np

def _ListHDW():
	'''
	List the radar hdw files.
	
	Returns 
	=======
	files : str
		Names of the hdw files within the hdw directory
	rads : str
		Radar codes
		
	
	'''

	#scan for files
	files = FileSearch(Globals.HardwarePath + 'hdw/','hdw.dat.*')
	
	#extract radar codes
	rads = []
	for f in files:
		rads.append(f.split('.')[-1])
	rads = np.array(rads)
	
	return files,rads
