
import numpy as np
from enum import Enum
from abc import ABC
"""git.ignore uv pour les import"""
size_max_row = 7
size_max_column = 7
size_min_row = 0
size_min_column = 0
class Color(Enum):
    WHITE = "w"
    BLACK = "b"
    EMPTY ="E"

class Target(Enum):
    ALLY = 0
    ENNEMY = 1
    NOTHING = 2

class Pieces(ABC):
    def __init__(self , position : tuple[int, int] , name : str , points : int = 0 , inlife : bool = True , already_moved : bool = False):
        self.statu = Color(name[0]) 
        self.position = position # emplacement is an array of 2 int, where the first value is the horizontal position and the second one the vertical position
        self.name = name
        self.points = points
        self.already_moved = already_moved

    def not_out_of_range(self, hor: int, vert : int) -> bool:
        return (size_max_row + 1 > hor >size_min_row - 1) and (size_max_column + 1> vert > size_min_column - 1)
    
#with enum
    def target_piece_statu(self , piece : Pieces) -> Target:
        match self.color :
            case piece.statu:
                return Target.ALLY
            case Color.EMPTY :
                return Target.NOTHING
            case _ :
                return Target.ENNEMY
    
    def mouvement_possible(self, board : np.array[Pieces], move : tuple[int, int]) -> bool:
        #look at if the move is possible make a super to look at it
        king = Pieces((8,8), "Em") #
        #find the king to see if after the move he is not check
        if king.check(board) : 
            return False
        
        pass



#direction : (-1/1,0) -> vert move, (0,1)->hor, (1,1)etc.. diago
    def get_sliding_moves(self , board : np.array[Pieces] , direction : tuple[int, int]) -> tuple[list, list] :
        moves = []
        eat = []
        vert, hor = self.position
        (dver , dhor) = direction
        vert , hor = vert + dver , hor + dhor
        while self.not_out_of_range(hor, vert) :
            match self.target_piece_statu(board[vert][hor]):
                case Target.NOTHING:
                    moves.append([vert,hor])
                case Target.ENNEMY:
                    eat.append([vert,hor])
                    return moves , eat
                case Target.ALLY:
                    return moves , eat
            vert , hor = vert + dver , hor + dhor
        return (moves , eat)


# vertical movement return a list with all of the possible move on the vertical road
    def vertical_movement(self , board  : np.array[Pieces] ) -> tuple[list, list]:
        moves_top , eat_top = self.get_sliding_moves( board , (1,0)) 
        moves_bottom , eat_bottom = self.get_sliding_moves( board , (-1,0))
        return (moves_top + moves_bottom , eat_top + eat_bottom)


# horizontal movement return a list with all of the possible move on the vertical road
    def horizontal_movement(self , board : np.array[Pieces]):
            moves_right , eat_right = self.get_sliding_moves( board , (0,1)) 
            moves_left , eat_left = self.get_sliding_moves( board , (0,-1))
            return moves_right + moves_left  , eat_right + eat_left


    def diago_movement(self , board : np.array[Pieces]):
        moves = []
        eat = []
        for i in [-1,1]:
            for j in [-1,1]:
                movement , eating = self.get_sliding_moves( board , (i,j))  
                moves , eat =  moves + movement , eat + eating       
        return moves ,eat

#thanks gemini I did 3 last code in 5lines instead of 30 lines for the last by implementeing a new function "get_sliding_moves"

   

    def the_L_movement(self , board : np.array[Pieces]): #knight
        moves = [] 
        eat =[]
        [vert , hor] = self.position 
        jumps = [( -2 , -1 ) , ( -2 , 1 )  , ( -1 , -2 ) ,( -1 , 2 ) , ( 1 , -2 ) , ( 1 , 2 ) , ( 2 , -1 ) , ( 2 , 1 ) ]
        for k in jumps :
            dver , dhor = k 
            new_vert = vert + dver
            new_hor = hor + dhor
            if self.not_out_of_range(new_hor, new_vert):
                if self.target_piece_statu(board[new_vert][new_hor]) == Target.NOTHING :
                    moves.append([new_vert, new_hor])
                elif self.target_piece_statu(board[new_vert][new_hor]) == Target.ENNEMY :
                    eat.append([new_vert, new_hor])
        return moves , eat



    def can_eat_piece(self , piece : Pieces , board : np.array[Pieces]):
        pass
    def eat_piece(self, piece , board):
        pass
         
class Pawn(Pieces):
    def mouvement_possible(self, board : np.array[Pieces], move : tuple[int, int]) -> bool : # il faudra ajouter une condition sur le fait que si c'est un coup prommotionnel ou non
        super().mouvement_possible(self, board , move)
        movement, eating = self.pawn_advancement(board)
        if (movement in move) or (movement in eating) : # si le coup est un avancement possible ou est un coup qui peut manger une autre pièce, le coup est possible
            return True
        return False


    def pawn_advancement(self , board  : np.array[Pieces] ):
            [vert , hor] = self.position
            moves = []
            vert_index = vert + 1 #the next move possible
            if vert != size_max_column : # if we are not at the end of the map, look at 
                if board[vert_index , hor].name == Target.NOTHING:
                    moves.append([vert_index , hor])
                    vert_index += 1
                    if not(self.already_moved) and board[vert_index , hor] == Target.NOTHING : # if we 'he never moved the pawn can andvance by 2 cases
                        moves.append([ vert_index , hor ])
                return moves , self.pawn_eating(board)
            

