import numpy as np
from ..FOV.LongitudinalCellArray import LongitudinalCellArray
from .RTI import RTI

def RTILon(Radar,Date,ut,Lat,dLat=0.4,Mag=True,LonRange=None,Param='V',
			fig=None,maps=[1,1,0,0],zlog=False,scale=None,cmap=None,
			yaxistype='lon',nobar=False,ZeroMean=False,
			Detrend=False,MaxVal=1500.0,ShowScatter=False):
	'''
	Plot RTI (range time intensity) for a longitudinal array of range 
	cells at approximately the same latitude.
	
	Inputs
	======
	Radar : str
		Radar code
	Date : int
		Date in format yyyymmdd (can be a 2-element range)
	ut : float
		UT range in hours since the start of the day.
	Lat : float
		Desired latitude (degrees)
	dLat : float
		Acceptable latitude deviation of centre of the cell from Lat
		(degrees)
	Mag : bool
		If True (default) then magnetic coordinates are used, geographic
		otherwise.
	LonRange : float
		2 element array indicating the minimum and maximum longitudes
		to use.
	Param : str
		Which of the followinf parameters to plot
		'V' :velocity
		'P_l' : Power
		'W_l' : width
		'Gnd' : ground scatter
	fig : None|pyplot|pyplot.Axes
		If None: a new plot is created
		if an instance pf matplotlib.pyplot is provided, the current
		figure is used, with a new subplot
		if an instance of pyplot.Axes is provided, then the current 
		subplot is to be plotted upon.
	maps : int
		4-element array defining the subplot position 
		[xmaps,ymaps,xmap,ymap] where:
			xmaps - total number of subplots horizontally
			ymaps - total number of subplots vertically
			xmap - position from left (starting at 0)
			ymap - position from top (starting at 0)
	zlog : bool
		If True then the color scale will be logarithmic
	scale : float
		2-element array defining the color scale range
	cmap : None|str
		color map to use
	yaxistype : str
		'lon'|'lat'|'mlon'|'mlat'|'cell'
	nobar : bool
		If true, then no color bar will be plotted
	ZeroMean : bool
		If True, then themean is subtracted from each time series before
		plotting.
	Detrend : bool
		Linear detrending on data before plotting.
	MaxVal : float
		Maximum data value, above which will be assumed to be erroneous.
	ShowScatter : bool
		If True then ground scatter will appear in color instead of grey
		
	Returns
	=======
	ax : pyplot.Axes
		axes of a plot	
	
	'''	
	#start by getting the cells we're interested in
	date0 = np.array([Date]).flatten()[0]
	Beams,Gates,_ = LongitudinalCellArray(Radar,Lat,dLat=dLat,
								Date=date0,Mag=Mag,LonRange=LonRange)

	#now call RTI function
	return RTI(Radar,Date,ut,Beams,Gates,Param=Param,fig=fig,maps=maps,
				zlog=zlog,scale=scale,cmap=cmap,Mag=Mag,yaxistype=yaxistype,
				nobar=nobar,ZeroMean=ZeroMean,Detrend=Detrend,MaxVal=MaxVal,
				ShowScatter=ShowScatter)
