#import math for rotations
import math
#TRANSFORMATION FUNCTIONs----------------------------------------------------------------
#add vectors A and B
def addVector(A,B):
    return {'x':A['x']+B['x'],'y':A['y']+B['y']}
#takes B from A
def takeBFromA(A,B):
	return addVector(A,{'x':(-1 * B['x']),'y':(-1 * B['y'])})
#carry out a rotation in euclidian space
def rotate(coordinates,angle):
    #get the coordinates to local variables so its easyer to see whats going on
    x = coordinates['x']
    y = coordinates['y']
    X = round(x * math.cos(angle) - y * math.sin(angle))
    Y = round(x * math.sin(angle) + y * math.cos(angle))
    return {'x':X,'y':Y}
#converting from battleship coordinate system to normal one with origin 11,0 in battle ship coordinates
def ZtoW(coordinates):
    u = coordinates['y']
    v = -coordinates['x']
    return {'x': u ,'y': v }
#a function such that WtoZ(ZtoW(coordinates)) = coordinates
def WtoZ(coordinates):
    u = -coordinates['y']
    v = coordinates['x']
    return {'x':u,'y':v}
#carry out a rotation in battleship space
def doRotation(coordinates,angle):
    return WtoZ(rotate(ZtoW(coordinates),angle))
#-----------------------------------------------------------------------------------------------
