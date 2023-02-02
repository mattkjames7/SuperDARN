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
	fields = [	'id','Status','StartDate','TimeStr','Glat','Glon','Alt','Boresight',
				'BSOffset','BeamSep','Vsign',
				'PhaseSign','TdiffA','TdiffB','IFOffsetx','IFOffsety','IFOffsetz',
				'RxRiseT','RxStep',
				'AttenStage','nGates','nBeams']
	nf = len(fields)
	for i in range(0,n):
		nd = np.min([len(data[0]),nf])
		for j in range(0,nd):
			
			if j == 3:
				s = data[i][j].split(':')
				d = np.int32(s)
				out.StartTime[i] = TT.HHMMtoDec(d[0],d[1],d[2])[0]
			elif fields[j] in out.dtype.names:
				if data[i][j][0] == '+':
					d = data[i][j].strip('+')
				else:
					d = data[i][j]
				if 'int' in str(out[fields[j]].dtype) and '.' in d:
					d = d.split('.')[0]
				out[fields[j]][i] = np.array(d).astype(out[fields[j]].dtype)
		

	
	#calculate date/time
	if n > 1:
		out.EndDate[:-1] = out.StartDate[1:]
		out.EndTime[:-1] = out.StartTime[1:]
	out.EndTime[-1] = 0.0
	out.EndDate[-1] = 21001231
	
			
	return out
	
