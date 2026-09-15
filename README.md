# Jeu-d-echec
Développement d'un jeu d'échecs en implémentant moi-même les règles et le déplacement des pièces tout en développant une IA pouvant jouer au jeu
Missions:
Création du plateau (avec numéros et lettres)
Baser la c réation des pièces sur des objets en y mettant les caractéristiques, le déplacement

création de chaque pièce : 
  -Pion
  -Cavalier
  -Fou
  -Tour
  -Dame
  -Roi
Règles:
  -Mouvement si place disponible
  -éches et échec  et mat
  -Prise d'une pièce
  -Promotion Dame du Pion
(D'abord créer la règle de l'échec pour ensuite pouvoir gérer les déplacemnts, faire en sorte que les échecs et les prises ne soient pas mis coder en fonction de chaque pièce, mais puissent être coder une fois pour toutes les pièces en même temps).
(les règles de prises et d'échecs sont sensiblements les mêmes)

REGLES DU JEU :
>[!NOTE]
>plato: 
Le plato comporte 64 cases et se déploie comme étant une grille de 8x8 cases numéroté à la verticales de 1 jusqu'à 8 et à l'horizontale de A à H.

>[!NOTE]
>pièces:

>[!NOTE]
>coup possible pour chaque pièce:

>[!TIP]
>coup spéciaux (ces coups ne sont possibles QUE si les pièces en question n'ont pas encore fait de mouvement):
-pion peut se déplacer de 2cases en avant

-prise en passant pour le pion: si un pion du côté adverse arrive à sa hauteur sur le plan vertical à ses 2 cases les plus proches (ou la case la plus proche pour ceux sur les bords), il peut le manger en passant par sa diagonale (ce coup est à effet immédiat)

-le rock, selon les endroits dégagés 

>[!Warning]
>être en échec:

>[!Warning]
>Parties nulles:

>[!CAUTION]
>échec et mat:

