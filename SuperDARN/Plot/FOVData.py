import numpy as np
from ..FOV.GetFOV import GetFOV
from ..Data.GetRadarData import GetRadarData
from ..Hardware.GetRadarHW import GetRadarHW
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from ..Tools.ColTab import ColTabbcyr,ColTabBinary
from ..Tools.ConvertGeoCart import ConvertGeoCart

def FOVData(Radar,Date,ut,Param='V',fig=None,maps=[1,1,0,0],
		zlog=False,scale=None,cmap=None,Mag=True,GS=False,
		nobar=False,MaxVal=1500.0,ShowScatter=False,
		Background=None,Continents=None,Coasts='black',
		Lon=False,Method='aacgm',color='black'):


	#get the FOV
	date0 = np.array([Date]).flatten()[0]
	ut0 = np.array([ut]).flatten()[0]
	fov = GetFOV(Radar,Date=date0)
	
	#get the data
	data = GetRadarData(Radar,Date,ut)
	
	#and the hardware
	hw = GetRadarHW(Radar,Date=date0)
	
	#create a grid for the data
	grid = np.zeros((hw.nBeams,hw.nGates),dtype='float64') + np.nan
	gridgs = np.zeros((hw.nBeams,hw.nGates),dtype='float64') + np.nan
	for i in range(0,hw.nBeams):
		# try:
			# #get the data parameter to be plotted and ground scatter
			# P = data[i][Param][0]
			# G = data[i]['Gnd'][0].astype('float64')
			# G[G <= 0] = np.nan
			
			# #remove ground scatter data
			# if Param != 'Gnd' and ShowScatter == False:
				# gs = np.where((G > 0) & np.isfinite(G))[0]
				# P[gs] = np.nan			

			# if not Param == 'Gnd':
				# #remove huge values
				# if not MaxVal is None:
					# bad = np.where(P > MaxVal)[0]
					# if bad.size > 0:
						# P[bad] = np.nan		
			# #add to the grids
			# grid[i]	= P
			# gridgs[i] = G
			
		#except:
		#	grid[i,:] = np.nan
		#	gridgs[i,:] = np.nan

		#get the data parameter to be plotted and ground scatter
		P = data[i][Param][0]
		G = data[i]['Gnd'][0].astype('float64')
		G[G <= 0] = np.nan
		
		#remove ground scatter data
		if Param != 'Gnd' and ShowScatter == False:
			gs = np.where((G > 0) & np.isfinite(G))[0]
			P[gs] = np.nan			

		if not Param == 'Gnd':
			#remove huge values
			if not MaxVal is None:
				bad = np.where(P > MaxVal)[0]
				if bad.size > 0:
					P[bad] = np.nan		
		#add to the grids
		grid[i,:P.size]	= P
		gridgs[i,:G.size] = G

	#get the scale
	if scale is None:
		if Param == 'V' or Param == 'W_l':
			scale = [-300,300]
		elif Param == 'P_l':
			scale = [-10,10]
		elif Param == 'Gnd':
			scale = [0,1]


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
	elif isinstance(cmap,str):
		cmap = plt.cm.get_cmap(cmap)
	
	#find the finite cells
	beams,gates = np.where(np.isfinite(grid))
	beamsgs,gatesgs = np.where(np.isfinite(gridgs))
	nCells = beams.size
	nCellsgs = beamsgs.size
	
	#get the lons/lats of the cells (edges)
	glon,glat = fov.CellCorners(beams,gates,Date=date0,Mag=False,GS=GS)
	glongs,glatgs = fov.CellCorners(beamsgs,gatesgs,Date=date0,Mag=False,GS=GS)
	
	#create the plot with coasts etc
	ax = fov.PlotPolar(	ShowBeams=False,ShowCells=False,color=color,Mag=Mag,GS=GS,fig=fig,maps=maps,
						Background=Background,Continents=Continents,Coasts=Coasts,
						Lon=Lon,Method=Method,Cart=True,Date=date0,ut=ut0)
						
	#work out the hemisphere to plot
	if fov.fov['glatc'][0][0] > 0:
		hem = 'north'
	else:
		hem = 'south'
	
	#now to loop through each cell
	for i in range(0,nCells):
		#get the plotting color
		col = cmap(norm(grid[beams[i],gates[i]]))
		
		#now the coordinates to fill
		x,y = ConvertGeoCart(glon[i],glat[i],Date=date0,ut=ut0,Mag=Mag,Lon=Lon,Method=Method,Hemisphere=hem)

		#fill it in 
		ax.fill(x,y,color=col)	
	
	#same for the ground scatter	
	if not ShowScatter and not Param == 'Gnd':
		for i in range(0,nCellsgs):
			#get the plotting color
			col = gscmap(gsnorm(gridgs[beamsgs[i],gatesgs[i]]))
			
			#now the coordinates to fill
			x,y = ConvertGeoCart(glongs[i],glatgs[i],Date=date0,ut=ut0,Mag=Mag,Lon=Lon,Method=Method,Hemisphere=hem)

			#fill it in 
			ax.fill(x,y,color=col)
		
	
	if Param == 'V':
		ztitle = 'Line of Sight Velocity (m s$^{-1}$)'
	elif Param == 'P_l':
		ztitle = 'Power (dB)'
	elif Param == 'W_l':
		ztitle = 'Width (m s$^{-1}$)'
	elif Param == 'Gnd':
		ztitle = 'Ground Scatter Flag'		


	if not nobar:
		sm = plt.cm.ScalarMappable(cmap=cmap,norm=norm)
		sm._A = []
		cbar = plt.colorbar(sm)
		cbar.set_label(ztitle)		
		
	return ax
