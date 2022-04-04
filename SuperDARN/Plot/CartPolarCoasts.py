import numpy as np
from ..Tools.ReadCoasts import ReadCoasts
from ..Tools.ConvertGeoCart import ConvertGeoCart
import aacgmv2
import DateTimeTools as TT
from ..Tools.Today import Today
from ..Tools.Now import Now

def CartPolarCoasts(ax,Date=None,ut=None,Mag=True,Lon=False,Hemisphere='North',
				Fill=None,zorder=-1,Method='aacgm',color='black'):	
	'''
	Plot the coastlines on a polar plot which uses Cartesian coords
	(Plot.CartPolarAxis).
	
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
	x,y = ConvertGeoCart(lons,lats,Date=Date,ut=ut,Mag=Mag,Lon=Lon,Method=Method,Hemisphere=Hemisphere)

	
	#coastlines are split into chunks
	zero = np.where((lats == 0) & (lons == 0))[0]
	nz = np.size(zero)
	zero = np.append(0,zero)
	if Hemisphere == 'south':
		lats = -lats
	
	for i in range(0,nz):
		xi = x[zero[i]+1:zero[i+1]-1]
		yi = y[zero[i]+1:zero[i+1]-1]
		li = lats[zero[i]+1:zero[i+1]-1]
		
		if (li > 0.0).any():
			ax.plot(xi,yi,color=color)

			if not Fill is None:
				ax.fill(xi,yi,color=Fill,zorder=zorder)
