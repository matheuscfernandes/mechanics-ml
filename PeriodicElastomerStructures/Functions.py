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

session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

def DeleteAbaqusFiles(Job):
	try:
		os.remove(Job+'.odb')
	except: pass
	
	try:
		os.remove(Job+'.dat')
	except: pass
	
	try:
		os.remove(Job+'.com')
	except: pass
	
	try:
		os.remove(Job+'.ipm')
	except: pass
	
	try:
		os.remove(Job+'.log')
	except: pass
	
	try:
		os.remove(Job+'.prt')
	except: pass
	
	try:
		os.remove(Job+'.sim')
	except: pass
	
	try:
		os.remove(Job+'.sta')
	except: pass
		
	try:
		os.remove(Job+'.msg')
	except: pass
	
	try:
		os.remove(Job+'.lck')
	except: pass

def DeleteAbaqusFilesButODB(Job):
	try:
		os.remove(Job+'.dat')
	except: pass
	
	try:
		os.remove(Job+'.com')
	except: pass
	
	try:
		os.remove(Job+'.ipm')
	except: pass
	
	try:
		os.remove(Job+'.log')
	except: pass
	
	try:
		os.remove(Job+'.prt')
	except: pass
	
	try:
		os.remove(Job+'.sim')
	except: pass
	
	try:
		os.remove(Job+'.sta')
	except: pass
		
	try:
		os.remove(Job+'.msg')
	except: pass
	
	try:
		os.remove(Job+'.lck')
	except: pass
				

def ExtractVirtualPointRF(instanceVP,stepName,nodeSetVP,JobName):
	odb=openOdb(path=JobName+'.odb')
	set = odb.rootAssembly.instances[instanceVP.upper()].nodeSets[nodeSetVP.upper()]
	
	Frame = odb.steps[stepName].frames[-1].frameValue
	RF1 = odb.steps[stepName].frames[-1].fieldOutputs['RF'].getSubset(region = set).values[0].data[0]
	RF2 = odb.steps[stepName].frames[-1].fieldOutputs['RF'].getSubset(region = set).values[0].data[1]
	
	odb.close()
	return Frame,RF1,RF2

def ExtractVirtualPointU(instancename,NameStep,setname,JobName):  
	odb=openOdb(path=JobName+'.odb')
	FrameLength=len(odb.steps[NameStep].frames)
	Frame=odb.steps[NameStep].frames[-1]
	Time=odb.steps[NameStep].frames[-1].frameValue
	set=odb.rootAssembly.instances[instancename.upper()].nodeSets[setname.upper()] 
	displacement=Frame.fieldOutputs['U'].getSubset(region=set).values
	
	xDisp=displacement[0].data[0]
	yDisp=displacement[0].data[1]

	odb.close()
	return Time,xDisp,yDisp
				

def ExtractEigenMode(JobName,NumberOfModes):
	odb=openOdb(path=JobName+'.odb')
	Freq=[]
	for i in xrange(1,NumberOfModes+1):
		Desc=odb.getFrame(i).description
		Desc=Desc.split("=");Freq.append(float(Desc[1]))
	odb.close()
	return Freq

def CreateEString(Number):
	string='%e'
	for i in xrange(1,Number):
		string+=' %e'
	string+='\r\n'
	return string

