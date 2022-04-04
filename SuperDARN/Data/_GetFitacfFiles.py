import numpy as np
from ..Tools.FileSearch import FileSearch
from .. import Globals
import DateTimeTools as TT

def _GetFitacfFiles(Radar,Date,ut):
	
	'''
	Scans the fitacf path for files which fit within the requested
	time/date range.
	
	This should work with file names with the format:
	$FITACF_PATH/stn/yyyy/yyyymmhh.hhmm.00.stn.fitacf.bz2
	where 
		stn : 3-letter radar code (lower case)
		yyyy : year folder
		yyyymmdd : Date
		hhmm : time (hours and minutes) 
	e.g.
	$FITACF_PATH/han/2002/20020321.2001.00.han.fitacf.bz2
	
	Our files are stored in two hour blocks, other configs may do 
	strange things - so file a bug report!
	
	Inputs
	======
	Radar : str
		Radar code
	Date : int
		Date in format yyyymmdd (can be one or two elements)
	ut : float
		UT range in hours since the start of the day (2 elements)
		
	Returns
	=======
	filesp : str
		Array of files including their paths
	files : str
		Array of file names without their paths.
	
	'''
	
	#get the base path for the radar
	RadarPath = Globals.FitACFPath + '{:s}/'.format(Radar.lower())
	
	#get a list of dates
	if np.size(Date) == 2:
		dates = TT.ListDates(Date[0],Date[1])
	else:
		dates = np.array([Date]).flatten()
		
	#work out the years
	years = dates//10000
	uyears = np.unique(years)
	nuy = uyears.size
	
	#get the list of files which correspond to those dates
	files = np.array([],dtype='object')
	filesp = np.array([],dtype='object')
	#loop through each unique year folder
	for i in range(0,nuy):
		path = RadarPath + '{:04d}/'.format(uyears[i])
		use = np.where(years == uyears[i])[0]
		nu = use.size
		#then each date which should be in that folder
		for j in range(0,nu):
			f = FileSearch(path,'{:08d}*.fitacf.bz2'.format(dates[use[j]]))
			if f.size > 0:
				#if we find matches, then add them!
				fp = [path+k for k in f]
				files = np.append(files,f)
				filesp = np.append(filesp,fp)	
	
	if files.size == 0:
		return filesp,files
	
	#sort by their name
	srt = np.argsort(files)
	files = files[srt]
	filesp = filesp[srt]


	#get the dates and times for each file
	fDate = np.array([np.int32(s[0:8]) for s in files])
	fhhmm = np.array([np.int32(s[9:13]) for s in files])
	hh = fhhmm/100
	mm = fhhmm//100
	fut = hh + mm/60.0
	
	#limit to the files within ut range
	futc = TT.ContUT(fDate,fut)
	utc0 = TT.ContUT(dates[0],ut[0])[0]
	utc1 = TT.ContUT(dates[-1],ut[1])[0]
	use = np.where((futc >= utc0-2.0) & (futc <= utc1))[0]

	files = files[use]
	filesp = filesp[use]
	
	return filesp,files
