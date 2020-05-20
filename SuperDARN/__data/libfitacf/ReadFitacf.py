import ctypes as ct
import numpy as np
from numpy.ctypeslib import ndpointer

def ReadFitacf(fname="20120425.0801.00.han.fitacf",Verbose=True):
	
	lib=ct.CDLL('./libfitacf.so')
	libfunc = lib.ReadFITACF
	freeint = lib.FreeInt
	freeflt = lib.FreeFloat
	
	libfunc.argtypes = [ct.c_char_p,
						ndpointer(ct.c_int, flags="C_CONTIGUOUS"),
						ndpointer(ct.c_int, flags="C_CONTIGUOUS"),
						ct.POINTER(ct.POINTER(ct.c_int)),
						ct.POINTER(ct.POINTER(ct.c_float)),
						ct.POINTER(ct.POINTER(ct.c_int)),
						ct.POINTER(ct.POINTER(ct.c_int)),
						ct.POINTER(ct.POINTER(ct.c_int)),
						ct.POINTER(ct.POINTER(ct.c_int)),
						ct.POINTER(ct.POINTER(ct.c_int)),
						ct.POINTER(ct.POINTER(ct.c_int)),
						ct.POINTER(ct.POINTER(ct.c_float)),
						ct.POINTER(ct.POINTER(ct.c_float)),
						ct.POINTER(ct.POINTER(ct.c_float)),
						ct.POINTER(ct.POINTER(ct.c_int)),
						ct.POINTER(ct.POINTER(ct.c_int)),
						ct.c_int]	
	
	freeint.argtypes = [ct.POINTER(ct.c_int)]
	freeflt.argtypes = [ct.POINTER(ct.c_float)]

	fstring = fname.encode('utf-8')
	nRec = np.array([0],dtype='int32')
	n = np.array([0],dtype='int32')
	Date = ct.POINTER(ct.c_int)()
	ut = ct.POINTER(ct.c_float)()
	Beam = ct.POINTER(ct.c_int)()
	Channel = ct.POINTER(ct.c_int)()
	ScanCode = ct.POINTER(ct.c_int)()
	nGates = ct.POINTER(ct.c_int)()
	lagfr = ct.POINTER(ct.c_int)()
	smsep = ct.POINTER(ct.c_int)()
	V = ct.POINTER(ct.c_float)()
	P_l = ct.POINTER(ct.c_float)()
	W_l = ct.POINTER(ct.c_float)()
	Gnd = ct.POINTER(ct.c_int)()
	Gate = ct.POINTER(ct.c_int)()
	
	libfunc(fstring,nRec,n,ct.byref(Date),ct.byref(ut),ct.byref(Beam),ct.byref(Channel),ct.byref(ScanCode),ct.byref(nGates),
			ct.byref(lagfr),ct.byref(smsep),ct.byref(V),ct.byref(P_l),ct.byref(W_l),ct.byref(Gnd),ct.byref(Gate),np.int32(Verbose))
			
	n = n[0]
	dtype = [('Date','int32'),('ut','float32'),('Beam','int32'),('Channel','int32'),('ScanCode','int32'),('nGates','int32'),('lagfr','int32'),
			('smsep','int32'),('V','float32'),('P_l','float32'),('W_l','float32'),('Gnd','bool'),('Gate','int32')]
	
	data = np.recarray(n,dtype=dtype)
	
	data.Date = np.array([Date[i] for i in range(0,n)])
	data.ut = np.array([ut[i] for i in range(0,n)])
	data.Beam = np.array([Beam[i] for i in range(0,n)])
	data.Channel = np.array([Channel[i] for i in range(0,n)])
	data.ScanCode = np.array([ScanCode[i] for i in range(0,n)])
	data.nGates = np.array([nGates[i] for i in range(0,n)])
	data.lagfr = np.array([lagfr[i] for i in range(0,n)])
	data.smsep = np.array([smsep[i] for i in range(0,n)])
	data.V = np.array([V[i] for i in range(0,n)])
	data.P_l = np.array([P_l[i] for i in range(0,n)])
	data.W_l = np.array([W_l[i] for i in range(0,n)])
	data.Gnd = np.array([Gnd[i] for i in range(0,n)])
	data.Gate = np.array([Gate[i] for i in range(0,n)])
	
	freeint(Date)
	freeflt(ut)
	freeint(Beam)
	freeint(Channel)
	freeint(ScanCode)
	freeint(nGates)
	freeint(lagfr)
	freeint(smsep)
	freeflt(V)
	freeflt(P_l)
	freeflt(W_l)
	freeint(Gnd)
	freeint(Gate)
	return data
