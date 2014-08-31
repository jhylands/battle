UNKOWN = 0
EMPTY = 1
OCCUPIED = 2
MISSED = 3
HIT = 4

MISSED_GIF = "images/missed.gif"
HIT_GIF = "images/hit.gif"
WINNER_GIF = "images/winner.gif"
LOOSER_GIF = "images/looser.gif"
BOARD_BKG_GIF = "images/boardBKG.gif"


CARRIER = 10
HOVERCRAFT = 11
BATTLESHIP = 12
CRUISER = 13
DESTROYER = 14

ROUNDS = 3    ## Number of rounds per match
GRID_SIZE = 12 ## size of the board


GAME_FLEET = ["Carrier", "Hovercraft", "Battleship", "Cruiser", "Destroyer"]


############################################################
##
## Constants used for the client/server functionalities
##
############################################################
# Constant containing the IP address of the server
GAME_SERVER_ADDR = ''   #meaning the server is on the local host. Comment if server is elsewhere and provide
                        # an address like the one below
# GAME_SERVER_ADDR = '10.240.74.225' 
 
# Port used for the socket communication. You must ensure the same port is used by the client & the server
# Note: another port number could be used
GAME_SERVER_PORT = 12345 

# Constant used in the communication to acknowledge a received message
# Typically this constant is used to synchronise the clients and the server
ACKNOWLEDGED = 'ACK'
