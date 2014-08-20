'''
This module handle the client side of the client/server communication of the game.
It calls the functions defined in the Player_strategy module and send the output/input 
information needed by the server.

Created on 7 Aug 2014

@author: Lilian
'''


import socket # Import socket module
import player_strategy as player
import const
from battleships_client_gui import BattleshipsGraphics


def main(gui):
    game_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
    if const.GAME_SERVER_ADDR == '':        
        host = socket.gethostname() # Get local machine name
	print host
        game_server.connect((host, const.GAME_SERVER_PORT))
    else:
        game_server.connect((const.GAME_SERVER_ADDR, const.GAME_SERVER_PORT))
        
    status = game_server.recv(1024)
    game_server.send(const.ACKNOWLEDGED)    # used for client/server synchronisation purpose
    print status
    
    if status == "connected":
        while True:
            request = game_server.recv(1024)
            print "template rqt:", request, "|"
            request = eval(request)
            
            if request[0] == "deployFleet":
                player_board = player.deployFleet()
                for row in range(len(player_board)):
                    for col in range(len(player_board[row])):
                        if player_board[row][col] == const.OCCUPIED:
                            gui.drawBoat('left', row, col)
                game_server.send(str(player_board))

            elif request[0] == "getName":
                game_server.send(str(player.playerName))
                
            elif request[0] == "newPlayer":
                player.newPlayer()
                game_server.send(const.ACKNOWLEDGED)    # used for client/server synchronisation purpose
                
            elif request[0] == "newRound":
                gui.turtle.clear()
                gui.drawBoards()
                gui.drawPlayer(player.playerName, '', 'left')
                gui.drawPlayer('Opponent', '', 'right')
                player.newRound()
                game_server.send(const.ACKNOWLEDGED)    # used for client/server synchronisation purpose
                
            elif request[0] == "getDescription":
                game_server.send(str(player.playerDescription))
                
            elif request[0] == "chooseMove":
                game_server.send(str(player.chooseMove()))
                
            elif request[0] == "setOutcome":
                player.setOutcome(request[1], request[2], request[3])
                if request[1] == const.HIT:
                    gui.drawHit('right', request[2], request[3])
                else:
                    gui.drawMiss('right', request[2], request[3])
                game_server.send(const.ACKNOWLEDGED)    # used for client/server synchronisation purpose
                
            elif request[0] == "getOpponentMove":
                result = player.getOpponentMove(request[1], request[2])
                if result == const.HIT:
                    gui.drawHit('left', request[1], request[2])
                else:
                    gui.drawMiss('left', request[1], request[2])
                                        
                game_server.send(const.ACKNOWLEDGED)    # used for client/server synchronisation purpose
                
            else:
                # unknown request so must be either end of game or a fatal error. Exit the game loop
                print request
                game_server.send(const.ACKNOWLEDGED)    # used for client/server synchronisation purpose
                break
            

    game_server.close # Close the socket when done


gui = BattleshipsGraphics(const.GRID_SIZE) # The graphics for the game
        
main(gui)

## Must be the last line of code 
gui.screen.exitonclick()
