#fucntion to create an array of posible rotation configerations for the ships
def addRotaty(ships,mainList = [],CountingList = []):
    #pop ship from array for use on this recusion level
    ship = ships.pop()
    #get the number of rotations for this ship
    rotations = shipRotations[ship['ship']]
    #loop through each rotation
    for x in range(0,rotations):
	#add this rotation to the counting list
        countingList.append(x)
	#if we don't need to go any deeper add the counting array as an element of the main list
	if len(ships) ==0:
	    mainList.append(countingList)
	else:
	    #otherwise recure deeper updating mainlist
	    mainList = addRotary(mainList,countinglist)
	#remove this loops countingList contribution so next loop can take its place
	countingList.pop()
    #return the mainlist
    return mainList


#shipList is a list of the ships to use in current test
#hitList is a list of hits in blob that must be covered
#NotList is a list of ships not to be used in futher loops
def recursion(hitList,shipList = None, missList = None, Notlist = None, n = None):
    #if not shipList provided set it as empty array
    if shipList == None:
	shipList = []
    #if no misses have been reported (lucky first shot) then inishiate missList as empty array
    if missList == None:
	missList = []
    #if no notlist provided as parameter then set is as empty array
    if Notlist == None:
	Notlist = []
    #if n not provided take 5 a defualt
    if n == None:
	n=5

    #inisiate list of valid combinations
    validList=[]

    #loop through ships
    for i in range(0,n):
	#but not ships already in use as each ship can only appear once
	if not i in NotList:
	    #check for possibles using the ship proposed by current value of i in the loop and the other ships added in higher branches of the recursion
	    shipList.append(i)#add current ship to shipList
     	    validList += test(shipList,hitList,MissList)

	    #if there are more hits then we have ships, look at possibilities that use more ships
	    if len(hitList)>len(NotList):
		#for futher recurtions remove i (the current ship represented by I) from the loops
	        NotList.append(i)
		#use more ships in check
 		ValidList += recursion(hitList,missList, shipList,Notlist,n)
		#remove this ship from notlist as i is about to change to a new value
	        Notlist.pop()
	    #remove i from shipList as i is about to change
	    shipList.pop()
    return validList

#place the ships on the blobs
def BlobSelection(shipList,hitList,missList,shipPlace = None):
    #define an empty valid list
    validList = []
    if shipPlace == None:
	shipPlace = []
    if len(shipList) == 0:
	#all ships assigned a place
	#get them each a rotation
	
    else:
	for place in hitList:
	    shipPlace.append({'ship':shipList.pop(),'x':place['x'],'y' : place['y']})
	    #add the recursive valid options to the valid list
	    validList += BlobSelection(shipList, hitList, missList, shipPlace)
    return validList


#fucntion to create an array of posible rotation configerations for the ships
def addPannels(ships,mainList = [],CountingList = []):
    #pop ship from array for use on this recusion level
    ship = ships.pop()
    #get the number of rotations for this ship
    pannels = len(Globalships[ship['ship']])
    #loop through each rotation
    for x in range(0,rotations):
	#add this rotation to the counting list
        countingList.append(x)
	#if we don't need to go any deeper add the counting array as an element of the main list
	if len(ships) ==0:
	    mainList.append(countingList)
	else:
	    #otherwise recure deeper updating mainlist
	    mainList = addPannels(mainList,countinglist)
	#remove this loops countingList contribution so next loop can take its place
	countingList.pop()
    #return the mainlist
    return mainList
