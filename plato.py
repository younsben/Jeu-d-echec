import numpy as np

def update_plateau(chang):
#this function is dedicated to the changement during the game
# put here if the move is legal,
    if legal_move(chang):
        return chang
def begining_plate():
#This function create the game board
    board = np.full((8,8),"Vide")
    piece =np.array(["Rook","Knight","Bishop","Queen","King","Bishop","Knight","Rook"])
    board[0] = [ "w" + p for p in piece]
    board[1] = "wPawn"
    board[7] = [ "b" + p for p in piece]
    board[6] = "bPawn"
    return board

print(begining_plate())

def legal_move(chang):
# return True if the move is legit and False else, it means:
# if the piece can ordinary do the move
# if my king is in check and stay in check after the moove
#  or if my king will be in check after the moove
    return True