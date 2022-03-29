import numpy as np
import os

def _DelFitacfTemp(tpath,tfile):
	'''
	Delete a temporary file and the path it is in.
	
	Inputs
	======
	tpath : str
		Path to the temporary file
	tfile : str
		File name including path
	
	'''
	
	os.system('rm -v '+tfile)
	os.system('rm -rv '+tpath)
	
