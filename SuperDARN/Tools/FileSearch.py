import fnmatch as fnm
import os as os
import numpy as np

def FileSearch(dirname,fname):
	'''
	Scan a directory for files using a pattern.
	
	Inputs
	======
	dirname : str
		name of the directory in which to search for the file
	fname : str
		Name of file to search for e.g. 'file.txt' or 'blah*.bin'
	
	Returns
	=======
	files : str
		Array of string with the file names which match the input fname
	
	'''
	
	
	if os.path.isdir(dirname) == False:
		return np.array([])
		
	files=np.array(os.listdir(dirname))
	files.sort()
	matches=np.zeros(np.size(files),dtype='bool')
	for i in range(0,np.size(files)):
		if fnm.fnmatch(files[i],fname):
			matches[i]=True
	
	good=np.where(matches == True)[0]
	if np.size(good) == 0:
		return np.array([])
	else:
		return np.array(files[good])
