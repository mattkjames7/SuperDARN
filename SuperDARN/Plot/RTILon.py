import numpy as np
from ..FOV.LongitudinalCellArray import LongitudinalCellArray
from .RTI import RTI

def RTILon(Radar,Date,ut,Lat,dLat=0.4,Mag=True,LonRange=None,Param='V',
			fig=None,maps=[1,1,0,0],zlog=False,scale=None,cmap=None,
			yaxistype='lon',nobar=False,ZeroMean=False,
			Detrend=False,MaxVal=1500.0,ShowScatter=False):
	
	#start by getting the cells we're interested in
	date0 = np.array([Date]).flatten()[0]
	Beams,Gates,_ = LongitudinalCellArray(Radar,Lat,dLat=dLat,
								Date=date0,Mag=Mag,LonRange=LonRange)

	#now call RTI function
	return RTI(Radar,Date,ut,Beams,Gates,Param=Param,fig=fig,maps=maps,
				zlog=zlog,scale=scale,cmap=cmap,Mag=Mag,yaxistype=yaxistype,
				nobar=nobar,ZeroMean=ZeroMean,Detrend=Detrend,MaxVal=MaxVal,
				ShowScatter=ShowScatter)
