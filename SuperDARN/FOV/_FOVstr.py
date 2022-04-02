import numpy as np


def _FOVstr(Radar,Date,frang=180.0,rsep=45.0,Model='chisham08'):
	'''
	Return a string to be used for the FOV file name
	
	'''
	
	
	#work out a unique file name for the config
	if Model == 'chisham08':
		m = 'c'
	else:
		m = 'o'

	fstr = '{:s}-{:08d}-{:06.1f}-{:05.1f}-{:s}'.format(Radar.lower(),Date,frang,rsep,m)
	
	return fstr
