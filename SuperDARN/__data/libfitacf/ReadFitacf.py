import numpy as np
import ctypes as ct


#define some dtypes
c_bool = ct.c_bool
c_int = ct.c_int
c_float = ct.c_float
c_double = ct.c_double
c_int_ptr = np.ctypeslib.ndpointer(ct.c_int,flags="C_CONTIGUOUS")
c_float_ptr = np.ctypeslib.ndpointer(ct.c_float,flags="C_CONTIGUOUS")
c_double_ptr = np.ctypeslib.ndpointer(ct.c_double,flags="C_CONTIGUOUS")


def _FileSize(f):
	#0 is the offset, relative to 2 (2 is the end of the file, where 1 is current, 0 is beginning)
	return f.seek(0,2)

def _CountRecords(f,size):
	f.seek(4,0)
	nr = 0
	nb = 0
	while f.tell() < size:
		l = int.from_bytes(f.read(4),'little')
		f.seek(np.min([size,f.tell()+l-4]))
		nr += 1
		nb += l
	return nr,nb
	
def _ReadRecord(f):
	pass
	
def _ReadScalars(f):
	pass
	
def _ReadString(f):
	
	
def _ReadScalarVar(f):
	



def ReadFitacf(fname="20020321.2201.00.han.fitacf",Verbose=True):
	
	f = open(fname,'rb')
	size = _FileSize(f)
	nr,nb = _CountRecords(f,size)
	f.close()
	print(nr,nb)
