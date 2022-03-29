import numpy as np
from .ct import c_char_p,c_bool,c_bool_ptr,c_int,c_int_ptr,c_long,c_long_ptr
from .ct import c_float,c_float_ptr,c_double,c_double_ptr,c_double_ptr_ptr
from ._CppLib import _GetLib

#try loading the C++ library
libfitacf = _GetLib()


_CLoadFitacf = libfitacf.LoadFitacf
_CLoadFitacf.restype = c_int
_CLoadFitacf.argtypes = [	c_char_p,	#file name
							c_bool]		#verbose
							

_CGetScalarLen = libfitacf.GetScalarLen
_CGetScalarLen.restype = c_int
_CGetScalarLen.argtypes = [	c_int]		#fitacf ID


_CGetScalars = libfitacf.GetScalars
_CGetScalars.restype = None
_CGetScalars.argtypes = [	c_int,			#ID
							c_int_ptr,		#Date
							c_float_ptr,	#ut
							c_int_ptr,		#Beam
							c_int_ptr,		#Channel
							c_int_ptr,		#ScanCode
							c_int_ptr,		#nGates
							c_int_ptr,		#smsep
							c_int_ptr,		#lagfr
							c_int_ptr,		#ArrLen
							c_int_ptr,		#RecLen
							c_int_ptr,		#na
							c_long_ptr]		#ArrOffset

_CGetArrayLen = libfitacf.GetArrayLen
_CGetArrayLen.restype = c_int
_CGetArrayLen.argtypes = [	c_int]		#fitacf ID


_CGetArrays = libfitacf.GetArrays
_CGetArrays.restype = None
_CGetArrays.argtypes = [	c_int,			#ID
							c_int_ptr,		#Date
							c_float_ptr,	#ut
							c_int_ptr,		#Beam
							c_int_ptr,		#Channel
							c_int_ptr,		#ScanCode
							c_int_ptr,		#nGates
							c_int_ptr,		#smsep
							c_int_ptr,		#lagfr
							c_float_ptr,	#V
							c_float_ptr,	#P_l
							c_float_ptr,	#W_l
							c_int_ptr,		#Gnd
							c_int_ptr,		#Gate
							c_int_ptr]		#Index
							
_CDelFitacf = libfitacf.DelFitacf
_CDelFitacf.restype = None
_CDelFitacf.argtypes = [	c_int]			#ID
