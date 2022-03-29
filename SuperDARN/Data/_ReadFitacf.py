import numpy as np
from .._CFunctions import _CLoadFitacf,_CGetScalarLen,_CGetScalars
from .._CFunctions import _CGetArrayLen,_CGetArrays,_CDelFitacf
from ..ct import ctString,ctBool,ctInt,ctIntPtr,ctLongPtr,ctFloatPtr
from .. import Globals

def _ReadFitacf(fname,Verbose=False):
	'''
	Read a fitacf file, returning two recarrays - one with scalars for 
	each record, the other with arrays of data combined.
	
	Inputs
	======
	fname : str
		name of the fitacf file to load.
	Verbose : bool
		If True, some messages will be printed to stdout during laoding.
	
	Returns
	=======
	sc : numpy.recarray
		Recarray of scalars.
	ar : numpy.recarray
		Recarray of data.
	
	'''
	
	#create the initial fitacf object
	_fname = ctString(fname)
	_Verbose = ctBool(Verbose)
	ID = _CLoadFitacf(_fname,_Verbose)

	#get the lengths of the arrays
	ns = _CGetScalarLen(ID)
	na = _CGetArrayLen(ID)
	
	#create the otuput recarrays
	scout = np.recarray(ns,dtype=Globals.sdtype)
	arout = np.recarray(na,dtype=Globals.adtype)

	#temporary dictionaries
	sc = {}
	for s in Globals.sdtype:
		f,d = s
		sc[f] = np.zeros(ns,dtype=d)
	ar = {}
	for a in Globals.adtype:
		f,d = a
		ar[f] = np.zeros(na,dtype=d)
		
	#return the data
	_CGetScalars(ID,sc['Date'],sc['ut'],sc['Beam'],sc['Channel'],
				sc['ScanCode'],sc['nGates'],sc['smsep'],sc['lagfr'],
				sc['ArrLen'],sc['RecLen'],sc['na'],sc['ArrOffset'])
				
	_CGetArrays(ID,ar['Date'],ar['ut'],ar['Beam'],ar['Channel'],
				ar['ScanCode'],ar['nGates'],ar['smsep'],ar['lagfr'],
				ar['V'],ar['P_l'],ar['W_l'],ar['Gnd'],ar['Gate'],ar['Index'])

	#delete the objects
	_CDelFitacf(ID)

	#fill the recarrays
	for s in Globals.sdtype:
		f,d = s
		scout[f] = sc[f]
	for a in Globals.adtype:
		f,d = a
		arout[f] = ar[f]

	return scout,arout
