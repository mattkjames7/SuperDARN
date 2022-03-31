import numpy as np
from datetime import date


def Today():
	'''
	Get today's date.
	
	Returns
	=======
	tdate : int
		Date in the format yyyymmdd
	'''
	
	
	tdate = np.int32(date.today().strftime('%Y%m%d'))
	
	return tdate
