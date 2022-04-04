import numpy as np
import matplotlib.pyplot as plt


def PlotGridLine(ax,data,xaxis,yrange,norm,cmap):
	'''
	Plot a single horizontal line of a grid - useful for when each
	line in a grid doesn't necessary share the same x-axis
	
	Inputs
	======
	ax : pyplot.Axes
		Subplot instance to plot onto
	data : float
		1-D time series of data to plot
	xaxis : float
		1-D x-axis array, one longer than data
	yrange : float
		2-element array with the min/max y extents of this line
	norm : matplotlib.colors.norm
		This will tell the plot how to normalize the data
	cmap : str
		name of the color map to use
	
	'''
	Data = np.array([data])
	
	xmsh,ymsh=np.meshgrid(xaxis,yrange)
	ax.pcolormesh(xaxis,yrange,Data,cmap=cmap,norm=norm)
