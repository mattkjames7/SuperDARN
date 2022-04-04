import numpy as np
import aacgmv2
import DateTimeTools as TT

def _MagFOV(glon,glat,Date):
	'''
	Calculate the magnetic coordinates of the FOV for a given date.
	
	Inputs
	======
	glon : float
		Geographic longitudes (degrees)
	glat : float
		Geographic latitudes (degrees)
	
	Returns
	=======
	mlon : float
		Magnetic longitudes (degrees)
	mlat : float
		Magnetic latitudes (degrees)
		
	
	'''
	#get datetime
	dt = TT.Datetime(Date,0.0)[0]
	
	#alt = 0.0
	alt = np.zeros(glon.size,dtype='float32')
	lon = glon.flatten()
	lat = glat.flatten()
	s = glon.shape
	
	mlat,mlon,_ = aacgmv2.convert_latlon_arr(lat,lon,alt,dt,method_code='G2A')
	
	return mlon.reshape(s),mlat.reshape(s)
	
