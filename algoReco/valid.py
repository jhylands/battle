import math

def rotate(coordinates,angle):
    x = coordinates['x']
    y = coordinates['y']
    Xn = x*math.cos(angle) - y * math.sin(angle)
    Yn = x*math.sin(angle) + y * math.cos(angle)
    return {'x': Xn , 'y': Yn}

AircraftCarrior = [{'x':0,'y':0},{'x':0,'y':-1},{'x':0,'y':-2},{'x':0,'y':-3},{'x':-1,'y':-3},{'x':1,'y':-3}]
for pannal in AircraftCarrior:
    print rotate(pannal,(math.pi*3/2))
print rotate({'x': 1, 'y': -3},4.71)
