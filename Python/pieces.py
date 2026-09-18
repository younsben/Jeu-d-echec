import numpy as np

from abc import ABC

class Pieces():
    def __init__(self , position , name , points = 0 , inlife = True , already_moved = False):
        self.color = name[0]
        self.position = position # emplacement is an array of 2 int, where the first value is the horizontal position and the second one the vertical position
        self.name = name
        self.points = points
    
    
    def same_color(self,piece_same):
        if self.color == piece_same.color:
            return True
        return False

    

# vertical movement return a list with all of the possible move on the vertical road
    def vertical_movement(self , board):
        L = []
        [vert,hor] = self.position
        vert_index = vert-1
        while vert_index > -1 and board[vert_index][hor] == "Em" :
            L.append([vert_index, hor])
            vert_index -=1
        L = L[::-1] # put the List in order to test the function

        vert_index = vert + 1

        while vert_index < 8 and board[vert_index][hor] == "Em"  :
            L.append([vert_index, hor])
            vert_index +=1

        return L


    def horizontal_movement(self , board):
            L = []
            [vert,hor] = self.position
            hor_index = hor - 1
            while hor_index > -1 and board[vert][hor_index] == "Em" :
                L.append([vert, hor_index])
                hor_index -=1
            L = L [::-1] # put the List in order to test the function
            hor_index = hor + 1

            while hor_index < 8 and board[vert][hor_index] == "Em"  :
                L.append([vert, hor_index])
                hor_index +=1

            return L


    def diago_movement(self , board):
        L = []
        [vert,hor] = self.position
        vert_index, hor_index = vert , hor
        for i in [-1,1]:
            for j in [-1,1]:
                hor_index =  hor
                vert_index = vert
                vert_index = vert_index + i
                hor_index = hor_index + j
                while (8 > hor_index > -1) and (8 > vert_index > -1) and (board[vert_index][hor_index] == "Em") :
                    L.append([vert_index, hor_index])
                    vert_index = vert_index + i
                    hor_index = hor_index + j
                    
        return L

    def pawn_advancement(self , board):
        [vert , hor] = self.position
        L = []
        vert_index = vert + 1 
        if vert != 7:
            if board[vert_index , hor] == ["Em"] :
                L.append([vert_index , hor])
                vert_index += 1
                if not(self.already_moved) and board[vert_index , hor] == ["Em"] :
                    L.append([ vert_index , hor ])
        else :
            if board[vert_index , hor] == ["Em"] :
                self.promotion()
        return L
    
    def promotion():
        pass
    
    def pawn_eating(self , board):
        [vert , hor] = self.position
        L = []
        new_vert = vert + 1
        new_hor = hor
        if new_vert != 7:
            for p in [-1 , 1] :
                if (8 > new_hor > -1) and board:
                    pass
    

#add a super and instead of the name put the 'real name' like queen instead of Q
    def __str__(self):
        return "From str method of Test: name is %s" % (self.name)
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
print(piece1)

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