def PeriodicBound2D(mdb,NameModel,NameSet,LatticeVec):
    from part import TWO_D_PLANAR, DEFORMABLE_BODY
    #Create reference parts and assemble
    NameRef1='RefPoint-0'; NameRef2='RefPoint-1'
    mdb.models[NameModel].Part(dimensionality=TWO_D_PLANAR, name=NameRef1, type=
        DEFORMABLE_BODY)
    mdb.models[NameModel].parts[NameRef1].ReferencePoint(point=(0.0, 0.0, 0.0))
    mdb.models[NameModel].Part(dimensionality=TWO_D_PLANAR, name=NameRef2, type=
        DEFORMABLE_BODY)
    mdb.models[NameModel].parts[NameRef2].ReferencePoint(point=(0.0, 0.0, 0.0))
    mdb.models[NameModel].rootAssembly.Instance(dependent=ON, name=NameRef1, 
        part=mdb.models[NameModel].parts[NameRef1])
    mdb.models[NameModel].rootAssembly.Instance(dependent=ON, name=NameRef2, 
        part=mdb.models[NameModel].parts[NameRef2])

    #Create set of reference points
    mdb.models[NameModel].rootAssembly.Set(name=NameRef1, referencePoints=(
        mdb.models[NameModel].rootAssembly.instances[NameRef1].referencePoints[1],))
    mdb.models[NameModel].rootAssembly.Set(name=NameRef2, referencePoints=(
        mdb.models[NameModel].rootAssembly.instances[NameRef2].referencePoints[1],))

    #Get all nodes
    nodesAll=mdb.models[NameModel].rootAssembly.sets[NameSet].nodes
    nodesAllCoor=[]
    for nod in mdb.models[NameModel].rootAssembly.sets[NameSet].nodes:
	   nodesAllCoor.append(nod.coordinates)
    repConst=0
    #Find periodically located nodes and apply equation constraints
    ranNodes=range(0,len(nodesAll))	#Index array of nodes not used in equations constraint
    for repnod1 in xrange(0,len(nodesAll)):
    	stop=False			#Stop will become true when equation constraint is made between nodes
    	nod1=nodesAll[repnod1]		#Select Node 1 for possible equation constraint
    	Coor1=nodesAllCoor[repnod1]		#Coordinates of Node 1
    	for repnod2 in ranNodes:	#Loop over all available nodes
    	    nod2=nodesAll[repnod2]	#Select Node 2 for possible equation constraint
    	    Coor2=nodesAllCoor[repnod2]	#Coordinates of Node 2
    	    dx=Coor2[0]-Coor1[0]; dy=Coor2[1]-Coor1[1]	#X and Y Distance between nodes
    	    for comb in xrange(0,len(LatticeVec)):	#Check if nodes are located exactly the vector lattice apart
	    		if int(round(1000.0*(LatticeVec[comb][0]-dx)))==0:
	    		    if stop: break
	    		    elif int(round(1000.0*(LatticeVec[comb][1]-dy)))==0:
		    			#Correct combination found
		    			#Create sets for use in equations constraints
		    			mdb.models[NameModel].rootAssembly.Set(name='Node-1-'+str(repConst), nodes=
		    			    mdb.models[NameModel].rootAssembly.sets[NameSet].nodes[repnod1:repnod1+1])
		    			mdb.models[NameModel].rootAssembly.Set(name='Node-2-'+str(repConst), nodes=
		    			    mdb.models[NameModel].rootAssembly.sets[NameSet].nodes[repnod2:repnod2+1])
		    			#Create equations constraints for each dof
		    			for Dim1 in [1,2]:
		    			    mdb.models[NameModel].Equation(name='PerConst'+str(Dim1)+'-'+str(repConst),
			    				terms=((1.0,'Node-1-'+str(repConst), Dim1),(-1.0, 'Node-2-'+str(repConst), Dim1) ,
			    	   		        (dx, 'RefPoint-'+str(Dim1-1), 1),(dy, 'RefPoint-'+str(Dim1-1), 2)))
		    			mdb.models[NameModel].Equation(name='Rotation'+'-'+str(repConst), terms=(
   						    (1.0, 'Node-1-'+str(repConst), 6), 
        					(-1.0, 'Node-2-'+str(repConst), 6)))
		    			repConst=repConst+1	#Increase integer for naming equation constraint
		    			ranNodes.remove(repnod1)#Remove used node from available list
		    			stop=True		#Don't look further, go to following node.
		    			break
	
    #Return coordinates of free node so that it can be fixed
    return (NameRef1, NameRef2, repConst)

