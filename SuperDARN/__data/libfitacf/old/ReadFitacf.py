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
	fs = f.seek(0,2)
	f.seek(0,0)
	return fs

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


def GetScalars(f,nr):
	#create scalars array
	sdtype = [	('Date','int32'),
				('Beam','int32'),
				('Channel','int32'),
				('ScanCode','int32'),
				('nGates','int32'),
				('lagfr','int32'),
				('smsep','int32'),
				('ArrLen','int32'),
				('RecLen','int32'),
				('na','int32'),
				('ut','float32'),
				('ArrOffset','int64')]
	sc = np.recarray(nr,dtype=sdtype)
	
	#loop through each position, storing the position each time
	p = 0
	for i in range(0,nr):
		#seek to the start position of the current record
		f.seek(p,0)
	
		#Read in the scalars
		sc[i] = _ReadScalars(f)
		
		#update position
		p += sc[i].RecLen
		
	return sc
	
def _ReadHeader(f):
	magic,size,ns,na = np.fromfile(f,dtype='int32',count=4)
	return magic,size,ns,na
	
		
def _ReadScalars(f):
	#return a single record
	sdtype = [	('Date','int32'),
				('Beam','int32'),
				('Channel','int32'),
				('ScanCode','int32'),
				('nGates','int32'),
				('lagfr','int32'),
				('smsep','int32'),
				('ArrLen','int32'),
				('RecLen','int32'),
				('na','int32'),
				('ut','float32'),
				('ArrOffset','int64')]
	sc = np.recarray(1,dtype=sdtype)
	
	#read in the header first
	magic,size,ns,na = _ReadHeader(f)
	
	#list the fields
	fields = {	'cp' : 'ScanCode',
				'lagfr' : 'lagfr',
				'smsep' : 'smsep',
				'channel' : 'Channel',
				'bmnum' : 'Beam',
				'nrang' : 'nGates',}
	fk = list(fields.keys())
				
	#some temporary time variables
	time = {	'yr' : 0,
				'mo' : 0,
				'dy' : 0,
				'hr' : 0,
				'mt' : 0,
				'sc' : 0,
				'us' : 0}
	
	#read each scalar in
	for i in range(0,ns):
		#read the name of the variable in
		vname = _ReadString(f)
		
		#get the dtype
		dt,_ = _ReadDtype(f)
		
		#read the variable
		var = _ReadVar(f,dt)
	
		#check if it's a time variable
		if 'time' in vname:
			_,v = vname.split('.')
			time[v] = var
		elif vname in fk:
			ff = fields[vname]
			sc[ff] = var
			
	#calculate the date and time
	sc.Date = time['yr']*10000 + time['mo']*100 + time['dy']
	sc.ut = np.float32(time['hr']) + time['mt']/60.0 + time['sc']/3600.0 + time['us']/(3600.0*1000000.0)
	
	#input the other stuff
	sc.na = na
	sc.RecLen = size
	sc.ArrOffset = f.tell()
	sc.ArrLen = _GetArrayLen(f,sc.ArrOffset[0],sc.na[0])
	
	
	return sc

def _GetArrayLen(f,ArrOffset,na):
	#seek to the offset of the start of the arrays
	f.seek(ArrOffset,0)
	
	#loop through each array variable until we find one in the following list
	out = 0
	for i in range(0,na):
		
		#read the name of the variable
		vname = _ReadString(f)
		#dtype
		dtype,byte = _ReadDtype(f)
		
		#dimensions
		nd,shape,size = _ReadShape(f)
		
		#check if this is one of the required arrays
		if vname in ['v','p_l','w_l','gflg','slist']:
			out = size
			break

		#otherwise, skip to the next array
		if dtype == 'str':
			for i in range(0,size):
				tmp = _ReadString(f)
		else:
			f.seek(size*byte,1)
		
	return out
		
	
def _ReadDtype(f):
	#an unsigned integer defines the dtype 
	tmp = np.fromfile(f,dtype='int8',count=1)[0]

	dts = { 1 : ('uint8',1),
			2 : ('int16',2),
			3 : ('int32',4),
			4 : ('float32',4),
			8 : ('float64',8)}
			
	return dts.get(tmp,('str',0))
	
