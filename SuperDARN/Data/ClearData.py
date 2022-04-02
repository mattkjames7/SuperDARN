import numpy as np
from .. import Globals
from .MemUsage import MemUsage

def ClearData():
	'''
	Remove open fitacf data to free up memory.
	
	'''
	
	#get the size
	s = MemUsage()
	
	#clear data
	Globals.Data.clear()
	
	print('Freed {:6.1f} MB of memory'.format(s))
	
