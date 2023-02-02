import os

#check if environment variable has been set
FitACFPath = os.getenv('FITACF_PATH')
if FitACFPath is None:
	raise EnvironmentError('Please set the FITACF_PATH environment variable before importing')
if FitACFPath[-1] != '/':
	FitACFPath += '/'

DataPath = os.getenv('SUPERDARN_PATH')
if DataPath is None:
	raise EnvironmentError('Please set the SUPERDARN_PATH environment variable before importing')
if DataPath[-1] != '/':
	DataPath += '/'

ModulePath = os.path.dirname(__file__)+'/__data/'

HardwarePath = DataPath + 'Hardware/'
FOVPath = DataPath + 'FOV/'

#libWithinFOV = ct.CDLL(ModulePath + 'libWithinFov/libWithinFov.so')
#FitACFPath = '/data/sol-ionosphere/fitacf/'

Radars = None
Hardware = None
FOV = {}
Data = {}

#data types for fitacf (scalars and arrays)
sdtype = [	('Date','int32'),			#Date in format yyyymmdd
			('ut','float32'),			#ut hours (time of record/scan)
			('Beam','int32'),			#beam number
			('Channel','int32'),		#channel id
			('ScanCode','int32'),		#Scan code
			('nGates','int32'),			#number of range gates
			('smsep','int32'),			#sample separation in microseconds
			('lagfr','int32'),			#lag in microseconds to first range
			('rsep','int32'),			#sample separation in km
			('frang','int32'),			#km to first range
			('ArrLen','int32'),			#length of arrays stored in this record
			('RecLen','int32'),			#record length in bytes
			('na','int32'),				#the number of array variablesin the record
			('ArrOffset','int64')]		#file offset of the start of the arrays
				
adtype = [	('Date','int32'),			#Date in format yyyymmdd
			('ut','float32'),			#UT hours
			('Beam','int32'),			#beam number
			('Channel','int32'),		#channel id
			('ScanCode','int32'),		#scan code
			('nGates','int32'),			#number of gates
			('smsep','int32'),			#sample separation in microseconds
			('lagfr','int32'),			#lag to first range in microseconds
			('rsep','int32'),			#sample separation in km
			('frang','int32'),			#distance to first range in km
			('V','float32'),			#velocity
			('P_l','float32'),			#power from lambda fit
			('W_l','float32'),			#lambda spectral width
			('Gnd','int32'),			#ground scatter flag
			('Gate','int32'),			#range gate number
			('Index','int32')]			#record index

#hardware dtype
hwdtype = [	('id','int32'),
			('StartDate','int32'),
			('StartTime','float32'),
			('EndDate','int32'),
			('EndTime','float32'),
			('Status','int32'),
			('Glat','float32'),
			('Glon','float32'),
			('Alt','float32'),
			('Boresight','float32'),
			('BeamSep','float32'),
			('Vsign','int32'),
			('RxStep','int32'),
			('TdiffA','float32'),
			('TdiffB','float32'),
			('PhaseSign','int32'),
			('IFOffsetx','float32'),
			('IFOffsety','float32'),
			('IFOffsetz','float32'),
			('RxRiseT','float32'),
			('AttenStage','int32'),
			('nGates','int32'),
			('nBeams','int32')]
