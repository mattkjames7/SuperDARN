import numpy as np
from .. import Globals
import PyFileIO as pf
import DateTimeTools as TT

def _ReadHDW(fname):
	'''
	Read a single radar hdw file
	
	Inputs
	======
	fname : str
		File name
	
	Returns
	=======
	out : numpy.recarray
		Hardware information
	
	'''
	
	
	#read the file in
	lines = pf.ReadASCIIFile(fname)
	
	#count how many lines there are 
	data = []
	for l in lines:
		if l[0] != '#':
			s = l.split()
			if len(s) > 8:
				data.append(s)
	n = len(data)
	
	#create output
	out = np.recarray(n,dtype=Globals.hwdtype)
	
	#fill it
	fields = [	'id','EndYear','EndSec','Glat','Glon','Alt','Boresight',
				'BeamSep','Vsign','RxStep','Tdiff','PhaseSign',
				'IFOffsetx','IFOffsety','IFOffsetz','RxRiseT',
				'AttenStage','nGates','nBeams']
	nf = len(fields)
	for i in range(0,n):
		nd = np.min([len(data[0]),nf])
		for j in range(0,nd):
			if data[i][j][0] == '+':
				d = data[i][j].strip('=')
			else:
				d = data[i][j]
			if 'int' in str(out[fields[j]].dtype) and '.' in d:
				d = d.split('.')[0]
			out[fields[j]][i] = np.array(d).astype(out[fields[j]].dtype)
	

	
	#calculate date/time
	doy = out.EndSec/86400
	out.EndDate = TT.DayNotoDate(out.EndYear,np.int32(doy))
	out.EndTime = (doy - np.int32(doy))*24.0
	
			
	return out
	
