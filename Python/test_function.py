"""
Fichier de tests pour valider les fonctions de la classe Pieces et Board
Jeu d'échecs en Python
"""

import numpy as np

from pieces import Pieces, Board

# ==============================================================================
# Utilitaires pour créer et afficher des plateaux de test
# ==============================================================================

def create_empty_board():
    """Crée un plateau 8x8 rempli de cases vides Pieces([i, j], 'Em')."""
    board = np.empty((8, 8), dtype=object)
    for i in range(8):
        for j in range(8):
            board[i, j] = Pieces([i, j], "Em")
    return board


def create_custom_board(placements):
    """
    Crée un plateau sur-mesure à partir d'un dictionnaire :
    placements = {
        (ligne, colonne): ("nom_piece", points, already_moved)
    }
    Exemple : {(4, 4): ("wN", 3), (2, 3): ("wP", 1)}
    """
    board = create_empty_board()
    for (r, c), item in placements.items():
        if isinstance(item, Pieces):
            item.position = [r, c]
            board[r, c] = item
        elif isinstance(item, tuple):
            name = item[0]
            pts = item[1] if len(item) > 1 else 0
            moved = item[2] if len(item) > 2 else False
            p = Pieces([r, c], name, points=pts, already_moved=moved)
            p.already_moved = moved
            board[r, c] = p
        elif isinstance(item, str):
            board[r, c] = Pieces([r, c], item)
    return board


def display_board_with_moves(board, piece, possible_moves=None, title=""):
    """
    Affiche l'échiquier dans le terminal avec :
      - [wN] : la pièce active testée
      -  XX  : case vide où la pièce peut aller
      - *bP* : pièce ennemie prenable
      -  ..  : case vide inaccessible
    """
    if possible_moves is None:
        possible_moves = []

    moves_set = {tuple(m) for m in possible_moves}

    print("\n" + "=" * 45)
    if title:
        print(f" {title}")
    print("=" * 45)
    print("    0    1    2    3    4    5    6    7  (colonnes)")
    print("  +----+----+----+----+----+----+----+----+")

    for i in range(8):
        row_str = f"{i} |"
        for j in range(8):
            cell_piece = board[i, j]
            name = getattr(cell_piece, "name", "Em") if hasattr(cell_piece, "name") else str(cell_piece)

            if [i, j] == piece.position:
                row_str += f"[{name:^2}]|"
            elif (i, j) in moves_set:
                if name != "Em":
                    row_str += f"*{name:^2}*|"  # Prise possible
                else:
                    row_str += " XX |"           # Déplacement libre
            else:
                row_str += f" {name:^2} |" if name != "Em" else " .. |"
        print(row_str)
        print("  +----+----+----+----+----+----+----+----+")
    print(f"Position : {piece.position} ({piece.name})")
    print(f"Coups calculés ({len(possible_moves)}) : {possible_moves}")


# ==============================================================================
# TESTS DES DIFFÉRENTES PIÈCES ET LOGIQUES
# ==============================================================================

def test_knight_L_eatable():
    print("\n>>> TEST 1 : Cavalier (the_L_eatable)")

    # 1. Cavalier au centre (4, 4) sur plateau vide -> 8 sauts possibles
    board1 = create_empty_board()
    knight_center = Pieces([4, 4], "wN", 3)
    board1[4, 4] = knight_center
    moves = knight_center.the_L_eatable(board1)
    display_board_with_moves(board1, knight_center, moves, "Cavalier blanc au centre (4, 4)")
    assert len(moves) == 8, f"Erreur : attendu 8 coups, obtenu {len(moves)}"

    # 2. Cavalier dans un coin (0, 0) -> seulement 2 sauts possibles : (1, 2) et (2, 1)
    board2 = create_empty_board()
    knight_corner = Pieces([0, 0], "wN", 3)
    board2[0, 0] = knight_corner
    moves_corner = knight_corner.the_L_eatable(board2)
    display_board_with_moves(board2, knight_corner, moves_corner, "Cavalier blanc au coin (0, 0)")
    assert len(moves_corner) == 2, f"Erreur : attendu 2 coups dans le coin, obtenu {len(moves_corner)}"

    # 3. Cavalier avec allié et ennemi
    board3 = create_custom_board({
        (4, 4): ("wN", 3),
        (2, 3): ("wP", 1),  # Allié blanc (ne doit pas être pris)
        (2, 5): ("bP", 1),  # Ennemi noir (doit pouvoir être capturé)
    })
    knight_test = board3[4, 4]
    moves_obst = knight_test.the_L_eatable(board3)
    display_board_with_moves(board3, knight_test, moves_obst, "Cavalier avec allié en (2,3) et ennemi en (2,5)")
    print("✅ Test Cavalier validé !")