#the promotion function return [] if the pawn cannot be promuted else, it send the possibility to be promoted, if it can eat or just advance, we already know the pawn is at the end of the map
#this move required a new input
    def promotion(self , board  : np.array[Pieces] , hor : int ):
        moves = []
        vert = size_max_column - 1 
        if board[vert+1][hor].name == Target.NOTHING :
            moves.append(board[vert+1][hor])
        return moves , self.pawn_eating(board)
        


 # the pawn eat a piece   
    def pawn_eating(self , board : np.array[Pieces]):
        [vert , hor] = self.position
        eat = []
        new_vert = vert + 1
        new_hor = hor
        for p in [-1 , 1] :
            new_hor = hor + p
            if new_hor > -1 and self.target_piece_statu(board[new_vert][new_hor]) == Target.ENNEMY:
                eat.append([new_vert , new_hor])
        return eat


class King(Pieces):

#the usual movement
    def king_moves(self , board : np.array[Pieces]) -> bool:
        moves = []
        [vert , hor] = self.position 
        new_vert = vert 
        new_hor = hor
        king_movement = [[-1,-1] , [-1,0] , [-1,1] , [0,-1] , [0,0] , [0,1] , [1,-1] , [1,0] , [1,1]]
        for p in king_movement:
            new_vert += p[0]
            new_hor += p[1]
            if self.not_out_of_range(self, new_hor, new_vert):
                piece = board[new_vert][new_hor]
                if self.target_piece_statu(piece) != Target.ALLY :
                    moves.append([new_vert , new_hor])
            new_vert = vert
            new_hor = hor
        return moves


#a function that verify if the list is empty or not
    def move_eat(self , board , list_moves , name1 , name2) : #put a function on the enter of function
        if list_moves != [] :
            for p in list_moves :
                if self.target_piece_statu(p) == Target.ALLY and (p.name == name1 or p.name == name2 ):
                    return True
        return False


    def piece_being_eatable(self , board : np.array[Pieces]) -> bool:
        _ , eat_vert = self. vertical_movement(board) 
        _ , eat_hor = self. horizontal_movement(board)
        _ , eat_diago = self. diago_movement(board)
        _ , eat_Lmove = self. vertical_movement(board)
        if self.move_eat(board , eat_Lmove , "N", None):
            return True
        if self.king_moves(board) == [] :
            return False
        if self.move_eat( board , eat_vert , "Q" , "R") or self.move_eat( board , eat_hor , "Q" , "R") or self.move_eat( board , eat_diago , "Q" , "B") :
            return True
        return False

    # check if the color on the enter is check or not
    # to do it we will look at the king and see him like other pieces to see if anyone could eat him
    def check(self, board : np.array[Pieces]) -> bool:
        for p in board :
            if self.name == "K" and self.target_piece_statu == Target.ALLY and p.piece_being_eatable(board):
                    return True
        return False

    def check_mate(self, board : np.array[Pieces], my_color : Enum) -> bool:
        if not(self.checkmate(board)) :
            return False
        
# THE NEXT TIME, TEST THE FUNCTION ask to gemini to create test boards and test pieces:


#add a super and instead of the name put the 'real name' like queen instead of Q
"""  def __str__(self):
        return "From str method of Test: name is %s" % (self.name)"""
#for the move add the capture of the opponent , if not same color
# verify the check only if a piece could eat the king not always if there is a chack mat

class Empty(Pieces):
    pass

chess_board_size =(8,8)
class Board:
    def __init__(self ):
        tab = np.full(chess_board_size, "Em") #E is for an empty case
        first_line = np.array(["R","N","B","Q","K","B","N","R"])
        tab[0] = [ "w" + p for p in first_line]
        tab[1] = "wP"
        tab[7] = [ "b" + p for p in first_line]
        tab[6] = "bP"
        empt = Pieces([0,0] , "Em")
        self.board = np.full((8,8), empt, dtype = Pieces)
        for i in range(8):
            for j in range(8):
                self.board[i][j] = Pieces([i,j] , tab[i][j])


    def display(self):
        print("The board")
        for i in range(8):
            print("|_______________________________________|  \n")
            for j in range(8):
                print("|", self.board[i][j].name, end=" ") #to do not come to the line after this print
            print("| ")
            
        print(" _______________________________________  ")



piece1 = Pieces( [9,3] , "wP" , 1 )

piece2 = Pieces([-1,0],"wQ",9)


#print(piece1.name)
plato = Board()
#print(piece1)

#print(f"La pièce peut bouger de manière verticale dans les coins {piece1.vertical_movement(plato.board)}")

#print(f"La pièce peut bouger de manière horizontale dans les coins {piece1.horizontal_movement(plato.board)}")

#print(f"La pièce peut bouger de manière diagonale dans les coins {piece1.diago_movement(plato.board)}")

plato.display()

