import numpy as np
import matplotlib.pyplot as plt

def PolarAxis(fig=None,maps=[1,1,0,0],eqlat=45.0,ShowLatLines=True,
					ShowLonLines=True,Background=None):
	'''
	Create a polar axis.
	
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
	eqlat : float
		Most equatorward latitude to plot towards radially (middle of 
		the plot is 90)
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
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]),projection='polar')
	else:
		ax = fig
	
	#set the limits
	ax.set_ylim(90,eqlat)
	
	#set the orientation
	ax.set_rlabel_position(180)
	ax.set_theta_zero_location("S")
	ax.set_theta_direction(1.0)
	
	#tick marks
	rt = np.arange(90,eqlat,-10)
	rtl = ['{:2d}$^\circ$'.format(np.int32(np.round(r))) for r in rt]
	tt = np.arange(24)*15*np.pi/180.0
	ttl = ['']*24
	ax.set_rticks(rt)
	ax.set_yticklabels(rtl)
	ax.set_xticks(tt)
	ax.set_xticklabels(ttl)
	
	#set the grid
	ax.grid(ShowLatLines,axis='y')
	ax.grid(ShowLonLines,axis='x')
	
	#fill the background
	if not Background is None:
		ax.set_facecolor(Background)
	
	return ax