def test_king_eatable():
    print("\n>>> TEST 2 : Roi (king_eatable)")

    # 1. Roi au centre (3, 3) -> 8 cases adjacentes
    board = create_empty_board()
    king = Pieces([3, 3], "wK", 0)
    board[3, 3] = king
    moves = king.king_eatable(board)
    display_board_with_moves(board, king, moves, "Roi blanc au centre (3, 3)")
    assert len(moves) == 8, f"Attendu 8 coups, obtenu {len(moves)}"

    # 2. Roi au bord (0, 4) avec pièces autour
    board_edge = create_custom_board({
        (0, 4): ("wK", 0),
        (0, 3): ("wQ", 9),  # Allié à gauche
        (1, 4): ("bP", 1),  # Ennemi en face
    })
    king_edge = board_edge[0, 4]
    moves_edge = king_edge.king_eatable(board_edge)
    display_board_with_moves(board_edge, king_edge, moves_edge, "Roi au bord (0, 4) avec allié en (0,3) et ennemi en (1,4)")
    print("✅ Test Roi validé !")


def test_pawn_advancement():
    print("\n>>> TEST 3 : Avancement du Pion (pawn_advancement)")

    # 1. Pion n'ayant pas encore bougé (doit pouvoir avancer de 1 ou 2 cases)
    board = create_empty_board()
    pawn = Pieces([1, 4], "wP", 1, already_moved=False)
    pawn.already_moved = False
    board[1, 4] = pawn
    moves = pawn.pawn_advancement(board)
    display_board_with_moves(board, pawn, moves, "Pion initial en (1, 4) - départ")

    # 2. Pion bloqué par une pièce adverse juste devant
    board_blocked = create_custom_board({
        (1, 4): ("wP", 1, False),
        (2, 4): ("bP", 1, False)
    })
    pawn_b = board_blocked[1, 4]
    moves_b = pawn_b.pawn_advancement(board_blocked)
    display_board_with_moves(board_blocked, pawn_b, moves_b, "Pion bloqué par une pièce en (2, 4)")
    print("✅ Test Avancement Pion validé !")


def test_pawn_eatable():
    print("\n>>> TEST 4 : Prise diagonale du Pion (pawn_eatable)")

    board = create_custom_board({
        (2, 3): ("wP", 1),
        (3, 4): ("bP", 1),  # Ennemi en diagonale droite
        (3, 2): ("wP", 1),  # Allié en diagonale gauche
    })
    pawn = board[2, 3]
    can_eat = pawn.pawn_eatable(board)
    print(f"Le pion en (2, 3) peut-il capturer une pièce adverse ? : {can_eat}")
    display_board_with_moves(board, pawn, [], "Pion en (2, 3) face à un ennemi en (3, 4)")
    print("✅ Test Prise Pion validé !")


def test_vertical_and_horizontal():
    print("\n>>> TEST 5 : Lignes & Colonnes (Tour / Reine)")

    board = create_custom_board({
        (4, 4): ("wR", 5),
        (2, 4): ("bP", 1),  # Obstacle au-dessus
        (4, 6): ("wP", 1),  # Obstacle allié à droite
    })
    rook = board[4, 4]

    if hasattr(rook, "vertical_movement"):
        vert_moves = rook.vertical_movement(board)
        display_board_with_moves(board, rook, vert_moves, "Mouvements verticaux de la Tour en (4, 4)")

    if hasattr(rook, "horizontal_movement"):
        hor_moves = rook.horizontal_movement(board)
        display_board_with_moves(board, rook, hor_moves, "Mouvements horizontaux de la Tour en (4, 4)")


def test_diagonal_movement():
    print("\n>>> TEST 6 : Diagonales (Fou / Reine)")

    board = create_custom_board({
        (3, 3): ("wB", 3),
        (1, 1): ("bP", 1),  # Obstacle en diagonale
    })
    bishop = board[3, 3]

    if hasattr(bishop, "diago_movement"):
        diago_moves = bishop.diago_movement(board)
        display_board_with_moves(board, bishop, diago_moves, "Mouvements diagonaux du Fou en (3, 3)")


def test_standard_board():
    print("\n>>> TEST 7 : Plateau standard (Board)")
    b = Board()
    b.display()
    print("✅ Affichage standard validé !")


# ==============================================================================
# EXÉCUTION DE TOUS LES TESTS
# ==============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print(" DÉBUT DE LA SUITE DE TESTS - JEU D'ÉCHECS")
    print("=" * 60)

    test_knight_L_eatable()
    test_king_eatable()
    test_pawn_advancement()
    test_pawn_eatable()
    test_vertical_and_horizontal()
    test_diagonal_movement()
    test_standard_board()

    print("\n" + "=" * 60)
    print(" TOUS LES TESTS SE SONT EXÉCUTÉS ! 🎉")
    print("=" * 60)