def UpdatePeriodicBound2D(mdb,NameModel,NameRef1,NameRef2,repConst):
	
	for j in xrange(0,repConst):
		Node1=mdb.models[NameModel].rootAssembly.sets['Node-1-'+str(j)].nodes[0].coordinates
		Node2=mdb.models[NameModel].rootAssembly.sets['Node-2-'+str(j)].nodes[0].coordinates
		dx=(Node2[0]-Node1[0]);dy=(Node2[1]-Node1[1])

		# for Dim1 in [1,2]:
		#     mdb.models[NameModel].constraints['PerConst'+str(Dim1)+'-'+str(j)].setValues(
		# 		terms=((1.0,'Node-1-'+str(j), Dim1),(-1.0, 'Node-2-'+str(j), Dim1) ,
	 #   		        (dx, 'RefPoint-'+str(Dim1-1), 1),(dy, 'RefPoint-'+str(Dim1-1), 2)))

		mdb.models[NameModel].constraints['PerConst1-'+str(j)].setValues(terms=((1.0, 
		    'Node-1-'+str(j), 1), (-1.0, 'Node-2-'+str(j), 1), (dx, NameRef1, 1), (dy, 
		    NameRef1, 2)))
		mdb.models[NameModel].constraints['PerConst2-'+str(j)].setValues(terms=((1.0, 
		    'Node-1-'+str(j), 2), (-1.0, 'Node-2-'+str(j), 2), (dx, NameRef2, 1), (dy, 
		    NameRef2, 2)))


