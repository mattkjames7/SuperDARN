import numpy as np
import matplotlib.pyplot as plt


def PlotGridLine(ax,data,xaxis,yrange,norm,cmap):
	'''
	Plot a single horizontal line of a grid - useful for when each
	line in a grid doesn't necessary share the same x-axis
	'''
	Data = np.array([data])
	
	xmsh,ymsh=np.meshgrid(xaxis,yrange)
	ax.pcolormesh(xaxis,yrange,Data,cmap=cmap,norm=norm)
