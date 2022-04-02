import numpy as np
import sys
from .. import Globals


def MemUsage():
	'''
	Calcualte the approximate memory usage in MB due to loading fitacf
	data.
	
	Returns
	=======
	s : float
		Size in MB
	
	'''
	s = 0
	for k in Globals.Data:
		s += sys.getsizeof(Globals.Data[k][0])
		s += sys.getsizeof(Globals.Data[k][1])
	s/= (1024*1024)	
	
	return s
