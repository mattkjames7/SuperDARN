import numpy as np
from .CheckIndex import CheckIndex
from .SaveFOV import SaveFOV
from .. import Globals
import PyFileIO as pf
from ..Tools.Today import Today
import DateTimeTools as TT
from ..Tools.Today import Today
from ..Tools.Now import Now
import aacgmv2
from ..Tools.ConvertGeo import ConvertGeo
from ..Tools.ConvertGeoCart import ConvertGeoCart
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
		

	def CellCorners(self,Beams,Gates,Date=None,ut=None,Mag=False,GS=False):
		
		lon,lat = self.GetFOV(Center=False,Mag=Mag,GS=GS,Date=Date)
		
		#output cells
		clon = []
		clat = []
		for b,g in zip(Beams,Gates):
			ln00 = lon[b,g]
			ln10 = lon[b+1,g]
			ln11 = lon[b+1,g+1]
			ln01 = lon[b,g+1]
			lt00 = lat[b,g]
			lt10 = lat[b+1,g]
			lt11 = lat[b+1,g+1]
			lt01 = lat[b,g+1]
			clon.append(np.array([ln00,ln10,ln11,ln01]))
			clat.append(np.array([lt00,lt10,lt11,lt01]))
		
		return clon,clat

	def PlotPolar(self,Beams=None,Gates=None,color='black',linewidth=0.5,
					ShowBeams=True,ShowCells=True,Mag=False,
					GS=False,Date=None,ut=None,fig=None,maps=[1,1,0,0],
					eqlat=45.0,ShowLatLines=True,ShowLonLines=True,
					Background=None,Continents=None,Coasts='black',
					Lon=False,Method='aacgm',Cart=True):

		from ..Plot.PolarAxis import PolarAxis
		from ..Plot.PolarCoasts import PolarCoasts
		from ..Plot.CartPolarAxis import CartPolarAxis
		from ..Plot.CartPolarCoasts import CartPolarCoasts

		#get date and time
		if Date is None:
			Date = Today()
		if ut is None:
			ut = Now()			

		#get the hemisphere
		if self.fov['glat'][0][0] > 0:
			hem = 'north'
		else:
			hem = 'south'

		#get the FOV
		lon,lat = self.GetFOV(Beams=Beams,Gates=Gates,Mag=False,GS=GS,Date=Date)
		
		if Cart:
			#convert to the appropriate coordinate system
			t,r = ConvertGeoCart(lon,lat,Date=Date,ut=ut,Mag=Mag,Lon=Lon,Method=Method,Hemisphere=hem)
		else:
			#convert to the appropriate coordinate system
			t,r = ConvertGeo(lon,lat,Date=Date,ut=ut,Mag=Mag,Lon=Lon,Method=Method)
					
			if self.fov['glat'][0][0] < 0:
				r = -r
			

		#create the axes
		if fig is None:

			if Cart:
				xrnge = [t.min()-5,t.max()+5]
				yrnge = [r.min()-5,r.max()+5]
				ax = CartPolarAxis(maps=maps,xrnge=xrnge,yrnge=yrnge,ShowLatLines=ShowLatLines,
								ShowLonLines=ShowLonLines,Background=Background)

				CartPolarCoasts(ax,Date=Date,ut=ut,Lon=Lon,Hemisphere=hem,Mag=Mag,
							Fill=Continents,Method=Method,color=Coasts)
			else:			
				ax = PolarAxis(maps=maps,eqlat=eqlat,ShowLatLines=ShowLatLines,
								ShowLonLines=ShowLonLines,Background=Background)

				PolarCoasts(ax,Date=Date,ut=ut,Lon=Lon,Hemisphere=hem,Mag=Mag,
							Fill=Continents,Method=Method,color=Coasts)
		else:
			ax = fig		



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
					Lon=False,Method='aacgm',Cart=True):

		from ..Plot.PolarAxis import PolarAxis
		from ..Plot.PolarCoasts import PolarCoasts
		from ..Plot.CartPolarAxis import CartPolarAxis
		from ..Plot.CartPolarCoasts import CartPolarCoasts
				
		#get date and time
		if Date is None:
			Date = Today()
		if ut is None:
			ut = Now()			

		#get the hemisphere
		if self.fov['glat'][0][0] > 0:
			hem = 'north'
		else:
			hem = 'south'

		#get the FOV
		lon,lat = self.GetFOV(Mag=Mag,GS=GS,Date=Date)
		
		if Cart:
			#convert to the appropriate coordinate system
			t,r = ConvertGeoCart(lon,lat,Date=Date,ut=ut,Mag=Mag,Lon=Lon,Method=Method,Hemisphere=hem)
		else:
			#convert to the appropriate coordinate system
			t,r = ConvertGeo(lon,lat,Date=Date,ut=ut,Mag=Mag,Lon=Lon,Method=Method)
					
			if self.fov['glat'][0][0] < 0:
				r = -r
			
		#create the axes
		if fig is None:
			if Cart:
				xrnge = [t.min()-5,t.max()+5]
				yrnge = [r.min()-5,r.max()+5]
				ax = CartPolarAxis(maps=maps,xrnge=xrnge,yrnge=yrnge,ShowLatLines=ShowLatLines,
								ShowLonLines=ShowLonLines,Background=Background)

				CartPolarCoasts(ax,Date=Date,ut=ut,Lon=Lon,Hemisphere=hem,Mag=Mag,
							Fill=Continents,Method=Method,color=Coasts)
			else:			
				ax = PolarAxis(maps=maps,eqlat=eqlat,ShowLatLines=ShowLatLines,
								ShowLonLines=ShowLonLines,Background=Background)

				PolarCoasts(ax,Date=Date,ut=ut,Lon=Lon,Hemisphere=hem,Mag=Mag,
							Fill=Continents,Method=Method,color=Coasts)
		else:
			ax = fig		



		#plot the cells
		nC = np.size(Beams)
		for i in range(0,nC):
			t00 = t[Beams[i],Gates[i]]
			r00 = r[Beams[i],Gates[i]]
			t10 = t[Beams[i]+1,Gates[i]]
			r10 = r[Beams[i]+1,Gates[i]]
			t01 = t[Beams[i],Gates[i]+1]
			r01 = r[Beams[i],Gates[i]+1]
			t11 = t[Beams[i]+1,Gates[i]+1]
			r11 = r[Beams[i]+1,Gates[i]+1]
			
			rp = [r00,r10,r11,r01,r00]
			tp = [t00,t10,t11,t01,t00]
			
			ax.plot(tp,rp,color=color,linewidth=linewidth)
			
		return ax
			
