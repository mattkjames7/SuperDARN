import numpy as np
import aacgmv2
import DateTimeTools as TT

def _MagFOV(glon,glat,Date):
	'''
	Calculate the magnetic coordinates of the FOV for a given date.
	
	'''
	#get datetime
	dt = TT.Datetime(Date,0.0)
	
	#alt = 0.0
	alt = np.zeros(glon.size,dtype='float32')
	lon = glon.flatten()
	lat = glat.flatten()
	s = glon.shape
	
	mlat,mlon,_ = aacgmv2.convert_latlon_arr(lat,lon,alt,dt,method='G2A')
	
	return mlon.reshape(s),mlat.reshape(s)
	
