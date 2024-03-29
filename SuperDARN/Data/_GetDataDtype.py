import numpy as np


def _GetDataDtype(nB,nG):
	'''
	This is not used.
	
	'''
	
	dtype = [	('Date','int32'),			#Date in format yyyymmdd
				('ut','float32'),			#UT hours
				('Channel','int32'),		#channel id
				('ScanCode','int32'),		#scan code
				('nBeams','int32'),			#number of beams
				('nGates','int32'),			#number of gates
				('smsep','int32'),			#sample separation in microseconds
				('lagfr','int32'),			#lag to first range in microseconds
				('rsep','int32'),			#sample separation in km
				('frang','int32'),			#km to first range
				('V','float32',(nB,nG)),	#velocity
				('P_l','float32',(nB,nG)),	#power from lambda fit
				('W_l','float32',(nB,nG)),	#lambda spectral width
				('Gnd','int32',(nB,nG))]	#ground scatter flag

	return dtype

def _GetBeamDtype(nG):
	'''
	This is used to define the numpy.recarray dtype, where the number
	of range gates may differ from one radar to another.
	
	Inputs
	======
	nG : int
		Total number of range gates.
		
	Returns
	=======
	dtype : list
		list of dtype tuples for defining the numpy.recarray
	
	'''
	dtype = [	('Date','int32'),			#Date in format yyyymmdd
				('ut','float32'),			#UT hours
				('Channel','int32'),		#channel id
				('ScanCode','int32'),		#scan code
				('nBeams','int32'),			#number of beams
				('nGates','int32'),			#number of gates
				('smsep','int32'),			#sample separation in microseconds
				('lagfr','int32'),			#lag to first range in microseconds
				('rsep','int32'),			#sample separation in km
				('frang','int32'),			#km to first range
				('V','float32',(nG,)),		#velocity
				('P_l','float32',(nG,)),	#power from lambda fit
				('W_l','float32',(nG,)),	#lambda spectral width
				('Gnd','int32',(nG,))]		#ground scatter flag

	return dtype
