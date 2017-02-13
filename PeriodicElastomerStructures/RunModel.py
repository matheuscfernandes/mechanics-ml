'''
Created by: Miguel Bessa & Matheus Fernandes

California Institute of Technology
Harvard University

Note: This code contains the generation of arbitrary geometry specifically using ABAQUS 12.1-1 

'''

### MODEL PARAMETERS ###
NUMBER_OF_POINTS=100 # NUMBER OF POINTS TO GENERATE THE CENTER HOLE THROUGH THE PARAMETRIC FUNCTION
RO=
C1=
C2=
DOMAIN_SIZE=10.

### BEGIN RUNNING MODEL BY IMPORTING ABAQUS 12.1-1 FUNCTIONS ###
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

### GENERATING PART GEOMETRY ###
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-30.0, 26.25), 
    point2=(26.25, -22.5))
mdb.models['Model-1'].Part(dimensionality=TWO_D_PLANAR, name='Part-1', type=
    DEFORMABLE_BODY)


### GENERATING INNER SHAPE OF THE GEOMETRY ###

THETA=np.linspace(0,2*pi*0.99,NUMBER_OF_POINTS)

rr=RO*(1.+C1*cos(4*THETA)+C2*cos(8*THETA))

XCoor=rr*cos(THETA);YCoor=rr*sin(THETA)

mdb.models['Model-1'].sketches['__profile__'].Spline(points=((-7.5, 2.5), (-3.75, 
    7.5), (5.0, 6.25), (7.5, -1.25), (3.75, -6.25), (-1.25, -7.5), (-6.25, 
    -5.0), (-7.5, 2.5)))


mdb.models['Model-1'].parts['Part-1'].BaseShell(sketch=
    mdb.models['Model-1'].sketches['__profile__'])


del mdb.models['Model-1'].sketches['__profile__']