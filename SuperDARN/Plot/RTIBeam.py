import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from ..Tools.PlotGridLine import PlotGridLine
from ..Data.GetBeamData import GetBeamData
from ..FOV.GetFOV import GetFOV
from ..Tools.ColTab import ColTabbcyr,ColTabBinary
from scipy.stats import linregress,mode
import DateTimeTools as TT



def RTIBeam(Radar,Date,ut,Beam,GateRange,Param='V',fig=None,maps=[1,1,0,0],
		zlog=False,scale=None,cmap=None,Mag=True,yaxistype='cell',
		nobar=False,ZeroMean=False,Detrend=False,MaxVal=1500.0,ShowScatter=False):

	#get list of cells
	nCells = GateRange[1] - GateRange[0] + 1
	Gates = np.arange(nCells,dtype='int32') + GateRange[0]
	Beams = np.zeros(nCells,dtype='int32') + Beam

	#get coordinates of each cell
	date0 = np.array([Date]).flatten()[0]
	fov = GetFOV(Radar,date0)
	lon,lat = fov.CellCoords(Beams,Gates,Date=date0,ut=ut[0],Mag=Mag)

	#get the ylabels/grid coords
	if yaxistype.lower() in ['lon','longitude','maglon','mlon']:
		srt = np.argsort(lon)
		ylabel = 'Longitude ($^{o}$)'
		yaxismid = lon
		if Mag:
			ylabel = 'Magnetic '+ylabel
		
	elif yaxistype.lower() in ['lat','latitude','maglat','mlat']:
		srt = np.argsort(lat)
		yaxismid = lat
		ylabel = 'Latitude ($^{o}$)'
		if Mag:
			ylabel = 'Magnetic '+ylabel
	else:
		yaxismid = np.arange(Beams.size)+0.5 + Gates[0]
		srt = np.arange(Beams.size)
		ylabel = 'Range Cell'

	lon = lon[srt]
	lat = lat[srt]
	Beams = Beams[srt]
	Gates = Gates[srt]	
	yaxismid = yaxismid[srt]
		
	
	d = 0.5*(yaxismid[1:] - yaxismid[:-1])
	yaxis = np.append(yaxismid[0]-d[0],yaxismid[:-1]+d)
	yaxis = np.append(yaxis,yaxismid[-1]+d[-1])	

	Trange = None

	#get the scale
	if scale is None:
		if Param == 'V' or Param == 'W_l':
			scale = [-300,300]
		elif Param == 'P_l':
			scale = [-10,10]
		elif Param == 'Gnd':
			scale = [0,1]

	#get the data
	data = GetBeamData(Radar,Date,ut,Beam)
	
	#time axis
	t = TT.ContUT(data.Date,data.ut)
	dt = t[1:] - t[:-1]
	dt = mode(dt)[0][0]
	t = np.append(t,t[-1] + dt)

	#set norm
	if zlog:
		norm = colors.LogNorm(vmin=scale[0],vmax=scale[1])
	else:
		norm = colors.Normalize(vmin=scale[0],vmax=scale[1])	
	
	#also groundscatter
	gscmap = ColTabBinary([0.0,0.0,0.0,0.0],[0.5,0.5,0.5,1.0])
	gsnorm = colors.Normalize(vmin=0.0,vmax=1.0)

	if cmap is None:
		cmap = ColTabbcyr()
		
	if fig is None:
		fig = plt
		fig.figure()
	if hasattr(fig,'Axes'):	
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
	else:
		ax = fig
		
	for i in range(0,nCells):
		
		#select the appropriate parameter
		P = data[Param][:,Gates[i]]
		
		#ground scatter
		G = data['Gnd'][:,Gates[i]].astype('float64')
		G[G <= 0] = np.nan

		if Param != 'Gnd' and ShowScatter == False:
			gs = np.where((G > 0) & np.isfinite(G))[0]
			P[gs] = np.nan

		if not Param == 'Gnd':
			#remove huge values
			if not MaxVal is None:
				bad = np.where(P > MaxVal)[0]
				if bad.size > 0:
					P[bad] = np.nan
					
			#remove trend or zero mean
			if Detrend:
				gd = np.where(np.isfinite(P))[0]
				if gd.size > 0:
					m,c,_,_,_ = linregress(t[gd],P[gd])
					P[gd] -= t[gd]*m + c			
			elif ZeroMean:
				mu = np.nanmean(P)
				P = P - mu
			
		#plot the data
		PlotGridLine(ax,P,t,yaxis[i:i+2],norm,cmap)
		
		#plot scatter
		if not ShowScatter and not Param == 'Gnd':
			PlotGridLine(ax,G,t,yaxis[i:i+2],gsnorm,gscmap)
		
	if Param == 'V':
		ztitle = 'Line of Sight Velocity (m s$^{-1}$)'
	elif Param == 'P_l':
		ztitle = 'Power (dB)'
	elif Param == 'W_l':
		ztitle = 'Width (m s$^{-1}$)'
	elif Param == 'Gnd':
		ztitle = 'Ground Scatter Flag'		


	ax.set_ylabel(ylabel)
	TT.DTPlotLabel(ax)

	if not nobar:
		sm = plt.cm.ScalarMappable(cmap=cmap,norm=plt.Normalize(vmin=scale[0],vmax=scale[1]))
		sm._A = []
		cbar=fig.colorbar(sm)
		cbar.set_label(ztitle)		

	
	return ax