def _ReadShape(f):
	#dimensions
	ndim = np.fromfile(f,dtype='int32',count=1)[0]
	shape = np.fromfile(f,dtype='int32',count=ndim)
	size = np.prod(shape)
	return ndim,shape,size
	
	
def _ReadVar(f,dtype):
	if dtype == 'str':
		out = _ReadString(f)
	else:
		out = np.fromfile(f,dtype=dtype,count=1)[0]
	return out
		
def _ReadString(f):
	
	#read in individual bytes until we find 0
	b = []
	go = True
	while go:
		tmp = np.fromfile(f,dtype='uint8',count=1)[0]
		if tmp == 0:
			break
		else:
			b.append(tmp)
	
	#convert bytes to characters
	s = ''.join([chr(c) for c in b])

	return s

def _ReadRecordArrays(f,ArrOffset,na):
	#seek to the offset of the start of the arrays
	f.seek(ArrOffset,0)
	
	#loop through each array variable until we find one in the following list
	out = 0
	for i in range(0,na):
		
		#read the name of the variable
		vname = _ReadString(f)
		#dtype
		dtype,byte = _ReadDtype(f)
		
		#dimensions
		nd,shape,size = _ReadShape(f)
		
		#check if this is one of the required arrays
		if vname  == 'v':
			v = np.fromfile(f,dtype=dtype,count=size)
		elif vname == 'p_l':
			p = np.fromfile(f,dtype=dtype,count=size)
		elif vname == 'w_l':
			w = np.fromfile(f,dtype=dtype,count=size)
		elif vname == 'gflg':
			g = np.fromfile(f,dtype=dtype,count=size)
		elif vname == 'slist':
			r = np.fromfile(f,dtype=dtype,count=size)
		else:	
			#otherwise, skip to the next array
			if dtype == 'str':
				for i in range(0,size):
					tmp = _ReadString(f)
			else:
				f.seek(size*byte,1)
		
	return v,p,w,g,r

		
def GetArrays(f,nr,sc):
	#create an output dtype
	adtype = [	('Date','int32'),
				('ut','float32'),
				('Beam','int32'),
				('Channel','int32'),
				('ScanCode','int32'),
				('nGates','int32'),
				('lagfr','int32'),
				('smsep','int32'),
				('V','float32'),
				('P_l','float32'),
				('W_l','float32'),
				('Gnd','float32'),
				('Gate','float32')]
	
	# count the number of elements
	ne = np.sum(sc.ArrLen) + np.sum(sc.ArrLen == 0)
	
	out = np.recarray(ne,dtype=adtype)
	akeys = out.dtype.names
	skeys = sc.dtype.names
	
	P = 0
	for i in range(0,nr):
		
		if sc.ArrLen[i] > 0:
			pe = sc.ArrLen[i]
			v,p,w,g,r = _ReadRecordArrays(f,sc.ArrOffset[i],sc.na[i])
			#print(P,pe,v.shape)
			out['V'][P:P+pe] = v
			out['P_l'][P:P+pe] = p
			out['W_l'][P:P+pe] = w
			out['Gnd'][P:P+pe] = g
			out['Gate'][P:P+pe] = r
		else:
			pe = 1
			out['V'][P:P+pe] = 0.0
			out['P_l'][P:P+pe] = 0.0
			out['W_l'][P:P+pe] = 0.0
			out['Gnd'][P:P+pe] = -1
			out['Gate'][P:P+pe] = -1


		for k in akeys:
			if k in skeys:
				out[k][P:P+pe] = sc[k][i]
		P += pe

	return out

def ReadFitacf(fname="20020321.2201.00.han.fitacf",Verbose=True):
	
	f = open(fname,'rb')
	size = _FileSize(f)
	nr,nb = _CountRecords(f,size)
				
	#read in the scalars
	sc = GetScalars(f,nr)
	
	#read in the arrays
	ar = GetArrays(f,nr,sc)
	
	f.close()
	return sc,ar

