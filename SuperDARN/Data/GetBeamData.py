import numpy as np
from .GetFitacf import GetFitacf
import DateTimeTools as TT
from ._GetDataDtype import _GetBeamDtype

def GetBeamData(Radar,Date,ut,Beam):
	'''
	Get the data from a single beam of radar data
	
	Inputs
	======
	Radar : str
		Radar code
	Date : int
		Date in format yyyymmdd (can be a 2-element range)
	ut : float
		UT range in hours since the start of the day.
	Beam : int
		Beam number.
	
	Returns
	=======
	out : numpy.recarray
		Data
	
	'''
	
	#get the data first
	sc,data = GetFitacf(Radar,Date,ut=ut)
	
	#select this beam
	use = np.where(data.Beam == Beam)[0]
	uses = np.where(sc.Beam == Beam)[0]
	
	if use.size == 0:
		return None
		
	data = data[use]
	sc = sc[uses]
	
	#limit time
	utc = TT.ContUT(data.Date,data.ut)
	utcs = TT.ContUT(sc.Date,sc.ut)
	if np.size(Date) == 1:
		utcr = TT.ContUT(np.array([Date,Date]),ut)
	else:
		utcr = TT.ContUT(Date,ut)
	use = np.where((utc >= utcr[0]) & (utc <= utcr[1]))[0]
	uses = np.where((utcs >= utcr[0]) & (utcs <= utcr[1]))[0]

	if use.size == 0:
		return None
	
	data = data[use]
	sc = sc[uses]
	
	#work out indices
	ind = np.zeros(data.size,dtype='int32')
	I = data.Index[0]
	p = 0
	print(sc.size,np.unique(data.Index).size)
	for i in range(0,data.size):
		if I != data.Index[i]:
			p += 1
			I = data.Index[i]
		
		ind[i] = p
	
	#find the number of gates
	nG = np.max(data.nGates)
	
	#get output dtype
	dtype = _GetBeamDtype(nG)
	
	#output array
	out = np.recarray(sc.size,dtype=dtype)
	out.Date = sc.Date
	out.ut = sc.ut
	out.Beam = Beam
	out.ScanCode = sc.ScanCode
	out.smsep = sc.smsep
	out.lagfr = sc.lagfr
	out.rsep = sc.rsep
	out.frang = sc.frang
	out.V.fill(np.nan)
	out.W_l.fill(np.nan)
	out.P_l.fill(np.nan)
	out.Gnd.fill(np.nan)
	out.V[ind,data.Gate] = data.V
	out.P_l[ind,data.Gate] = data.P_l
	out.W_l[ind,data.Gate] = data.W_l
	out.Gnd[ind,data.Gate] = data.Gnd

		
	return out
