import numpy as np

def GetScale(P,nsigma=3.0,MeanZero=False,FromZero=False):
	'''
	Calculate the scale limits for a plot (this should help deal with
	outliers with stupidly large values).
	
	Inputs
	======
	P : float
		Array of parameters to work out the scale from.
	nsigma : float
		Number of standard deviations about the mean to use.
	MeanZero : float
		Force the mean to be zero.
	FromZero : float
		Assumes that all values >= 0
	
	Returns
	=======
	scale : float
		2 element array [min,max]
	
	'''
	gd = np.where(np.isfinite(P) & (np.abs(P) < 1e5))
	
	if FromZero or MeanZero:
		mu = 0.0
	else:
		mu = np.mean(P[gd])

	sigma = np.sqrt(np.sum((P[gd]-mu)**2.0)/np.size(P[gd]))
	if FromZero:
		scale = np.array([0.0, mu + nsigma*sigma])
	else:
		scale = np.array([mu - nsigma*sigma, mu + nsigma*sigma])

	return scale
