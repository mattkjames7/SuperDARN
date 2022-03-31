import numpy as np

def _OldModel(r,Altitude=400.0):
	'''
	Return the old model of the virtual height (as defined in Chisham et
	al. 2008).
	
	'''
	if r < 150.0:
		return 115.0*r/150.0
	elif (r >= 150.0) and (r < 600.0):
		return 115.0
	elif (r >= 600.0) and (r < 800.0):
		return ((r-600.0)/200.0)*(Altitude - 115.0) + 115.0
	else:
		return Altitude
	
def _ChishamModel(r,Altitude=400.0):
	'''
	Return the Chisham et al 2008 model for virtual height.
	'''
	#constants for the different half-hops
	A = [108.974,384.416,1098.28]
	B = [0.0191271,-0.178640,-0.354557]
	C = [6.68283e-5,1.81405e-4,9.39961e-5]
	
	#select which parameters to use based on distance
	if r < 790:
		i = 0
	elif r >= 790 and r < 2130:
		i = 1
	else: 
		i = 2
	
	#calculate the model (equation 12)
	return A[i] + B[i]*r + C[i]*r**2
	
	

def _VirtualHeight(r,Model='chisham08',Altitude=400.0):
	'''
	Use Chisham et al 2008 
	
	Inputs
	======
	r : float
		Slant range (km) 1D array.
	Model : str
		'chisham08' - use the Chisham et al 2008 model
		'old' - use the old model
	Altitude : float
		Maximum altitude for the old model.
	
	Returns
	=======
	out : float
		Array of virtual heights in km.
	
	'''

	#select the model
	if Model == 'chisham08':
		modelfunc = _ChishamModel
	else:
		modelfunc = _OldModel
		
	#output array
	out = np.zeros(np.size(r),dtype='float64')
	for i in range(0,out.size):
		out[i] = modelfunc(r[i])
		
	return out
	
