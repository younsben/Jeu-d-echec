import numpy as np

from abc import ABC

class Pieces(ABC):
    def __init__(self,couleur,emplacement,nom,points,inlife = True, already_moved = False):
        self.couleur = nom[0]
        self.emplacement = emplacement
        self.nom = nom
        self.points = points
    
    def same_color(self,piece_same):
        if self.color == piece_same.color:
            return True
        return False


    def eat_piece(self,piece1,piece2,board):
        if piece1.couleur == piece2.couleur :
            return False
        if not check(piece1,board) :
            piece1.move(piece1,piece2.emplacement)
        piece2.inlife = False
    
    def can_move(self, piece, emplacement, board):
        if board[piece.emplacement] !="Vide":
            return can_eat(piece,emplacement,board)
        return True #a fini

    def move(self, emplacement_wanna_move_to):
        if self.can_move(self, emplacement_wanna_move_to):
            self.emplacement = emplacement_wanna_move_to
        else :
            print( "Ce coup n'est pas possible")

    def can_vert(self,empl):
        pass

    def can_hor(self,empl):
        pass

    def can_diago(self,empl):
        pass

    def can_deplacement(self,empl)
   
class Pawn(Pieces): 
    def __init__(self, couleur,emplacement,nom,points,inlife = True, already_moved = False):
        super().__init__(couleur,emplacement,nom,points,inlife = True, already_moved = False )
        self.points = 1
    
    #A finir
    def can_move(self, piece, emplacement):
        super().can_move(self, piece, emplacement )
        return True

    def promotion(self,old_piece,color,new_piece):
        vert = old_piece.emplacement[0] # 0 ou 1 ça reste à vérifier
        hor = old_piece.emplacement[1]

# faire une fonction eatpawn

class Rook(Pieces):
    def __init__(self, couleur,emplacement,nom,points,inlife = True, already_moved = False):
        super().__init__(couleur,emplacement,nom,points,inlife = True, already_moved = False )
        self.points = 5



class Bishop(Pieces):
    def __init__(self, couleur,emplacement,nom,points,inlife = True, already_moved = False):
        super().__init__(couleur,emplacement,nom,points,inlife = True, already_moved = False )
        self.points = 3



class Knight(Pieces):
    def __init__(self, couleur,emplacement,nom,points,inlife = True, already_moved = False):
        super().__init__(couleur,emplacement,nom,points,inlife = True, already_moved = False )
        self.points = 3



class Queen(Pieces):
    def __init__(self, couleur,emplacement,nom,points,inlife = True, already_moved = False):
        super().__init__(couleur,emplacement,nom,points,inlife = True, already_moved = False )
        self.points = 9



class King(Pieces):
    def __init__(self, couleur,emplacement,nom,points,inlife = True, already_moved = False):
        super().__init__(couleur,emplacement,nom,points,inlife = True, already_moved = False )
        self.points = 1000000000

    def deplacement(self, board):
        pass

    def check(self, board):
        return True



   
   
    def rock(self,color,emplacement_rock):
        pass
    
#sous classe pour roi, tour pour le rock et le pion pour la prise en passant
# if != "Vide": alors utiliser le init sur la pièce
"""pour promotion d'un pion, il suffira de faire:
  pion = Pieces(dame)
  Faire héritage pour pion, roi et tour pour savoir si ils ont déjà bougé
  ajouté un répertoire de coup pour chaque pièces sous format tableau,
  mettre une méthode sous format __char__ pour print les coups
  Sous classe pour toutes les pièces où on met ce qu'ils peuvent faire comme coup
  mettre dans la sous classe roi qu'il ne peut pas bouger si il devient échec"""
  # regarder TOUTES les règles les lister et les transcrire
  #Mettre classe abstraite pour la classe pièce
  


#créer un dico pour associer chaque lettre à sa classe??
class Board:
    def __init__(self ):
        self.board = np.full((8,8),"Vide")
        first_line =np.array(["R","N","B","Q","K","B","K","R"])
        self.board[0] = [ "w" + p for p in first_line]
        self.board[1] = "wPawn"
        self.board[7] = [ "b" + p for p in first_line]
        self.board[6] = "bPawn"

    def display(self):
        print(self.board)
    
    def img(self) :
        pass #si le temps connecter chaque pièce et le plateau à une image


    def update_board(self, change):
        #if can_moove(change.piece, change.piece.mouvement):
            return True

plat = Board()
plat.display()