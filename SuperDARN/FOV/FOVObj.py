import numpy as np
from .CheckIndex import CheckIndex
from .SaveFOV import SaveFOV
from .. import Globals
import PyFileIO as pf
from ..Tools.Today import Today

class FOVObj(object):
	def __init__(self,Radar,Date,frang=180.0,rsep=45.0,Altitude=400.0,Model='Chisham08'):
		
		#store stuff
		self.Radar = Radar
		self.Date = Date
		self.frang = frang
		self.rsep = rsep
		self.Model = Model
		self.Altitude = Altitude
		
		#check if it exists
		exists,self.fname = CheckIndex(Radar,Date,frang,rsep,Model)
		
		#save if it doesn't exist
		if not exists:
			SaveFOV(Radar,Date,frang,rsep,Altitude,Model)
		
		#load it
		self._LoadFOV()

		self.mag = {}


	def _LoadFOV(self):
		'''
		Read the FOV coords from the file.
		
		'''
		self.fov = pf.LoadObject(Globals.FOVPath+self.fname)
		self.nBeams,self.nGates = self.fov['glonc'].shape
		self.Beams = np.arange(self.nBeams+1)
		self.Gates = np.arange(self.nGates+1)


	def GetFOV(self,Beams=None,Gates=None,Center=False,Mag=False,GS=False,Date=None):
		'''
		Return part or all of a field of view.
		
		Inputs
		======
		Beams : None|int
			If None - all beams are returned
			If 2 element array-like - beams from Beams[0] to Beams[1]
			are returned
		Gates : None|int
			If None - all Gates are returned
			If 2 element array-like - Gates from Gates[0] to Gates[1]
			are returned
		Center : bool
			If True, only the central coords of the FOV are returned
			otherwise the corners are.
		Mag : bool
			If True, magnetic coordinates are calculated (provide a date 
			for the mode accurate conversion).
		GS : bool
			The ground scatter model will be provided if this is True.
		Date : int
			Date in the format yyyymmdd
			
		Returns
		=======
		lon : float
			array of longitudes
		lat : float
			array of latitudes
		'''
		
		#get the appropriate arrays
		lonstr = 'lon'
		latstr = 'lat'

		if GS:
			lonstr = 'gs' + lonstr
			latstr = 'gs' + latstr
		
		if Center:
			lonstr = lonstr + 'c'
			latstr = latstr + 'c'
			c = 1
		else:
			c = 2
	
		lon = self.fov[lonstr]
		lat = self.fov[latstr]

		#calculate mag coords if needed
		if Mag:
			if Date is None:
				Date = Today()
			
			if Date in self.mag:
				lon,lat = self.mag[Date]
			else:
				lon,lat = _MagFOV(lon,lat,Date)
			
				#add to the dict
				self.mag[Date] = (lon,lat)
				
		#limit beams and gates
		if not Beams is None:
			lon = lon[Beams[0]:Beams[1]+c]
			lat = lat[Beams[0]:Beams[1]+c]
		
		if not Gates is None:
			lon = lon[:,Gates[0]:Gates[1]+c]
			lat = lat[:,Gates[0]:Gates[1]+c]
		
		return lon,lat
