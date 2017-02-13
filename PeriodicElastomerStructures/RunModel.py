Mdb()
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import numpy as np
import math
import time

session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

execfile('Functions.py')

mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-30.0, 26.25), 
    point2=(26.25, -22.5))
mdb.models['Model-1'].Part(dimensionality=TWO_D_PLANAR, name='Part-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].sketches['__profile__'].Spline(points=((-7.5, 2.5), (-3.75, 
    7.5), (5.0, 6.25), (7.5, -1.25), (3.75, -6.25), (-1.25, -7.5), (-6.25, 
    -5.0), (-7.5, 2.5)))


mdb.models['Model-1'].parts['Part-1'].BaseShell(sketch=
    mdb.models['Model-1'].sketches['__profile__'])


del mdb.models['Model-1'].sketches['__profile__']