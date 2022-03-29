import numpy as np
from .. import Globals
from ._ReadFitacf import _ReadFitacf
import DateTimeTools as TT
from ._GetFitacfFiles import _GetFitacfFiles 
from ._CatFitacfFiles import _CatFitacfFiles
from ._DelFitacfTemp import _DelFitacfTemp

def _ReadFitacfFiles(Radar,Date,ut=[0.0,24.0]):
	'''
	Find the appropriate fitacf files for a radar between a set of
	dates and times, then read them in.
	
	
	'''
	
	#get the list of file names
	filesp,files = _GetFitacfFiles(Radar,Date,ut)
	print('cat')
	print(files)
	print(filesp)
	
	#concatenate the files
	tpath,tfile = _CatFitacfFiles(filesp,files)
	
	#read it in 
	sc,ar = _ReadFitacf(tfile)
	
	#delete the temporary fitacf
	_DelFitacfTemp(tpath,tfile)


	return sc,ar
