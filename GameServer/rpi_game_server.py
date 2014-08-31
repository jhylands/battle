'''
Created on 7 Aug 2014

@author: Lilian
'''
#!/usr/bin/python # This is server.py file
import socket # Import socket module
import time
import threading

import const
#from battleships_gui import BattleshipsGraphics
from player_socket import PlayerSocket

##########################################
##           PARAMETERS SETTING         ##
##########################################

sizeFleet = 21 # the number of square covered by the fleet

# Check whether the fleet is sunk 
def checkWinner(board):
    # We just need to test whether the number of hits equals the total number of squares in the fleet
    hits = 0
    for i in range(12):
        hits += board[i].count(4)
    return hits==sizeFleet

def giveOutcome(player_board, i1, i2):
    """
    Check the board to see if the move is a hit or a miss.
    Return the value const.HIT or const.MISSED
    """
    if ((player_board[i1][i2]==const.OCCUPIED)
        or (player_board[i1][i2]==const.HIT)):
        # They may (stupidly) hit the same square twice so we check for occupied or hit
        player_board[i1][i2]=const.HIT
        result =const.HIT
    else:
        result = const.MISSED
    return result


def playMatch(firstPlayer, secondPlayer, rounds):
    """
    function handling a match between two players. Each match may be composed of several games/rounds.
    @param <BattleshipsGraphics> gui, the graphic interface displaying the match.
    @param <PlayerSocket> firstPlayer, secondPlayer: The player objects 
    """
    firstPlayer.newPlayer(secondPlayer.getName())
    secondPlayer.newPlayer(firstPlayer.getName())
    scorePlayer1 = scorePlayer2 = 0
    for game in range(rounds):
        firstPlayer.newRound()
        secondPlayer.newRound()
        #gui.turtle.clear()
        #gui.drawBoards()
        #gui.drawPlayer(firstPlayer.getName(), firstPlayer.getDescription(), 'left')
        #gui.drawPlayer(secondPlayer.getName(), secondPlayer.getDescription(), 'right')
        #gui.drawScore (scorePlayer1, scorePlayer2)
        turn = (-1)**game


        p1, p2 = playGame(firstPlayer, secondPlayer, turn)
         
        scorePlayer1 += p1
        scorePlayer2 += p2
        #gui.drawScore (scorePlayer1, scorePlayer2)
    
    if scorePlayer2 > scorePlayer1 :
	print 'right is the winner'
        #gui.drawWinner('right')
    elif scorePlayer2 == scorePlayer1:
        pass
    else:
	print 'Left is the winner'
        #gui.drawWinner('left')
    
    print "---------------- ",firstPlayer.getName(), scorePlayer1,"-",
    print scorePlayer2, secondPlayer.getName(), "----------------"
    return (scorePlayer1, scorePlayer2)

def playGame( firstPlayer, secondPlayer, turn):
    """
    function handling a game between two players (e.g. one single round).
    @param <BattleshipsGraphics> gui, the graphic interface displaying a round.
    @param <PlayerSocket> firstPlayer, secondPlayer: The player objects.
    @param <int> turn: parameter indicating who is starting the game. 
    if turn == 1 then firstPlayer starts, else if turn == -1 then secondPlayer starts.
    """
    
    # Distribute the fleet onto each player board
    player1_board = firstPlayer.deployFleet()

    for row in range(len(player1_board)):
        for col in range(len(player1_board[row])):
            if player1_board[row][col] == const.OCCUPIED:
		print 'right boats'
                #gui.drawBoat('right', row, col)
            
    player2_board = secondPlayer.deployFleet()

    for row in range(len(player2_board)):
        for col in range(len(player2_board[row])):
            if player2_board[row][col] == const.OCCUPIED:
                #gui.drawBoat('left', row, col)
		print 'left boats'
    
    

    haveWinner = False
    shots = 1
    while not haveWinner:
        if turn > 0:
            i1,i2 = firstPlayer.chooseMove()
            outcome = giveOutcome(player2_board, i1, i2)
            if outcome == const.HIT:
		print 'left hit at' + str(i1) + ':' + str(i2)
                #gui.drawHit('left', i1, i2)
            else:
		print 'left miss at' + str(i1) + ':' + str(i2) 
                #gui.drawMiss('left', i1, i2)
                 
            firstPlayer.setOutcome(outcome, i1, i2)
            secondPlayer.getOpponentMove(i1, i2)

            turn *= -1
            shots += 1
            haveWinner = checkWinner(player2_board)
 
        else:
            i1,i2 = secondPlayer.chooseMove()
            outcome = giveOutcome(player1_board, i1, i2)
            if outcome == const.HIT:
		print 'right hit at' + str(i1) + ':' + str(i2)
                #gui.drawHit('right', i1, i2)
            else:
		print 'right miss at' + str(i1) + ':' + str(i2)
                #gui.drawMiss('right', i1, i2)
                
            secondPlayer.setOutcome(outcome, i1, i2)
            firstPlayer.getOpponentMove(i1, i2)
        
            turn *= -1
            haveWinner = checkWinner(player1_board)
             
         
    winner = "Player 1"
    if turn > 0 :
        winner = "Player 2"
        result = (0,1)
    else:
        result = (1,0)
        

    print "---------------- " + winner + "is the winner in " + str(shots) + "shots ----------------"
    time.sleep(2)
    
    return result



# Main

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Create a socket object
sock.bind((const.GAME_SERVER_ADDR, const.GAME_SERVER_PORT)) # The same port as used by the server & clients

while True:
    incorrectPin = True
    while incorrectPin:
	sock.listen(1)                                              # Now wait for client connection (max of 2 client at a time).
	client1, addr1 = sock.accept()                          # Establish connection with first client.
	print 'Got connection from', addr1
	tempPlayer = PlayerSocket(client1, addr1)
	if tempPlayer.getPin() == const.PIN:
	    incorrectPin = False                  # Check player has correct pin
	    player1 = tempPlayer              # Create first player with that connection
	    player1.acknowledgeConnection()
	    print "player",player1.getName(),"is connected..."    
    incorrectPin = True
    while incorrectPin:
	sock.listen(1)                                              # Now wait for client connection (max of 2 client at a time).
	client1, addr1 = sock.accept()                          # Establish connection with first client.
	print 'Got connection from', addr1
	tempPlayer = PlayerSocket(client1, addr1)
	if tempPlayer.getPin() == const.PIN:
	    incorrectPin = False                  # Check player has correct pin
	    player2 = tempPlayer              # Create first player with that connection
	    player2.acknowledgeConnection()
	    print "player",player2.getName(),"is connected..."    
 
    #gui = BattleshipsGraphics(const.GRID_SIZE)
    try:
	    playMatch(player1, player2, 5)
	    player1.close()                                         # Close the connection
	    player2.close()                                         # Close the connection
    
    except:
	    player1.close()                                         # Close the connection
	    player2.close()                                         # Close the connection

    break                                                   # End of game, exit game loop


## Must be the last line of code 
#gui.screen.exitonclick()



