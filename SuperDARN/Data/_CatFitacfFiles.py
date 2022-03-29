import numpy as np
from .. import Globals
import os

def _CatFitacfFiles(filesp,files):
	'''
	Concatenate Fit ACF files into a single temporary file.
	
	'''
	
	#start by copying and unzipping individual files into a temp directory
	tmppath = Globals.DataPath+'tmp/' + '{:08d}/'.format(np.random.randint(0,99999999))
	os.system('mkdir -pv '+tmppath)

	tmpfiles = []
	for fp,fn in zip(filesp,files):
		os.system('cp -v '+fp+' '+tmppath+fn)
		os.system('bzip2 -dfq '+tmppath+fn)		
		tmpfiles.append(tmppath + os.path.splitext(fn)[0])

	#work out the command to execute
	catstr = 'cat '
	for tf in tmpfiles:
		catstr += tf + ' '
	catstr += ' > ' + tmppath + 'tmp.fitacf'
	
	#do it!
	os.system(catstr)
	
	#remove temporary files,except this one
	for tf in tmpfiles:
		os.system('rm '+tf)	
	
	#return the cat file and the tmp path
	return tmppath,tmppath + 'tmp.fitacf'
