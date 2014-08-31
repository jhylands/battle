import math

def rotate(coordinates,angle):
    x = coordinates['x']
    y = coordinates['y']
    Xn = x*int(math.cos(angle)) - y * int(math.cos(angle))
    Yn = x*int(math.sin(angle)) + y * int(math.cos(angle))
    return {'x': Xn , 'y': Yn}
AircraftCarrior = [{'x':0,'y':0},{'x':0,'y':-1},{'x':0,'y':-2},{'x':0,'y':-3},{'x':-1,'y':-3},{'x':1,'y':-3}]
for pannal in AircraftCarrior:
    print rotate(pannal,(math.pi*3/2))
