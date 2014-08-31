'''
Created on 7 Aug 2014

@author: Lilian
'''
class PlayerSocket(object):
    """
    class used for calling functions from the client player. This represents the communication protocol between 
    server and client. To synchronise the client and the server, requests from the server expect a reply from 
    the client.
    """
    
    def __init__(self, playerSocket, playerAddress):
        self._socket = playerSocket
        self._addr = playerAddress
        
    def acknowledgeConnection(self):
        self._socket.send("connected")
        return self._socket.recv(1024) # used for client/server synchronisation purpose
        
    def newPlayer(self, name):
        self._socket.send("('newPlayer', '" + name + "')")
        return self._socket.recv(1024)
        
   
    def newRound(self):
        self._socket.send("('newRound', None)")
        return self._socket.recv(1024)
    
    def getName(self):
        self._socket.send("('getName', None)")
        return self._socket.recv(1024)

    def getDescription(self):
        self._socket.send("('getDescription', None)")
        return self._socket.recv(1024)
    
    def deployFleet(self):
        self._socket.send("('deployFleet', None)")
        return eval(self._socket.recv(1024))
    
    def chooseMove(self):
        self._socket.send("('chooseMove', None)")
        return eval(self._socket.recv(1024))
    
    def setOutcome(self, outcome, row, col):
        self._socket.send("('setOutcome', "+str(outcome)+","+str(row)+", "+str(col)+")")
        return self._socket.recv(1024)
     
    def getOpponentMove(self, row, col):
        self._socket.send("('getOpponentMove', "+str(row)+", "+str(col)+")")
        return self._socket.recv(1024)
            
    def close(self):
        self._socket.send("('GameOver', None)")
        print self._socket.recv(1024) # used for client/server synchronisation purpose
        self._socket.close()
        
    def getPin(self):
	self._socket.send("('pin', None)")
	return self._socket.recv(1024)
