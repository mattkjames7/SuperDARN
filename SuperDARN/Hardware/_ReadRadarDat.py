import numpy as np
from .. import Globals
import PyFileIO as pf

def _ReadRadarDat():
	'''
	This function will attempt to read the information from radar.dat
	
	Returns
	=======
	out : numpy.recarray
		Radar information
	
	'''
	
	#the name of the file to read
	fname = Globals.HardwarePath + 'radar.dat'
	
	#get data
	lines = pf.ReadASCIIFile(fname)
	
	#work out where the data starts
	splits = [3,5,14,23,50,88,102,108]
	data = []
	for l in lines:		
		if l[0] != '#' and len(l) > 100:
			ls = l.replace('"',' ').replace('\n',' ')
			tmp = []
			p = 0
			for s in splits:
				tmp.append(ls[p:s])
				p = s
			data.append(tmp)
				
	#get the number of radars and the output array
	nr = len(data)
	dtype = [	('ID','int16'),
				('Status','int8'),
				('StartDate','int32'),
				('EndDate','int32'),
				('Name','object'),
				('Operator','object'),
				('HDW','object'),
				('Code','U3')]
	
	out = np.recarray(nr,dtype=dtype)
	
	#fill it up
	for i in range(0,nr):
		out[i].ID = np.int16(data[i][0])
		out[i].Status = np.int8(data[i][1])
		out[i].StartDate = np.int32(data[i][2])
		out[i].EndDate = np.int32(data[i][3])
		out[i].Name = data[i][4].strip()
		out[i].Operator = data[i][5].strip()
		out[i].HDW = data[i][6].strip()
		out[i].Code = data[i][7].strip()
	
	return out
