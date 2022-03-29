import numpy as np
from ._GetDataDtype import _GetDataDtype

def _FormatFitacfData(Radar,sc,ar):
	'''
	Reformat the data into grids based on the number of gates, the 
	number of beams defined by the hardware and the lag settings.
	
	
	'''
	
	#get the number of beams
	ud = np.unique(ar.Date)
	nBeams = np.zeros(ar.size,dtype='int32')
	for i in range(0,ud.size):
		hw = GetRadarHW(Radar,ud[i])
		use = np.where(ar.Date == ud[i])[0]
		nBeams[use] = hw['nBeams']
	
	

	#find indices where number of gates or beams changes
	dnG = ar[1:].nGates != ar[:-1].nGates
	dnB = nBeams[1:] != nBeams[:-1]
	chg = dnG | dnB
	ind = np.where(chg)[0]
		
	if ind.size == 0:
		i0 = np.array([0])
		i1 = np.array([ar.size])
	else:
		i0 = np.append(0,ind)
		i1 = np.append(ind + 1,ar.size)


	#loop through each change
	out = []
	for i in range(0,i0.size):
		use = np.arange(i0[i],i1[i])
		tmp = ar[use]
		
		data = np.recarray(
		
