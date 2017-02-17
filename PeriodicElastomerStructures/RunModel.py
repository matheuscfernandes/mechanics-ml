'''
Created by: Miguel Bessa & Matheus Fernandes

California Institute of Technology
Harvard University

Note: This code contains the generation of arbitrary geometry specifically using ABAQUS 12.1-1 

'''

### MODEL PARAMETERS ###
NUMBER_OF_POINTS=100 # NUMBER OF POINTS TO GENERATE THE CENTER HOLE THROUGH THE PARAMETRIC FUNCTION
RO=1
C1=.1
C2=.2
DOMAIN_SIZE=3.5

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

### GENERATING INNER SHAPE OF THE GEOMETRY ###

THETAALL=np.linspace(0,2*pi,NUMBER_OF_POINTS)
POINTS=[]
for i in xrange(NUMBER_OF_POINTS):
    THETA=THETAALL[i]
    rr=RO*(1.+C1*cos(4*THETA)+C2*cos(8*THETA))
    POINTS.append((rr*cos(THETA),rr*sin(THETA)))
    if i==0: xFirst=rr*cos(THETA);yFirst=rr*sin(THETA)
    if i==NUMBER_OF_POINTS-1: POINTS.append((xFirst,yFirst))

### GENERATING PART GEOMETRY ###
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].Part(dimensionality=TWO_D_PLANAR, name='Part-1', type=
    DEFORMABLE_BODY)

mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-DOMAIN_SIZE/2., -DOMAIN_SIZE/2.), 
    point2=(DOMAIN_SIZE/2., DOMAIN_SIZE/2.))
mdb.models['Model-1'].sketches['__profile__'].Spline(points=POINTS)


mdb.models['Model-1'].parts['Part-1'].BaseShell(sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

#PART DEFINITION
Part_Full=mdb.models['Model-1'].parts['Part-1']


### CREATING ASSEMBLY ###
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
#INSTANCE DEFINITION
Instace_Full=mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-1', 
	part=Part_Full)


### SEEDING MODEL AND GENERATING MESH ###
Part_Full.seedPart(deviationFactor=0.1,	minSizeFactor=0.1, size=0.1)
Part_Full.setMeshControls(elemShape=QUAD, regions=Part_Full.faces[:])
Part_Full.Set(name='ALL',faces=Part_Full.faces)
Part_Full.setElementType(elemTypes=(ElemType(
    elemCode=CPE8R, elemLibrary=STANDARD), ElemType(elemCode=CPE6M, 
    elemLibrary=STANDARD)), regions=Part_Full.sets['ALL'])

mdb.models['Model-1'].parts['Part-1'].generateMesh()

### CREATING STEPS ###

### CREATING SETS ###


### DEFINING MATERIAL PROPERTIES AND SECTION PROPERTIES ###