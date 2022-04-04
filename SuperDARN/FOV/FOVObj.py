import numpy as np
from .CheckIndex import CheckIndex
from .SaveFOV import SaveFOV
from .. import Globals
import PyFileIO as pf
from ..Tools.Today import Today
from ..Plot.PolarAxis import PolarAxis
from ..Plot.PolarCoasts import PolarCoasts
import DateTimeTools as TT
from ..Tools.Today import Today
from ..Tools.Now import Now
import aacgmv2
from ..Tools.ConvertGeo import ConvertGeo
from ._MagFOV import _MagFOV

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
		lonstr = 'glon'
		latstr = 'glat'

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

	def CellCoords(self,Beams,Gates,Date=None,ut=None,Mag=False,GS=False):
		
		lon,lat = self.GetFOV(Center=True,Mag=Mag,GS=GS,Date=Date)
		
		return lon[Beams,Gates],lat[Beams,Gates]
		
		

	def PlotPolar(self,Beams=None,Gates=None,color='black',linewidth=0.5,
					ShowBeams=True,ShowCells=True,Mag=False,
					GS=False,Date=None,ut=None,fig=None,maps=[1,1,0,0],
					eqlat=45.0,ShowLatLines=True,ShowLonLines=True,
					Background=None,Continents=None,Coasts='black',
					Lon=False,Method='aacgm'):

		#get date and time
		if Date is None:
			Date = Today()
		if ut is None:
			ut = Now()			


		#create the axes
		if fig is None:
			ax = PolarAxis(maps=maps,eqlat=eqlat,ShowLatLines=ShowLatLines,
							ShowLonLines=ShowLonLines,Background=Background)
			if self.fov['glat'][0][0] > 0:
				hem = 'north'
			else:
				hem = 'south'
			PolarCoasts(ax,Date=Date,ut=ut,Lon=Lon,Hemisphere=hem,Mag=Mag,
						Fill=Continents,Method=Method,color=Coasts)
		else:
			ax = fig		


		#get the FOV
		lon,lat = self.GetFOV(Beams=Beams,Gates=Gates,Mag=False,GS=GS,Date=Date)
		
		#convert to the appropriate coordinate system
		t,r = ConvertGeo(lon,lat,Date=Date,ut=ut,Mag=Mag,Lon=Lon,Method=Method)
				
		if self.fov['glat'][0][0] < 0:
			r = -r
			
		#plot each beam edge
		if ShowBeams:
			for i in range(0,t.shape[0]):
				ax.plot(t[i],r[i],color=color,linewidth=linewidth)
		else:
			ax.plot(t[0],r[0],color=color,linewidth=linewidth)
			ax.plot(t[-1],r[-1],color=color,linewidth=linewidth)
			
		#and gate edge
		if ShowCells:
			for i in range(0,t.shape[1]):
				ax.plot(t[:,i],r[:,i],color=color,linewidth=linewidth)
		else:
			ax.plot(t[:,0],r[:,0],color=color,linewidth=linewidth)
			ax.plot(t[:,-1],r[:,-1],color=color,linewidth=linewidth)
					
		return ax

	def PlotPolarCells(self,Beams,Gates,color='black',linewidth=0.5,
					Mag=False,GS=False,Date=None,ut=None,fig=None,maps=[1,1,0,0],
					eqlat=45.0,ShowLatLines=True,ShowLonLines=True,
					Background=None,Continents=None,Coasts='black',
					Lon=False,Method='aacgm'):
		
		#get date and time
		if Date is None:
			Date = Today()
		if ut is None:
			ut = Now()			


		#create the axes
		if fig is None:
			ax = PolarAxis(maps=maps,eqlat=eqlat,ShowLatLines=ShowLatLines,
							ShowLonLines=ShowLonLines,Background=Background)
			if self.fov['glat'][0][0] > 0:
				hem = 'north'
			else:
				hem = 'south'
			PolarCoasts(ax,Date=Date,ut=ut,Lon=Lon,Hemisphere=hem,
						Fill=Continents,Method=Method,color=Coasts)
		else:
			ax = fig		


		#get the FOV
		lon,lat = self.GetFOV(Mag=Mag,GS=GS,Date=Date)
		
		#convert to the appropriate coordinate system
		t,r = ConvertGeo(lon,lat,Date=Date,ut=ut,Mag=Mag,Lon=Lon,Method=Method)
				
		if self.fov['glat'][0][0] < 0:
			r = -r
		
		#plot the cells
		nC = np.size(Beams)
		for i in range(0,nC):
			t0 = t[Beams[i],Gates[i]]
			t1 = t[Beams[i]+1,Gates[i]+1]			
			r0 = r[Beams[i],Gates[i]]
			r1 = r[Beams[i]+1,Gates[i]+1]
			
			rp = [r0,r0,r1,r1,r0]
			tp = [t0,t1,t1,t0,t0]
			
			ax.plot(tp,rp,color=color,linewidth=linewidth)
			
		return ax
			
