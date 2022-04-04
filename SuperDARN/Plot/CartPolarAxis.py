import numpy as np
import matplotlib.pyplot as plt

def CartPolarAxis(	fig=None,maps=[1,1,0,0],xrnge=[-90.0,90.0],
					yrnge=[-90.0,90.0],ShowLatLines=True,
					ShowLonLines=True,Background=None):
	'''
	Create a polar axis which uses Cartesian coordinates (useful for 
	zooming in).
	
	Inputs
	======
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
	xrnge : float
		2-element array of x-axis range (in degree latitude)
	yrnge : float
		2-element array of y-axis range (in degree latitude)
	ShowLatLines : bool
		Show lines of latitude every 10 degrees
	ShowLonLines : bool
		Show the lines of longitude/local time every 15 degrees
	Background : float
		3 or 4 element array providing a background color.
		
	Returns
	=======
	ax : pyplot.Axes
		axes of a plot
			
	'''
	#create the axes
	if fig is None:
		fig = plt
		fig.figure()
	if hasattr(fig,'Axes'):	
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
	else:
		ax = fig
	
	#set the limits
	ax.set_xlim(xrnge)
	ax.set_ylim(yrnge)
	ax.set_aspect(1.0)
	
	#tick marks/grid
	if ShowLatLines:
		rt = np.arange(80,-1.0,-10)
		rtl = ['{:2d}$^\circ$'.format(np.int32(np.round(r))) for r in rt]
		a = np.arange(361,dtype='int32')*np.pi/180.0	
		xt = np.cos(a)
		yt = np.sin(a)
		for r,rl in zip(rt,rtl):
			d = 90 - r
			xr = xt*d
			yr = yt*d
			ax.plot(xr,yr,color=[0.7,0.7,0.7,0.5],linewidth=0.5)
			if d < np.max(yrnge):
				ax.text(0.0,d,rl,size='small')
		
	if ShowLonLines:
		tt = np.arange(24)*15*np.pi/180.0
		xt = 90.0*np.cos(tt)
		yt = 90.0*np.sin(tt)
		for x,y in zip(xt,yt):
			ax.plot([0.0,x],[0.0,y],color=[0.7,0.7,0.7,0.5],linewidth=0.5)
	
	ax.set_xticks([])
	ax.set_yticks([])
	

	
	#fill the background
	if not Background is None:
		ax.set_facecolor(Background)
	
	return ax
