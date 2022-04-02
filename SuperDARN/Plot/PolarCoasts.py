import numpy as np
from ..Tools.ReadCoasts import ReadCoasts

import aacgmv2
import DateTimeTools as TT
from ..Tools.Today import Today
from ..Tools.Now import Now

def PolarCoasts(ax,Date=None,ut=None,Mag=True,Lon=False,Hemisphere='North',
				Fill=None,zorder=-1,Method='aacgm',color='black'):	
	'''
	Plot the coastlines on a polar plot.
	
	Inputs
	======
	ax : pyplot.Axes
		Subplot axes to plot onto
	Date : int
		Date in the format yyyymmdd for use in orienting the plot and for
		the magnetic conversion. If none are provided, then the current
		day is used.
	ut : float
		Time in hours since the beginning of the day
	Mag : bool
		If True, plots will be in magnetic coords rather than geographic
	Lon : bool
		If True then the plot will be oriented such that the azimuthal 
		axis is the longitude rather than the local time.
	Hemisphere : str
		'north'|'south'
	Fill : None|float
		If not None, set to a 3 or 4 element array to fill the land a 
		certain colour.
	zorder : float
		plotting order
	Method : str
		'igrf'|'aacgm'
		
	'''
	
	#get date and time
	if Date is None:
		Date = Today()
	if ut is None:
		ut = Now()
	
	#read in the coastlines
	lons,lats = ReadCoasts()
	
	#convert to the appropriate coordinate system
	if Mag and Method == 'igrf':
		try:
			import PyGeopack as gp
		except:
			print('PyGeopack needed to use Method="igrf"')
			Method = 'aacgm'	
	
	if Mag:
		if Method == 'igrf':
			mlon,mlat = gp.Coords.GEOtoMAGLL(lons,lats,Date,ut)
			r = mlat
			if Lon == False:	
				mlt = gp.Coords.MLONtoMLT(mlon,Date,ut)
				t = mlt*15*np.pi/180.0
			else:
				t = mlon*np.pi/180.0
		else:
			DT = TT.Datetime(Date,ut)
			mlat,mlon,_ = aacgmv2.convert_latlon_arr(lats,lons,0.0,DT[0],method_code='G2A')
			r = mlat
			if Lon == False:	
				mlt = aacgmv2.convert_mlt(mlon,DT[0])
				t = mlt*15*np.pi/180.0
			else:
				t = mlon*np.pi/180.0
	else:
		r = lats
		if Lon:
			t = lons*np.pi/180.0
		else:
			t = (lons + 15*ut)*np.pi/180.0

	#reverse r if we are polotting the south
	if Hemisphere.lower() == 'south' or Hemisphere.lower() == 's':
		r = -r

		
	#coastlines are split into chunks
	zero = np.where((lats == 0) & (lons == 0))[0]
	nz = np.size(zero)
	zero = np.append(0,zero)
	for i in range(0,nz):
		ti = t[zero[i]+1:zero[i+1]-1]
		ri = r[zero[i]+1:zero[i+1]-1]
		
		ax.plot(ti,ri,color=color)

		if not Fill is None:
			ax.fill(ti,ri,color=Fill,zorder=zorder)
