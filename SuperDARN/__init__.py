__version__ = '0.1.0'


from . import Globals
from . import Hardware
from . import Data
from . import Tools 
from . import FOV
from . import Plot

Hardware.LoadHDW()
if len(Globals.FOV) == 0:
	FOV.PopulateFOV()
