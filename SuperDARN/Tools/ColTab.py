import numpy as np
import matplotlib as mpl


def ColTabbw():
	
	cdict = {'red':   ((0.0, 0.0, 0.0), 
					   (1.0, 1.0, 1.0)),

			 'green': ((0.0, 0.0, 0.0),
					   (1.0, 1.0, 1.0)),

			 'blue':  ((0.0, 0.0, 0.0),
					   (1.0, 1.0, 1.0)) 
			  }	
			  
	col_map=mpl.colors.LinearSegmentedColormap('bw',cdict)
	
	return col_map

def ColTabBinary(col0,col1):
	
	cdict = {'red':   ((0.0, col0[0], col0[0]), 
					   (0.5, col0[0], col1[0]),
					   (1.0, col1[0], col1[0])),

			 'green': ((0.0, col0[1], col0[1]), 
					   (0.5, col0[1], col1[1]),
					   (1.0, col1[1], col1[1])),

			 'blue':  ((0.0, col0[2], col0[2]), 
					   (0.5, col0[2], col1[2]),
					   (1.0, col1[2], col1[2])), 
					   
			 'alpha': ((0.0, col0[3], col0[3]), 
					   (0.5, col0[3], col1[3]),
					   (1.0, col1[3], col1[3]))
			  }	
			  
	col_map=mpl.colors.LinearSegmentedColormap('binary',cdict)
	
	return col_map

def ColTabwb():
	
	cdict = {'red':   ((0.0, 1.0, 1.0), 
					   (1.0, 0.0, 0.0)),

			 'green': ((0.0, 1.0, 1.0),
					   (1.0, 0.0, 0.0)),

			 'blue':  ((0.0, 1.0, 1.0),
					   (1.0, 0.0, 0.0)) 
			  }	
			  
	col_map=mpl.colors.LinearSegmentedColormap('wb',cdict)
	
	return col_map


def ColTabbcyr():
	
	cdict = {'red':   ((0.0, 0.0, 0.0), 
					   (0.5, 0.0, 1.0), 
					   (1.0, 1.0, 1.0)),

			 'green': ((0.0, 0.0, 0.0),
					   (0.5, 1.0, 1.0),
					   (1.0, 0.0, 0.0)),

			 'blue':  ((0.0, 0.0, 1.0),
					   (0.5, 1.0, 0.0), 
					   (1.0, 0.0, 0.0)) 
			  }	
			  
	col_map=mpl.colors.LinearSegmentedColormap('bcyr',cdict)
	
	return col_map


def ColTabbr():
	
	cdict = {'red':   ((0.0, 0.0, 0.0), 
					   (1.0, 1.0, 1.0)),

			 'green': ((0.0, 0.0, 0.0),
					   (1.0, 0.0, 0.0)),

			 'blue':  ((0.0, 1.0, 1.0),
					   (1.0, 0.0, 0.0)) 
			  }	
			  
	col_map=mpl.colors.LinearSegmentedColormap('br',cdict)
	
	return col_map

def ColTabyr():
	
	cdict = {'red':   ((0.0, 1.0, 1.0), 
					   (1.0, 1.0, 1.0)),

			 'green': ((0.0, 1.0, 1.0),
					   (1.0, 0.0, 0.0)),

			 'blue':  ((0.0, 0.0, 0.0),
					   (1.0, 0.0, 0.0)) 
			  }	
			  
	col_map=mpl.colors.LinearSegmentedColormap('yr',cdict)
	
	return col_map

def ColTabor():
	
	cdict = {'red':   ((0.0, 1.0, 1.0), 
					   (1.0, 1.0, 1.0)),

			 'green': ((0.0, 0.5, 0.5),
					   (1.0, 0.0, 0.0)),

			 'blue':  ((0.0, 0.0, 0.0),
					   (1.0, 0.0, 0.0)) 
			  }	
			  
	col_map=mpl.colors.LinearSegmentedColormap('or',cdict)
	
	return col_map

def ColTabwyr():
	
	cdict = {'red':   ((0.0, 1.0, 1.0), 
					   (0.5, 1.0, 1.0), 
					   (1.0, 1.0, 1.0)),

			 'green': ((0.0, 1.0, 1.0),
					   (0.5, 1.0, 1.0),
					   (1.0, 0.0, 0.0)),

			 'blue':  ((0.0, 1.0, 1.0),
					   (0.5, 0.0, 0.0), 
					   (1.0, 0.0, 0.0)) 
			  }	
			  
	col_map=mpl.colors.LinearSegmentedColormap('wyr',cdict)
	
	return col_map

