class Pieces:
    def __init__(self,couleur,emplacement,nom,points,inlife = True, already_moved = False):
        self.couleur = nom[0]
        self.emplacement = emplacement
        self.nom = nom
        self.points = points

    def eat_piece(self,piece1,piece2):
        if piece1.couleur == piece2.couleur :
            return False
        piece1.move(piece1,piece2.emplacement)
        piece2.emplacement = "Vide"
        piece2.inlife = False
    
    def can_move(self, piece, emplacement):
        return True #a finir

    def move(self,piece, emplacement):
        if piece.can_move(piece, emplacement):
            piece.emplacement = emplacement
        else :
            print( "Ce coup n'est pas possible")


   
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
  
class Board:
    def __init__(self ):
        pass

    def update_board(self, change):
        #if can_moove(change.piece, change.piece.mouvement):
            return True
