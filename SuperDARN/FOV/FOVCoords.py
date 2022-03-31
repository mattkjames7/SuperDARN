import numpy as np
from ._SlantRange import _SlantRange,_SlantRangeGS
from ._GroundRange import _GroundRange
from ._VirtualHeight import _VirtualHeight
from ._RangeCoords import _RangeCoords

def FOVCoords(rlon,rlat,Boresight,nBeams,nGates,Beamsep,frang=180.0,
				rsep=45.0,rxrise=0.0,Altitude=400.0,Model='chisham08'):
	'''
	Calculate the positions of the FOV in geographic coordinates. This
	routine will work out coordinatesfor the centre and the four corners
	of each cell.
	
	Inputs
	======
	rlon : float
		radar longitude (deg)
	rlat : float
		radar latitude (deg)
	Boresight : float
		boresight of the beam (deg) - angle is positive clockwise of
		north		
	nBeams : int
		Number of beams
	nGates : int
		Number of range gates
	Beamsep : float
		Separation between beams (deg)
	frang : float
		Distance to first range (km)
	rsep : float
		Range separation
	rxrise : float
		Rx rise time (us)
	Altitude : float
		Altitude for old virtual height model
	Model : str
		Virtual height model: 'chisham08'|'old'
		
	Returns
	=======
	glon : float
		Longitudes at the corners of each cell (nBeams+1,nGates+1)
	glat : float
		Latitudes at the corners of each cell (nBeams+1,nGates+1)
	glonc : float
		Longitudes at the centres of each cell (nBeams,nGates)
	glatc : float
		Latitudes at the centres of each cell (nBeams,nGates)
	gsglon : float
		Longitudes at the corners of each cell (nBeams+1,nGates+1)
		for ground scatter.
	gsglat : float
		Latitudes at the corners of each cell (nBeams+1,nGates+1)
		for ground scatter.
	gsglonc : float
		Longitudes at the centres of each cell (nBeams,nGates)
		for ground scatter.
	gsglatc : float
		Latitudes at the centres of each cell (nBeams,nGates)
		for ground scatter.
	
	'''

	#create the output arrays
	# beam edges
	glon = np.zeros((nBeams+1,nGates+1),dtype='float64')
	glat = np.zeros((nBeams+1,nGates+1),dtype='float64')
	#beam centers
	glonc = np.zeros((nBeams,nGates),dtype='float64')
	glatc = np.zeros((nBeams,nGates),dtype='float64')
	# beam edges (ground scatter)
	gsglon = np.zeros((nBeams+1,nGates+1),dtype='float64')
	gsglat = np.zeros((nBeams+1,nGates+1),dtype='float64')
	#beam centers (ground scatter)
	gsglonc = np.zeros((nBeams,nGates),dtype='float64')
	gsglatc = np.zeros((nBeams,nGates),dtype='float64')
	
	#calculate the slant ranges
	sr,src = _SlantRange(frang,rsep,rxrise,nGates)
	
	#and the ground scatter equivalent
	gssr = _SlantRangeGS(sr,Altitude)
	gssrc = _SlantRangeGS(src,Altitude)
	
	#calculate virtual height
	hv = _VirtualHeight(sr,Model=Model,Altitude=Altitude)
	hvc = _VirtualHeight(src,Model=Model,Altitude=Altitude)
	gshv = _VirtualHeight(gssr,Model=Model,Altitude=Altitude)
	gshvc = _VirtualHeight(gssrc,Model=Model,Altitude=Altitude)

	#ground range angles
	_,rang = _GroundRange(sr,hv)
	_,rangc = _GroundRange(src,hvc)
	_,gsrang = _GroundRange(gssr,gshv)
	_,gsrangc = _GroundRange(gssrc,gshvc)
	
	#calculate the boresights for each beam
	bmbs = (np.arange(nBeams+1) - nBeams/2)*Beamsep + Boresight
	bmbsc = (np.arange(nBeams) - (nBeams-1)/2)*Beamsep + Boresight
	
	#now calculate the coordinates
	for i in range(0,nBeams):
		glon[i],glat[i] = _RangeCoords(rlon,rlat,rang,bmbs[i])
		glonc[i],glatc[i] = _RangeCoords(rlon,rlat,rangc,bmbsc[i])
		gsglon[i],gsglat[i] = _RangeCoords(rlon,rlat,gsrang,bmbs[i])
		gsglonc[i],gsglatc[i] = _RangeCoords(rlon,rlat,gsrangc,bmbsc[i])
	glon[nBeams],glat[nBeams] = _RangeCoords(rlon,rlat,rang,bmbs[nBeams])
	gsglon[nBeams],gsglat[nBeams] = _RangeCoords(rlon,rlat,gsrang,bmbs[nBeams])

	return glon,glat,glonc,glatc,gsglon,gsglat,gsglonc,gsglatc