def ColTab6Step():
	
	cdict = {'red':   ((0.0, 0.5, 0.5), 
					   (0.167, 0.5, 0.0), 
					   (0.333, 0.0, 0.0), 
					   (0.5, 0.0, 0.0), 
					   (0.667, 0.0, 1.0),
					   (0.833, 1.0, 1.0),  
					   (1.0, 1.0, 1.0)),

			 'green': ((0.0, 0.0, 0.0),
					   (0.167, 0.0, 0.0), 
					   (0.333, 0.0, 0.5), 
					   (0.5, 0.5, 1.0), 
					   (0.667, 1.0, 1.0),
					   (0.833, 1.0, 0.0), 
					   (1.0, 0.0, 0.0)),

			 'blue':  ((0.0, 1.0, 1.0),
					   (0.167, 1.0, 1.0), 
					   (0.333, 1.0, 1.0), 
					   (0.5, 1.0, 0.0), 
					   (0.667, 0.0, 0.0),
					   (0.833, 0.0, 0.0),  
					   (1.0, 0.0, 0.0)) 
			  }	
			  
	col_map=mpl.colors.LinearSegmentedColormap('6step',cdict)
	
	return col_map
	
def ColTabCircular():
	cdict = {'red':   ((0.0, 1.0, 1.0), 
					   (0.25,1.0, 1.0),
					   (0.5, 1.0, 1.0),
					   (0.75,1.0, 1.0), 
					   (1.0, 1.0, 1.0)),

			 'green': ((0.0, 0.0, 0.0),
					   (0.25,0.0, 0.0),
					   (0.5, 1.0, 1.0),
					   (0.75,1.0, 1.0), 
					   (1.0, 0.0, 0.0)),

			 'blue':  ((0.0, 0.0, 0.0),
					   (0.25,1.0, 1.0),
					   (0.5, 1.0, 1.0),
					   (0.75,0.0, 0.0), 
					   (1.0, 0.0, 0.0)),
			  }	
			  	
	col_map=mpl.colors.LinearSegmentedColormap('Circular',cdict)
	
	return col_map

def ColTabNonLin():
	cdict = {'red':   ((  0.0, 1.0, 1.0), #white  1.0 1.0 1.0
					   ( 0.01, 0.0, 0.0), #blue   0.0 0.0 1.0
					   (0.025, 0.7, 0.7), #purple 0.7 0.0 0.7
					   (0.063, 0.0, 0.0), #green  0.0 1.0 0.0
					   (0.158, 1.0, 1.0), #yellow 1.0 1.0 0.0
					   (0.398, 1.0, 1.0), #red    1.0 0.0 0.0
					   (  1.0, 0.0, 0.0)), #black 0.0 0.0 0.0

			 'green': ((  0.0, 1.0, 1.0),
					   ( 0.01, 0.0, 0.0),
					   (0.025, 0.0, 0.0),
					   (0.063, 1.0, 1.0), 
					   (0.158, 1.0, 1.0),
					   (0.398, 0.0, 0.0),
					   (  1.0, 0.0, 0.0)),

			 'blue':  ((  0.0, 1.0, 1.0),
					   ( 0.01, 1.0, 1.0),
					   (0.025, 0.7, 0.7),
					   (0.063, 0.0, 0.0), 
					   (0.158, 0.0, 0.0),
					   (0.398, 0.0, 0.0),
					   (  1.0, 0.0, 0.0)),
			  }	
			  	
	col_map=mpl.colors.LinearSegmentedColormap('NonLin',cdict)
	
	return col_map



def ColTabNonLin2():
	cdict = {'red':   ((  0.0, 1.0, 1.0), #white  1.0 1.0 1.0
					   (0.025, 0.5, 0.5), #purple 0.7 0.0 0.7
					   (0.063, 1.0, 1.0), #pink   1.0 0.5 0.5
					   (0.158, 1.0, 1.0), #yellow 1.0 1.0 0.0
					   (0.398, 1.0, 1.0), #red    1.0 0.0 0.0
					   (  1.0, 0.0, 0.0)),#black  0.0 0.0 0.0

			 'green': ((  0.0, 1.0, 1.0),
					   (0.025, 0.0, 0.0),
					   (0.063, 0.5, 0.5), 
					   (0.158, 1.0, 1.0),
					   (0.398, 0.0, 0.0),
					   (  1.0, 0.0, 0.0)),

			 'blue':  ((  0.0, 1.0, 1.0),
					   (0.025, 0.5, 0.5),
					   (0.063, 0.5, 0.5), 
					   (0.158, 0.0, 0.0),
					   (0.398, 0.0, 0.0),
					   (  1.0, 0.0, 0.0)),
			  }	
			  	
	col_map=mpl.colors.LinearSegmentedColormap('NonLin2',cdict)
	
	return col_map
