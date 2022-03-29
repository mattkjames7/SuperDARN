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
	_,data = GetFitacf(Radar,Date,ut=ut)
	
	#select this beam
	use = np.where(data.Beam == Beam)[0]
	
	if use.size == 0:
		return None
		
	data = data[use]
	
	#limit time
	utc = TT.ContUT(data.Date,data.ut)
	if np.size(Date) == 1:
		utcr = TT.ContUT(np.array([Date,Date]),ut)
	else:
		utcr = TT.ContUT(Date,ut)
	use = np.where((utc >= utcr[0]) & (utc <= utcr[1]))[0]
	if use.size == 0:
		return None
	
	data = data[use]
	utc = utc[use]
	
	#find the number of gates
	nG = np.max(data.nGates)
	
	#get output dtype
	dtype = _GetBeamDtype(nG)
	
	#output array
	uutc,ui = np.unique(utc,return_index=True)
	nu = uutc.size
	out = np.recarray(nu,dtype=dtype)
	out.Date,out.ut = TT.ContUTtoDate(uutc)
	out.Beam = Beam
	out.ScanCode = data.ScanCode[ui]
	out.smsep = data.smsep[ui]
	out.lagfr = data.lagfr[ui]
	out.V.fill(np.nan)
	out.W_l.fill(np.nan)
	out.P_l.fill(np.nan)
	out.Gnd.fill(np.nan)
	for i in range(0,nu):
		use = np.where(utc == uutc[i])[0]
		tmp = data[use]
		out.V[i][tmp.Gate] = tmp.V
		out.P_l[i][tmp.Gate] = tmp.P_l
		out.W_l[i][tmp.Gate] = tmp.W_l
		out.Gnd[i][tmp.Gate] = tmp.Gnd
		
	return out
