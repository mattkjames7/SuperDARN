import numpy as np
import os
from ._CheckHardware import _CheckHardware
from .. import Globals
from datetime import date

def _DownloadHDW():
	'''
	Attempt to download HDW files.
	
	Returns
	=======
	success : bool
		True if the operation was successful
	
	'''
	
	#address of the master zip
	gitadr = 'https://github.com/SuperDARN/rst/archive/refs/heads/master.zip'
	
	#download the zip
	hwpath = Globals.HardwarePath
	os.system('wget ' + gitadr + ' -O '+hwpath+'rst.zip')
	
	#unzip it
	os.system('unzip -q '+hwpath+'rst.zip -d '+hwpath)
	
	#copy the files we need
	os.system('cp -r '+hwpath+'rst-master/tables/superdarn/hdw '+hwpath)
	os.system('cp '+hwpath+'rst-master/tables/superdarn/radar.dat '+hwpath)

	#remove the other stuff
	os.system('rm -fr '+hwpath+'rst-master/')
	os.system('rm '+hwpath+'rst.zip')

	#check if it worked
	success,_ = _CheckHardware()
	
	#get the current date and write it to lastupdate file
	cdate = np.int32(date.today().strftime('%Y%m%d'))
	lu = hwpath + 'lastupdate'
	f = open(lu,'w')
	f.write('{:08d}'.format(cdate))
	f.close()
	
	return success
