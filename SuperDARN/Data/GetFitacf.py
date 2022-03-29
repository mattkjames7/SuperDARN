import numpy as np
from .. import Globals
from ._ReadFitacfFiles import _ReadFitacfFiles

def GetFitacf(Radar,Date,ut=[0.0,24.0],Reload=False):
	'''
	Retrieve the FitACF data for a specific radar and time range. Data
	are stored in memory once loaded, and multiple calls with the same
	parameters should result in the files being read once, then data
	being returned from memory afterwards (unless the Reload keyword is
	set to True).
	
	Inputs
	======
	Radar : str
		3-letter radar code.
	Date : int
		Either a single date in the format yyyymmdd, or a 2-element
		list/tuple/array date range.
	ut : float
		UT range covered in hours from the start of the day. If a single 
		date is used then the data will cover the range: 
			Date ut[0] to Date ut[1]
		if a range of dates is provided:
			Date[0] ut[0] to Date[1] ut[1]
	Reload : bool
		If True, then the routine will be forced to re-read the fitacf 
		files.
		
	Returns
	=======
	sc : numpy.recarray
		Record array containing the scalars for each fitacf record
	ar : numpy.recarray
		Arrays from each record combined (this is the actual data).
	
	'''	
	
	
	#get the key
	ut0 = np.int32(2.0*np.floor(ut[0]/2.0))
	ut1 = np.int32(2.0*np.ceil(ut[1]/2.0))	
	if np.size(Date) == 1:
		key = Radar.lower()+'-{:08d}T{:02d}-{:08d}T{:02d}'.format(Date,ut0,Date,ut1)
	else:
		key = Radar.lower()+'-{:08d}T{:02d}-{:08d}T{:02d}'.format(Date[0],ut0,Date[1],ut1)
	
	#read data in if it doesn't alread exist in memory
	if (key in Globals.Data) == False or Reload:
		Globals.Data[key] = _ReadFitacfFiles(Radar,Date,ut)

	return Globals.Data[key]
