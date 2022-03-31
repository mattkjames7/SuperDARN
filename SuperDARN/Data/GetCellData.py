import numpy as np
from .GetFitacf import GetFitacf
import DateTimeTools as TT
from .. import Globals

def GetCellData(Radar,Date,ut,Beam,Gate):
	'''
	Get the data from a single cell of radar data
	
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
	Gate : int
		Gate number
	
	Returns
	=======
	out : numpy.recarray
		Data
	
	'''
	
	#get the data first
	sc,data = GetFitacf(Radar,Date,ut=ut)
	scind = np.arange(sc.size)
	
	#select this beam
	use = np.where((data.Beam == Beam) & (data.Gate == Gate))[0]
	uses = np.where((sc.Beam == Beam))[0]
	
	if use.size == 0:
		return None
		
	data = data[use]
	sc = sc[uses]
	scind = scind[uses]
	
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
	scind = scind[uses]

	#work out indices
	ind = np.zeros(data.size,dtype='int32')
	I = data.Index[0]
	p = 0
	for i in range(0,data.size):
		#I could do with replacing this with something faster
		ind[i] = np.where(scind == data.Index[i])[0][0]
			
	#output array
	out = np.recarray(sc.size,dtype=Globals.adtype)
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
	out.V[ind] = data.V
	out.P_l[ind] = data.P_l
	out.W_l[ind] = data.W_l
	out.Gnd[ind] = data.Gnd
	out.Index = scind
		
	return out
