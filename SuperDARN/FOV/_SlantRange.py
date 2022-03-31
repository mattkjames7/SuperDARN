import numpy as np


def _SlantRange(frang,rsep,rxrise,nGates):
	'''
	Calculate the slant range
	
	Inputs
	======
	frang : float
		Distance to the first range (km)
	rsep : float
		Distance between ranges (km)
	rxrise : float
		Receiver rise time (us)
	nGates : int
		Number of range gates
	
	Returns
	=======
	srange : float
		Array of slant ranges for the edges of each gate
	srangec : float
		Array of slant ranges for the centres of each gate
	
	'''
	
	#factor to convert between lags in ms and distance in km
	#calculated using the speed of light, the factor of 2 is
	#because the radio waves must travel to and from the irregularity
	C = 2.0/0.3
	
	#get gates
	gates = np.arange(nGates + 1)
	gatec = np.arange(nGates) + 0.5
		
	#convert rxrise to dist
	rxdist = rxrise/C
	
	#calculate first gate dist
	fr = frang - rxdist
	
	#now both outputs
	srange = fr + rsep*gates
	srangec = fr + rsep*gatec
	
	return srange,srangec
	
def _SlantRangeGS(srange,altitude=300.0):
	'''
	Use equation defined by Bristow et al 1994 to work out the 
	approximate distance of the reflection point in the ionosphere
	for groundscatter.
	
	Inputs
	======
	srange : float
		Array of slant ranges in km.
	altitude : float
		Reflection altitude (km).
	
	Returns
	=======
	gsrange : float
		reflection range for ground scatter in km.
	
	'''
	Re = 6371.0
	
	gsrange = Re*np.arcsin(np.sqrt((srange**2/4.0) - altitude**2)/Re)
	
	return gsrange
