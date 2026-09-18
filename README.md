# Jeu-d-echec
Développement d'un jeu d'échecs en implémentant moi-même les règles et le déplacement des pièces tout en développant une IA pouvant jouer au jeu
Missions:
Création du plateau (avec numéros et lettres)


Règles:
  -Mouvement si place disponible

  -Promotion Dame du Pion
(D'abord créer la règle de l'échec pour ensuite pouvoir gérer les déplacements, faire en sorte que les échecs et les prises ne soient pas mis coder en fonction de chaque pièce, mais puissent être coder une fois pour toutes les pièces en même temps).
(les règles de prises et d'échecs sont sensiblements les mêmes)

REGLES DU JEU :
>[!NOTE]
>plato: 
Le plato comporte 64 cases et se déploie comme étant une grille de 8x8 cases numéroté à la verticales de 1 jusqu'à 8 et à l'horizontale de A à H.
La case en bas à gauche est une case blanche

>[!NOTE]
>pièces:
16 pions
4 cavaliers
4 fous
4 tours
2 dames
2 rois


>[!NOTE]
>coup possible pour chaque pièce:

Le pion :
il peut se déplacer d'une case en avant, il peut avancer de deux cases si les deux cases sont libres et s'il n'a pas encore fait de coup. Lorsqu'une pièce est une case en diagonale vers l'avant il peut la capturer.

Le cavalier :
Il peut se déplacer de deux cases dans une direction puis une case à la perpendiculaire de cette direction (forme de L), il a la possibilité de sauter des cases.

Le fou :
Il peut se déplacer d'autant de case qu'il le souhaite en diagonale sans pouvoir sauter par-dessus d’autres pièces d’échecs.

La tour :
Elle peut se déplacer d'autant de case qu'il le souhaite à l'horizontale ou à la verticale sans pouvoir sauter par-dessus d’autres pièces d’échecs.

La dame :
Elle peut se déplacer dans toutes les directions (horizontale, verticale, diagonales (mettre ces directions dans la classe pièce)) sans pouvoir sauter par-dessus d’autres pièces d’échecs.

Le roi:
Il peut se déplacer dans toutes les directions dans un périmètre de une case.

>[!TIP]
>Les coup spéciaux (ces coups ne sont possibles QUE si les pièces en question n'ont pas encore fait de mouvement):*

-Le pion peut se déplacer de 2cases en avant

-La prise en passant pour le pion: si un pion du côté adverse arrive à sa hauteur sur le plan vertical à ses 2 cases les plus proches (ou la case la plus proche pour ceux sur les bords), il peut le manger en passant par sa diagonale (ce coup est à effet immédiat)

-Le roque, . Le roi se déplace de deux cases vers la tour et la tour se place sur la case que le roi a franchie

>[!Warning]
>être en échec:
Lorsqu'une pièce à la possibilité de capturer le roi

>[!Warning]
>Parties nulles:
Se produit lorsque :
- La même position s'est produite 3 fois sans aucun changement sur le plato
- Le pat, l'adversaire n'a aucun moyen de bouger ses pièces ou son roi sans que celui-ci soit en échec
- Demander la partie nulle
- Matériel insuffisant, avec les pièces restantes, aucun joueur ne peut finir la partie en mettant échecs et mat l'adversaire.

>[!CAUTION]

>Echec et mat:

Lorsque le roi est mis en échec et qu'il n'y a aucun moyen de déplacer son roi ou une autre pièce de tel sorte qu'il ne soit plus en échec

>[!TIPS]

>les règles sous forme de classe?

>[!TIPS]

>Structure du code:

Enumérer toutes les règles implicites ce qui me permettra de mieux structurer mon code et d'éviter des oublis de dernière minute ainsi que des erreurs simple à corriger.

>[!Note]
>Listage:
- Les pièces d'une même couleur ne peuvent pas se capturer entre elle
- Une pièce ne peut pas mettre en échec son propre roi
- One ne peut pas dépasser les limites physique du plateau
- Dans la fonction update plato il faudra faire plusieurs vérifications, est-ce que les coups sont bons, est-ce qu'un roi est en échec si oui est-ce que c'est un mat
- Ajouter des photos d'un plateau, de chaque pièces, pour les pièces faire une méthode dans la classe pièces auquel on fera un super dans chaque sous classe, différencier si la pièce est blanche ou noit
- Ajouter la possibilité de retourner le plato selon qu'on joue avec les blancs ou les noirs
- Placer les numérotations sur le plato


Je vais commencer par créer le plateau d'échec.
Puis je vais créer chacune des pièces et leur spécificité (les déplacements et les coups spéciaux).
Et enfin je vais y implémenter les différentes règles.
Le concept du jeu est d'opposer les pièces noires aux pièces blanches, donc une pièce blanche ne peut ni capturer une pièce et ni mettre le roi de sa couleur en échec

Pour simplifier le jeu, je vais commencer par prendre en compte que les joueurs savent jouer aux échecs, ce qui permettra d'aller plus vite au début, les contraintes viendront au fur et à mesure.

Une fois que le jeu d'échec sera fini, je vais pouvoir commencer par développer l'IA, je n'ai pas encore d'idée sur comment le structurer ni même quelle stratégie de code utiliser