def PeriodicBound2DXY(mdb,NameModel,NameSetTop,NameSetBottom,NameSetRight,NameSetLeft,LatticeVec):
	from part import TWO_D_PLANAR, DEFORMABLE_BODY
	
	TOL=0.001 
	
	#Create reference parts and assemble
	NameRef1='RefPoint-0'; NameRef2='RefPoint-1'
	mdb.models[NameModel].Part(dimensionality=TWO_D_PLANAR, name=NameRef1, type=
		DEFORMABLE_BODY)
	mdb.models[NameModel].parts[NameRef1].ReferencePoint(point=(0.0, 0.0, 0.0))
	mdb.models[NameModel].Part(dimensionality=TWO_D_PLANAR, name=NameRef2, type=
		DEFORMABLE_BODY)
	mdb.models[NameModel].parts[NameRef2].ReferencePoint(point=(0.0, 0.0, 0.0))
	mdb.models[NameModel].rootAssembly.Instance(dependent=ON, name=NameRef1, 
		part=mdb.models[NameModel].parts[NameRef1])
	mdb.models[NameModel].rootAssembly.Instance(dependent=ON, name=NameRef2, 
		part=mdb.models[NameModel].parts[NameRef2])

	#Create set of reference points
	mdb.models[NameModel].rootAssembly.Set(name=NameRef1, referencePoints=(
		mdb.models[NameModel].rootAssembly.instances[NameRef1].referencePoints[1],))
	mdb.models[NameModel].rootAssembly.Set(name=NameRef2, referencePoints=(
		mdb.models[NameModel].rootAssembly.instances[NameRef2].referencePoints[1],))

	#Get all nodes NameSet
	nodesTop=mdb.models[NameModel].rootAssembly.sets[NameSetTop].nodes
	nodesBottom=mdb.models[NameModel].rootAssembly.sets[NameSetBottom].nodes
	nodesRight=mdb.models[NameModel].rootAssembly.sets[NameSetRight].nodes
	nodesLeft=mdb.models[NameModel].rootAssembly.sets[NameSetLeft].nodes
	
	ranNodesRight=range(0,len(mdb.models[NameModel].rootAssembly.sets[NameSetRight].nodes))
	ind1=1
	for i in range(0,len(mdb.models[NameModel].rootAssembly.sets[NameSetLeft].nodes)):
		LeftCoordinate = mdb.models[NameModel].rootAssembly.sets[NameSetLeft].nodes[i].coordinates
		mdb.models[NameModel].rootAssembly.Set(name='Node-Left-'+str(ind1), nodes=
			mdb.models[NameModel].rootAssembly.sets[NameSetLeft].nodes[i:i+1])
		for j in ranNodesRight:
			RightCoordinate = mdb.models[NameModel].rootAssembly.sets[NameSetRight].nodes[j].coordinates
			if (fabs(fabs(LeftCoordinate[0]-RightCoordinate[0])-LatticeVec[0][0]) < TOL and 
				fabs(LeftCoordinate[1]-RightCoordinate[1]) < TOL):
				mdb.models[NameModel].rootAssembly.Set(name='Node-Right-'+str(ind1), nodes=
					mdb.models[NameModel].rootAssembly.sets[NameSetRight].nodes[j:j+1])
				mdb.models[NameModel].Equation(name='LR-X'+'-'+str(ind1),
					terms=((1.0,'Node-Left-'+str(ind1), 1),(-1.0, 'Node-Right-'+str(ind1), 1) ,
					(1.0, NameRef1, 1)))
				mdb.models[NameModel].Equation(name='LR-Y'+'-'+str(ind1),
					terms=((1.0,'Node-Left-'+str(ind1), 2),(-1.0, 'Node-Right-'+str(ind1), 2) ,
					(1.0, NameRef1, 2)))
				# mdb.models[NameModel].Equation(name='LR-RZ'+'-'+str(ind1),
				# 	terms=((1.0,'Node-Left-'+str(ind1), 6),(-1.0, 'Node-Right-'+str(ind1), 6)))
				ind1=ind1+1
				break
	
	ranNodesBottom=range(0,len(mdb.models[NameModel].rootAssembly.sets[NameSetBottom].nodes))
	ind2=1
	for i in range(0,len(mdb.models[NameModel].rootAssembly.sets[NameSetTop].nodes)):
		TopCoordinate = mdb.models[NameModel].rootAssembly.sets[NameSetTop].nodes[i].coordinates
		if (fabs(TopCoordinate[0])> TOL): #and fabs(TopCoordinate[0]-LatticeVec[0][0])> TOL):
			mdb.models[NameModel].rootAssembly.Set(name='Node-Top-'+str(ind2), nodes=
				mdb.models[NameModel].rootAssembly.sets[NameSetTop].nodes[i:i+1])
			for j in ranNodesBottom:
				BottomCoordinate = mdb.models[NameModel].rootAssembly.sets[NameSetBottom].nodes[j].coordinates
				if (fabs(sqrt((TopCoordinate[1]-BottomCoordinate[1])**2)-LatticeVec[1][1]) < TOL and 
					fabs(TopCoordinate[0]-BottomCoordinate[0]) < TOL):
					mdb.models[NameModel].rootAssembly.Set(name='Node-Bottom-'+str(ind2), nodes=
						mdb.models[NameModel].rootAssembly.sets[NameSetBottom].nodes[j:j+1])
					mdb.models[NameModel].Equation(name='TB-X'+'-'+str(ind2),
						terms=((1.0,'Node-Top-'+str(ind2), 1),(-1.0, 'Node-Bottom-'+str(ind2), 1) ,
						(-1.0, NameRef2, 1)))
					mdb.models[NameModel].Equation(name='TB-Y'+'-'+str(ind2),
						terms=((1.0,'Node-Top-'+str(ind2), 2),(-1.0, 'Node-Bottom-'+str(ind2), 2) ,
						(-1.0, NameRef2, 2)))
					# mdb.models[NameModel].Equation(name='TB-RZ'+'-'+str(ind2),
					# 	terms=((1.0,'Node-Top-'+str(ind2), 6),(-1.0, 'Node-Bottom-'+str(ind2), 6)))
					ind2=ind2+1
					break
	
	return (NameRef1, NameRef2)