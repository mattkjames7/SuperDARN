import numpy as np
from ..FOV.LatitudinalCellArray import LatitudinalCellArray
from .RTI import RTI

def RTILat(Radar,Date,ut,Lon,dLon=0.4,Mag=True,LatRange=None,Param='V',
			fig=None,maps=[1,1,0,0],zlog=False,scale=None,cmap=None,
			yaxistype='lat',nobar=False,ZeroMean=False,
			Detrend=False,MaxVal=1500.0,ShowScatter=False):
	
	#start by getting the cells we're interested in
	date0 = np.array([Date]).flatten()[0]
	Beams,Gates,_ = LatitudinalCellArray(Radar,Lon,dLon=dLon,
								Date=date0,Mag=Mag,LatRange=LatRange)

	#now call RTI function
	return RTI(Radar,Date,ut,Beams,Gates,Param=Param,fig=fig,maps=maps,
				zlog=zlog,scale=scale,cmap=cmap,Mag=Mag,yaxistype=yaxistype,
				nobar=nobar,ZeroMean=ZeroMean,Detrend=Detrend,MaxVal=MaxVal,
				ShowScatter=ShowScatter)
