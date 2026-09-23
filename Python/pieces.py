import numpy as np

from abc import ABC

class Pieces():
    def __init__(self , position , name , points = 0 , inlife = True , already_moved = False):
        self.color = name[0]
        self.position = position # emplacement is an array of 2 int, where the first value is the horizontal position and the second one the vertical position
        self.name = name
        self.points = points
    def can_eat_piece(self , piece , board):
        pass
    def eat_piece(self, piece , board):
        pass
    def same_color(self,piece_same):
        if self.color == piece_same.color:
            return True
        return False

#direction : (-1/1,0) -> vert move, (0,1)->hor, (1,1)etc.. diago
    def get_sliding_moves(self , board , direction):
        moves =[]
        [vert,hor] = self.position
        (dver , dhor) = direction
        vert , hor = vert + dver , hor + dhor
        while (8 > vert > -1) and (8 > hor > -1)  and board[vert][hor].name == "Em" :
            moves.append([vert, hor])
            vert , hor = vert + dver , hor + dhor
        return moves


# vertical movement return a list with all of the possible move on the vertical road
    def vertical_movement(self , board ):
        return self.get_sliding_moves( board , (1,0)) + self.get_sliding_moves( board , (-1,0))

# horizontal movement return a list with all of the possible move on the vertical road
    def horizontal_movement(self , board):
            return self.get_sliding_moves( board , (0,1)) + self.get_sliding_moves( board , (0,-1))


    def diago_movement(self , board):
        moves = []
        for i in [-1,1]:
            for j in [-1,1]:
                moves = moves + self.get_sliding_moves( board , (i,j))       
        return moves

#thanks gemini I did 3 last code in 5lines instead of 30 lines for the last by implementeing a new function "get_sliding_moves"

   

    def the_L_eatable(self , board): #knight
        moves = [] 
        [vert , hor] = self.position 
        jumps = [( -2 , -1 ) , ( -2 , 1 )  , ( -1 , -2 ) ,( -1 , 2 ) , ( 1 , -2 ) , ( 1 , 2 ) , ( 2 , -1 ) , ( 2 , 1 ) ]
        for k in jumps :
            dver , dhor = k 
            new_vert = vert + dver
            new_hor = hor + dhor
            if (8 > new_vert > -1) and (8 > new_hor > -1)  and not(self.same_color(board[new_vert][new_hor])) :
                moves.append([new_vert, new_hor])
        return moves

    
         
class Pawn(Pieces):
    def pawn_advancement(self , board):
            [vert , hor] = self.position
            moves = []
            vert_index = vert + 1 
            if vert != 7:
                if board[vert_index , hor] == ["Em"] :
                    moves.append([vert_index , hor])
                    vert_index += 1
                    if not(self.already_moved) and board[vert_index , hor] == ["Em"] :
                        moves.append([ vert_index , hor ])
            else :
                if board[vert_index , hor] == ["Em"] or self.pawn_eatable(board) :
                    self.promotion()
            return moves
        
    def promotion(self):
        pass
    
    def pawn_eating(self , board):
        [vert , hor] = self.position
        moves = []
        new_vert = vert + 1
        new_hor = hor
        if new_vert != 7:
            for p in [-1 , 1] :
                if (8 > new_hor > -1) and board:
                    pass

    def pawn_eatable(self , board):
        [vert , hor] = self.position
        vert_index = vert + 1 
        if not(self.same_color(board[vert_index , hor+1])) or not(self.same_color(board[vert_index , hor-1])) :
            return True
        return False

class King(Pieces):
    def king_moves(self , board):
        moves = []
        [vert , hor] = self.position 
        new_vert = vert 
        new_hor = hor
        for i in [-1 , 0, 1]:
            new_vert += i
            if 8 > new_vert > -1:
                for j in [-1,0,1]:
                    new_hor += j
                    if not(self.same_color(board[new_vert , new_hor])) and 8 > new_hor > -1 :
                        moves.append([new_vert , new_hor])
                    new_hor = hor
            new_vert = vert
        return moves


#a function that verify if the list is empty or not
    def fun_eat(self , board ) : #put a function on the enter of function
        pass


    def piece_being_eatable(self , board):
        v = self. vertical_movement(board) 
        h = self. vertical_movement(board)
        d = self. vertical_movement(board)
        lmove = self. vertical_movement(board)
        if self.king_moves(board) == [] and lmove == []:
                return False
        if v != [] :
            for p in v :
                if self.same_color(p) and (p.name == "Q" or p.name == "R"):
                    return True
            for p in h :
                if self.same_color(p) and (p.name == "Q" or p.name == "R"):
                    return True
    
    # check if the color on the enter is check or not
    # to do it we will look at the king and see him like other pieces to see if anyone could eat him
    def check(self, board , my_color):
        for p in board :
            if self.name == "K" and self.same_color(my_color) :
                    pass
        pass
# THE NEXT TIME, TEST THE FUNCTION ask to gemini to create test boards and test pieces:


#add a super and instead of the name put the 'real name' like queen instead of Q
"""  def __str__(self):
        return "From str method of Test: name is %s" % (self.name)"""
#for the move add the capture of the opponent , if not same color
# verify the check only if a piece could eat the king not always if there is a chack mat

class Empty(Pieces):
    pass


class Board:
    def __init__(self ):
        tab = np.full((8,8),"Em") #E is for an empty case
        first_line = np.array(["R","N","B","Q","K","B","K","R"])
        tab[0] = [ "w" + p for p in first_line]
        tab[1] = "wP"
        tab[7] = [ "b" + p for p in first_line]
        tab[6] = "bP"
        empt = Pieces([0,0] , "empt")
        self.board = np.full((8,8), empt, dtype = Pieces)
        for i in range(8):
            for j in range(8):
                self.board[i][j] = Pieces([i,j] , tab[i][j])


    def display(self):
        print("The board")
        for i in range(8):
            for j in range(8):
                print(self.board[i][j].name, end=" ") #to do not come to the line after this print
            print("\n")



piece1 = Pieces( [9,3] , "wP" , 1 )

piece2 = Pieces([0,7],"wQ",9)
#print(piece1.name)
plato = Board()
#print(piece1)

#print(f"La pièce peut bouger de manière verticale dans les coins {piece1.vertical_movement(plato.board)}")

#print(f"La pièce peut bouger de manière horizontale dans les coins {piece1.horizontal_movement(plato.board)}")

#print(f"La pièce peut bouger de manière diagonale dans les coins {piece1.diago_movement(plato.board)}")

plato.display()

"""
def vertical_movement(self , board):
        L = []
        [vert,hor] = self.position
        for p in [-1,1]:
            vert_index = vert + p
            while 8 > vert_index > -1 and board[vert_index][hor] == "Em" :
                L.append([vert_index, hor])
                vert_index + = p
        return L
        #Prend moins de ligne


def horizontal_movement(self , board):
            L = []
            [vert,hor] = self.position
            for p in [-1,1]:
            hor_index = hor + p
            while 8 > hor_index > -1 and board[vert][hor_index] == "Em" :
                L.append([vert, hor_index])
                hor_index + = p
        return L

"""