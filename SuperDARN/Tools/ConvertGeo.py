import numpy as np
import aacgmv2
import DateTimeTools as TT
from ..Tools.Today import Today
from ..Tools.Now import Now

def ConvertGeo(lon,lat,Date=None,ut=None,Mag=False,Lon=False,Method='aacgm'):
	'''
	Converts geographic longitudes and latitudes to whatever coordinates
	are required for the polar axis plot.
	
	Inputs
	======
	lon : float
		longitude(s) in degrees
	lat : float
		latitude(s) in degrees
	Date : int
		Date in format yyyymmdd
	ut : float
		UT in hours since the start of the day
	Mag : bool
		If True, magnet coordinates are returned
	Lon : 
		If True, azimuthal coordinate is longitude, if False then it is
		local time.
	Method : str
		'aacgm'|'igrf'
		
	Returns
	=======
	t : float
		azimuthal plotting coordinate (rad)
	r : float
		radial plotting coordinate (degrees)
		
	Yes - I know that it a horrible mix of units.
	
	'''
	#check of the array can be flattened
	flt = hasattr(lon,'flatten')
	if flt:
		sh = lon.shape
		lon = lon.flatten()
		lat = lat.flatten()

	#get date and time
	if Date is None:
		Date = Today()
	if ut is None:
		ut = Now()			
	
	
	#convert to the appropriate coordinate system
	if Mag and Method == 'igrf':
		try:
			import PyGeopack as gp
		except:
			print('PyGeopack needed to use Method="igrf"')
			Method = 'aacgm'	
		
	if Mag:
		if Method == 'igrf':
			mlon,mlat = gp.Coords.GEOtoMAGLL(lon.flatten(),lat.flatten(),Date,ut)
			r = mlat
			if Lon == False:	
				mlt = gp.Coords.MLONtoMLT(mlon,Date,ut)
				t = mlt*15*np.pi/180.0
			else:
				t = mlon*np.pi/180.0
			r = r.reshape(lat.shape)
			t = t.reshape(lat.shape)
		else:
			DT = TT.Datetime(Date,ut)
			mlat,mlon,_ = aacgmv2.convert_latlon_arr(lat.flatten(),lon.flatten(),0.0,DT[0],method_code='G2A')
			r = mlat
			if Lon == False:	
				mlt = aacgmv2.convert_mlt(mlon,DT[0])
				t = mlt*15*np.pi/180.0
			else:
				t = mlon*np.pi/180.0
			r = r.reshape(lat.shape)
			t = t.reshape(lat.shape)
	else:
		r = lat
		if Lon:
			t = lon*np.pi/180.0
		else:
			t = (lon + 15*ut)*np.pi/180.0	
			
	#reshape
	if flt:
		t = t.reshape(sh)
		r = r.reshape(sh)

	return t,r
