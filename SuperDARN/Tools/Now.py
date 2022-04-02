import numpy as np
from datetime import datetime

def Now():
	'''
	Return the current time in hours since the start of the day.
	
	Returns
	=======
	ut : float
		Time in hours since the start of the day.
	
	'''
	
	now = datetime.utcnow()
	ut = now.hour + now.minute/60.0 + now.second/3600.0

	return ut
