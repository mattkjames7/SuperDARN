import numpy as np


def _GroundRange(r,hv):
	'''
	Calculate the ground range assuming a spherical earth.
	
	Inputs
	======
	r : float
		slant range (km)
	hv : float
		virtual height (km)
	
	Returns
	=======
	gr : float
		ground range (km)
	phi : float
		angle between radar and each range (deg)
	'''
	
	#use the cosine rule to calculate the angle
	Re = 6371.0
	r2 = r*r
	Re2 = Re*Re
	Reh = Re + hv
	Reh2 = Reh*Reh
	cosphi = (Re2 + Reh2 - r2)/(2.0*Re*Reh)
	phi = np.arccos(cosphi)
	
	#work out the ground distance
	gr = phi*Re
	
	return gr,phi*180.0/np.pi
	
