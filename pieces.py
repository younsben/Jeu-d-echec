class Pieces:
    def __init__(self,couleur,emplacement,nom,points,inlife = True, already_moved = False):
        self.couleur = couleur
        self.emplacement = emplacement
        self.nom = nom
        self.points = points
    def eat_piece(self,piece1,piece2):
        piece1.emplacement = piece2.emplacement
        piece2.inlife = False
    def rock(self,color,emplacement_rock):
        pass
    def promotion(self,color,new_piece):
        pass
#sous classe pour roi, tour pour le rock et le pion pour la prise en passant
# if != "Vide": alors utiliser le init sur la pièce
"""pour promotion d'un pion, il suffira de faire:
  pion = Pieces(dame)
  Faire héritage pour pion, roi et tour pour savoir si ils ont déjà bougé
  ajouté un répertoire de coup pour chaque pièces sous format tableau,
  mettre une méthode sous format __char__ pour print les coups"""
  # regarder TOUTES les règles les lister et les transcrire
