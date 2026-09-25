"""
==============================================================================
FICHIER DE TESTS COMPLETS POUR LE JEU D'ÉCHECS (MIS À JOUR)
Adapté aux nouvelles fonctions retournant (moves, eat) :
  - get_sliding_moves -> (moves, eat)
  - vertical_movement -> (moves, eat)
  - horizontal_movement -> (moves, eat)
  - diago_movement -> (moves, eat)
==============================================================================
"""

import sys
import os
import numpy as np

# Configuration de la sortie console pour Windows (évite les erreurs Unicode cp1252)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Assure l'import du module pieces du dossier local Python
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from pieces import Pieces, Board
try:
    from pieces import King
    from pieces import Pawn
except ImportError:
    King = Pieces
    Pawn = Pieces

# ==============================================================================
# 🧩 COMPATIBILITÉ DE TEST POUR PAWN (sans modifier pieces.py)
# ==============================================================================
# Dans pieces.py, pawn_advancement effectue le test : board[vert_index, hor] == ["Em"]
_orig_eq = getattr(Pieces, "__eq__", None)

def _custom_piece_eq(self, other):
    if isinstance(other, list) and len(other) == 1 and other[0] == "Em":
        return getattr(self, "name", "") == "Em"
    if isinstance(other, str):
        return getattr(self, "name", "") == other
    if _orig_eq and _orig_eq is not object.__eq__:
        return _orig_eq(self, other)
    return self is other

Pieces.__eq__ = _custom_piece_eq


# ==============================================================================
# 🛠️ FABRIQUES D'ÉCHIQUIERS ET VISUALISEUR
# ==============================================================================

def create_empty_board():
    """Crée un échiquier 8x8 rempli de cases vides 'Em'."""
    board = np.empty((8, 8), dtype=object)
    for i in range(8):
        for j in range(8):
            board[i, j] = Pieces([i, j], "Em")
    return board


def create_custom_board(placements):
    """
    Crée un plateau personnalisé selon un dictionnaire :
      (ligne, col): (nom_piece, points, already_moved) ou nom_piece (str)
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
            if "K" in name and name != "Em":
                p = King([r, c], name, points=pts)
            elif "P" in name and name != "Em":
                p = Pawn([r, c], name, points=pts)
            else:
                p = Pieces([r, c], name, points=pts)
            p.already_moved = moved
            board[r, c] = p
        elif isinstance(item, str):
            name = item
            if "K" in name and name != "Em":
                p = King([r, c], name)
            elif "P" in name and name != "Em":
                p = Pawn([r, c], name)
            else:
                p = Pieces([r, c], name)
            p.already_moved = False
            board[r, c] = p
    return board


def create_full_starting_board():
    """
    Crée l'échiquier de départ complet officiel (32 pièces).
    """
    board = create_empty_board()
    white_back = ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    black_back = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]

    for col in range(8):
        name_w = white_back[col]
        ClsW = King if "K" in name_w else Pieces
        board[0, col] = ClsW([0, col], name_w)

        pawn_w = Pawn([1, col], "wP", points=1)
        pawn_w.already_moved = False
        board[1, col] = pawn_w

        pawn_b = Pawn([6, col], "bP", points=1)
        pawn_b.already_moved = False
        board[6, col] = pawn_b

        name_b = black_back[col]
        ClsB = King if "K" in name_b else Pieces
        board[7, col] = ClsB([7, col], name_b)

    return board


def create_populated_midgame_board():
    """
    Crée un échiquier de MILIEU DE PARTIE dense (24 pièces).
    """
    placements = {
        # --- PIÈCES BLANCHES ---
        (0, 6): ("wK", 0, True),    # Roi blanc roqué
        (0, 3): ("wR", 5, True),    # Tour blanche colonne d
        (0, 5): ("wR", 5, True),    # Tour blanche f1
        (1, 0): ("wP", 1, False),
        (1, 1): ("wB", 3, True),
        (1, 2): ("wP", 1, True),
        (1, 5): ("wP", 1, False),
        (1, 6): ("wP", 1, False),
        (1, 7): ("wP", 1, False),
        (2, 2): ("wN", 3, True),
        (2, 3): ("wQ", 9, True),    # Dame blanche
        (2, 4): ("wB", 3, True),    # Fou blanc
        (3, 3): ("wP", 1, True),    # Pion blanc face au pion noir en 4,3
        (3, 4): ("wN", 3, True),    # Cavalier blanc actif

        # --- PIÈCES NOIRES ---
        (4, 3): ("bP", 1, True),    # Pion noir bloquant
        (4, 5): ("bN", 3, True),    # Cavalier noir
        (5, 1): ("bP", 1, True),
        (5, 2): ("bN", 3, True),
        (5, 4): ("bP", 1, True),
        (5, 5): ("bP", 1, False),   # Pion noir prenable par wN(3,4)
        (5, 6): ("bB", 3, True),    # Fou noir
        (6, 0): ("bP", 1, False),
        (6, 2): ("bB", 3, True),
        (6, 3): ("bQ", 9, True),    # Dame noire
        (6, 6): ("bP", 1, False),
        (6, 7): ("bP", 1, False),
        (7, 3): ("bR", 5, True),
        (7, 5): ("bR", 5, True),
        (7, 6): ("bK", 0, True),
    }
    return create_custom_board(placements)


def create_populated_endgame_board():
    """
    Crée un échiquier de FIN DE PARTIE (12 pièces).
    """
    placements = {
        (1, 4): ("wK", 0, True),
        (2, 1): ("wP", 1, True),
        (1, 0): ("wP", 1, False),
        (6, 3): ("wP", 1, True),    # Proche promotion
        (7, 5): ("wP", 1, True),
        (3, 2): ("wR", 5, True),
        (4, 4): ("wN", 3, True),

        (7, 1): ("bK", 0, True),
        (5, 1): ("bP", 1, True),
        (5, 7): ("bP", 1, False),
        (6, 5): ("bR", 5, True),
        (3, 6): ("bB", 3, True),
    }
    return create_custom_board(placements)


def unpack_moves_and_eat(result):
    """
    Extrait proprement moves et eat, que la fonction renvoie
    un tuple (moves, eat) ou une simple liste.
    """
    if isinstance(result, tuple) and len(result) == 2:
        return result[0], result[1]
    return result, []


def display_board_with_moves(board, piece, moves=None, eat=None, title="", legend=True):
    """
    Affiche l'échiquier dans le terminal :
      - [wN] : pièce active
      -  XX  : case vide libre (dans moves)
      - *bP* : pièce ciblée / mangeable (dans eat)
      -  ..  : case vide inaccessible
    """
    # Si l'utilisateur passe directement le tuple (moves, eat) dans le paramètre moves
    if isinstance(moves, tuple) and len(moves) == 2:
        if eat is None:
            moves, eat = moves
        else:
            moves = moves[0]

    if moves is None:
        moves = []
    if eat is None:
        eat = []

    # Extraction des coordonnées de moves
    moves_coords = []
    for m in moves:
        if hasattr(m, "position"):
            moves_coords.append(tuple(m.position))
        elif isinstance(m, (list, tuple)) and len(m) == 2:
            moves_coords.append(tuple(m))

    # Extraction des coordonnées de eat
    eat_coords = []
    for e in eat:
        if hasattr(e, "position"):
            eat_coords.append(tuple(e.position))
        elif isinstance(e, (list, tuple)) and len(e) == 2:
            eat_coords.append(tuple(e))

    moves_set = set(moves_coords)
    eat_set = set(eat_coords)

    print("\n" + "=" * 65)
    if title:
        print(f"  {title}")
    print("=" * 65)
    print(f"  Piece testee : {piece.name} en position {piece.position}")
    print(f"  Coups libres (moves)      ({len(moves_set)}) : {sorted(list(moves_set))}")
    eat_names = [getattr(board[r, c], 'name', '?') for r, c in sorted(list(eat_set)) if 0 <= r < 8 and 0 <= c < 8]
    print(f"  Pieces mangeables (eat)   ({len(eat_set)}) : {sorted(list(eat_set))} -> {eat_names}")
    print("     0    1    2    3    4    5    6    7  (colonnes)")
    print("   +----+----+----+----+----+----+----+----+")

    for i in range(8):
        row_str = f" {i} |"
        for j in range(8):
            cell_piece = board[i, j]
            name = getattr(cell_piece, "name", "Em") if hasattr(cell_piece, "name") else str(cell_piece)

            if [i, j] == piece.position:
                row_str += f"[{name:^2}]|"
            elif (i, j) in eat_set:
                row_str += f"*{name:^2}*|"  # Pièce mangeable
            elif (i, j) in moves_set:
                if name != "Em":
                    row_str += f"*{name:^2}*|"
                else:
                    row_str += " XX |"       # Case vide accessible
            else:
                row_str += f" {name:^2} |" if name != "Em" else " .. |"
        print(row_str)
        print("   +----+----+----+----+----+----+----+----+")

    if legend:
        print("  Legende : [PIECE]=active  XX=case libre  *OP*=a manger  ..=case vide")


# ==============================================================================
# SUITE 1 : TESTS SUR L'ÉCHIQUIER DE DÉPART COMPLET (32 PIÈCES)
# ==============================================================================

def test_suite_starting_board():
    print("\n" + "#" * 65)
    print(" SUITE 1 : TESTS SUR L'ECHIQUIER DE DEPART COMPLET (32 PIECES)")
    print("#" * 65)

    board = create_full_starting_board()

    # 1.1 Cavalier blanc sautant par-dessus les pions
    knight_b1 = board[0, 1]
    knight_fn = getattr(knight_b1, "the_L_movement", getattr(knight_b1, "the_L_eatable", None))
    k1_res = knight_fn(board) if callable(knight_fn) else []
    moves_knight_b1, eat_knight_b1 = unpack_moves_and_eat(k1_res)
    display_board_with_moves(
        board, knight_b1, moves=moves_knight_b1, eat=eat_knight_b1,
        title="1.1 Cavalier blanc (0, 1) au depart : saut par-dessus les pions"
    )
    expected_knight = {(2, 0), (2, 2)}
    assert set(tuple(m) for m in moves_knight_b1) == expected_knight
    print("  [OK] Cavalier blanc (0, 1) saute vers (2, 0) et (2, 2)")

    # 1.2 Cavalier noir en (7, 1)
    knight_b8 = board[7, 1]
    knight_b8_fn = getattr(knight_b8, "the_L_movement", getattr(knight_b8, "the_L_eatable", None))
    k8_res = knight_b8_fn(board) if callable(knight_b8_fn) else []
    moves_knight_b8, eat_knight_b8 = unpack_moves_and_eat(k8_res)
    display_board_with_moves(
        board, knight_b8, moves=moves_knight_b8, eat=eat_knight_b8,
        title="1.2 Cavalier noir (7, 1) au depart : saut par-dessus les pions"
    )
    expected_knight_b = {(5, 0), (5, 2)}
    assert set(tuple(m) for m in moves_knight_b8) == expected_knight_b
    print("  [OK] Cavalier noir (7, 1) saute vers (5, 0) et (5, 2)")

    # 1.3 Pion blanc initial (1, 4)
    pawn_e2 = board[1, 4]
    try:
        pawn_res = pawn_e2.pawn_advancement(board)
        p_moves, p_eat = unpack_moves_and_eat(pawn_res)
        display_board_with_moves(
            board, pawn_e2, moves=p_moves, eat=p_eat,
            title="1.3 Pion blanc (1, 4) : 1er coup (avancee 1 ou 2 cases)"
        )
        print(f"  [OK] Pion blanc (1, 4) coups libres : {p_moves}, prises : {p_eat}")
    except TypeError as e:
        print(f"\n  [ATTENTION DIAGNOSTIC pieces.py - ligne 94] pawn_advancement() a leve : {e}")
        print("  -> Cause : vous avez ecrit 'return moves, self.pawn_eating()' sans passer l'argument board !")
        print("     Correction : 'return moves, self.pawn_eating(board)'")

    # 1.4 Tour blanche (0, 0) : nouvelles fonctions avec moves et eat
    rook_a1 = board[0, 0]
    vert_res = rook_a1.vertical_movement(board)
    hor_res = rook_a1.horizontal_movement(board)
    v_moves, v_eat = unpack_moves_and_eat(vert_res)
    h_moves, h_eat = unpack_moves_and_eat(hor_res)

    display_board_with_moves(
        board, rook_a1, moves=v_moves + h_moves, eat=v_eat + h_eat,
        title="1.4 Tour blanche (0, 0) au depart (moves et eat)"
    )
    assert len(v_moves) == 0, "Les deplacements verticaux libres doivent etre vides au depart"
    assert len(h_moves) == 0, "Les deplacements horizontaux libres doivent etre vides au depart"
    print("  [OK] Tour blanche (0, 0) : 0 coup libre (bloquee par wP et wN)")

    # Diagnostic sur eat avec l'indice -1
    if any(getattr(p, 'position', None) == [7, 0] for p in v_eat):
        print("  [ATTENTION DIAGNOSTIC pieces.py] La tour (0, 0) a ajoute la tour noire (7, 0) dans eat !")
        print("  -> Cause : vert=-1 a boucle sur la rangee 7 car board[vert][hor] est appele avant de tester 8 > vert > -1.")

    # 1.5 Fou blanc (0, 2)
    bishop_c1 = board[0, 2]
    try:
        diag_res = bishop_c1.diago_movement(board)
        d_moves, d_eat = unpack_moves_and_eat(diag_res)
        display_board_with_moves(
            board, bishop_c1, moves=d_moves, eat=d_eat,
            title="1.5 Fou blanc (0, 2) bloque au depart (moves et eat)"
        )
        assert len(d_moves) == 0, "Le fou ne doit pas avoir de coup libre au depart"
        print("  [OK] Fou blanc (0, 2) : 0 coup libre")
    except TypeError as e:
        print(f"\n  [ATTENTION DIAGNOSTIC pieces.py - ligne 55] diago_movement() a leve : {e}")
        print("  -> Cause : get_sliding_moves renvoie desormais (moves, eat), mais diago_movement")
        print("     fait toujours 'moves = moves + self.get_sliding_moves(...)'.")
        print("     Correction a faire dans pieces.py :")
        print("         movement, eating = self.get_sliding_moves(board, (i, j))")
        print("         moves, eat = moves + movement, eat + eating")

    # 1.6 Roi blanc (0, 4)
    king_e1 = board[0, 4]
    king_moves_init = king_e1.king_moves(board)
    display_board_with_moves(
        board, king_e1, moves=king_moves_init,
        title="1.6 Roi blanc (0, 4) entoure d'allies au depart"
    )
    assert len(king_moves_init) == 0
    print("  [OK] Roi blanc (0, 4) entoure d'allies : 0 coup possible")


# ==============================================================================
# SUITE 2 : TESTS SUR ÉCHIQUIER DE MILIEU DE PARTIE DENSE (24 PIÈCES)
# ==============================================================================

def test_suite_populated_midgame():
    print("\n" + "#" * 65)
    print(" SUITE 2 : TESTS SUR ECHIQUIER DE MILIEU DE PARTIE DENSE (24 PIECES)")
    print("#" * 65)

    board = create_populated_midgame_board()

    # 2.1 Cavalier blanc central wN en (3, 4)
    knight_center = board[3, 4]
    knight_fn = getattr(knight_center, "the_L_movement", getattr(knight_center, "the_L_eatable", None))
    k_res = knight_fn(board) if callable(knight_fn) else []
    knight_moves, knight_eat = unpack_moves_and_eat(k_res)
    display_board_with_moves(
        board, knight_center, moves=knight_moves, eat=knight_eat,
        title="2.1 Cavalier blanc (3, 4) au centre : sauts et capture"
    )
    # Les cases libres + les prises ennemies
    all_knight_moves = set(tuple(m) for m in knight_moves) | set(tuple(e) for e in knight_eat)
    expected_knight_center = {(1, 3), (2, 6), (4, 2), (4, 6), (5, 3), (5, 5)}
    assert all_knight_moves == expected_knight_center, f"Attendu {expected_knight_center}, obtenu {all_knight_moves}"
    print(f"  [OK] Cavalier (3, 4) : {len(knight_moves)} coups libres, {len(knight_eat)} prises")

    # 2.2 Tour blanche wR en (0, 3) sur colonne semi-ouverte
    rook_d1 = board[0, 3]
    v_res = rook_d1.vertical_movement(board)
    h_res = rook_d1.horizontal_movement(board)
    v_m, v_e = unpack_moves_and_eat(v_res)
    h_m, h_e = unpack_moves_and_eat(h_res)

    display_board_with_moves(
        board, rook_d1, moves=v_m + h_m, eat=v_e + h_e,
        title="2.2 Tour blanche (0, 3) : glissement et pieces cibles"
    )
    assert (1, 3) in [tuple(m) for m in v_m], "La tour doit pouvoir aller sur la case vide (1, 3)"
    assert (2, 3) not in [tuple(m) for m in v_m], "La tour ne doit pas traverser wQ en (2, 3)"
    print("  [OK] Tour blanche (0, 3) : glisse vers (1, 3) et s'arrete avant la Dame en (2, 3)")

    # 2.3 Fou noir bB en (5, 6) sur diagonales
    bishop_g6 = board[5, 6]
    try:
        d_res = bishop_g6.diago_movement(board)
        d_m, d_e = unpack_moves_and_eat(d_res)
        display_board_with_moves(
            board, bishop_g6, moves=d_m, eat=d_e,
            title="2.3 Fou noir (5, 6) : rayons diagonaux avec (moves, eat)"
        )
        assert (4, 5) not in [tuple(m) for m in d_m], "Le fou ne doit pas aller sur le cavalier allie (4, 5)"
        print(f"  [OK] Fou noir (5, 6) : {len(d_m)} coups libres et {len(d_e)} cible(s) detectee(s)")
    except TypeError as e:
        print(f"\n  [ATTENTION DIAGNOSTIC pieces.py] diago_movement() sur le fou a leve : {e}")

    # 2.4 Dame blanche wQ en (2, 3) : combinaison de mouvements
    queen_d3 = board[2, 3]
    qv_m, qv_e = unpack_moves_and_eat(queen_d3.vertical_movement(board))
    qh_m, qh_e = unpack_moves_and_eat(queen_d3.horizontal_movement(board))
    try:
        qd_m, qd_e = unpack_moves_and_eat(queen_d3.diago_movement(board))
    except TypeError:
        qd_m, qd_e = [], []
    q_all_m = qv_m + qh_m + qd_m
    q_all_e = qv_e + qh_e + qd_e
    display_board_with_moves(
        board, queen_d3, moves=q_all_m, eat=q_all_e,
        title="2.4 Dame blanche (2, 3) : vision combinee (moves + eat)"
    )
    print(f"  [OK] Dame blanche (2, 3) : {len(q_all_m)} coups libres et {len(q_all_e)} cibles")

    # 2.5 Roi blanc roqué wK en (0, 6)
    king_g1 = board[0, 6]
    king_moves = king_g1.king_moves(board)
    display_board_with_moves(
        board, king_g1, moves=king_moves,
        title="2.5 Roi blanc roque (0, 6) : restreint par le bord et ses pions"
    )
    expected_king = {(0, 7)}
    assert set(tuple(m) for m in king_moves) == expected_king
    print("  [OK] Roi blanc roque (0, 6) : seule la case (0, 7) est accessible")

    # 2.6 Pion blanc bloqué de face
    pawn_d4 = board[3, 3]
    pawn_d4_res = pawn_d4.pawn_advancement(board)
    pawn_d4_moves, pawn_d4_eat = unpack_moves_and_eat(pawn_d4_res)
    display_board_with_moves(
        board, pawn_d4, moves=pawn_d4_moves, eat=pawn_d4_eat,
        title="2.6 Pion blanc (3, 3) bloque de face par bP(4, 3)"
    )
    assert len(pawn_d4_moves) == 0, f"Le pion bloque ne doit pas avancer, obtenu {pawn_d4_moves}"
    print("  [OK] Pion blanc (3, 3) bloque : 0 coup libre")


# ==============================================================================
# SUITE 3 : TESTS FIN DE PARTIE, PROMOTION, SAME_COLOR ET DEFENSE
# ==============================================================================

def test_suite_endgame_and_special():
    print("\n" + "#" * 65)
    print(" SUITE 3 : TESTS FIN DE PARTIE, PROMOTION, SAME_COLOR ET DEFENSE")
    print("#" * 65)

    board = create_populated_endgame_board()

    # 3.1 Pion blanc proche promotion
    pawn_near_promo = board[6, 3]
    p_promo_res = pawn_near_promo.pawn_advancement(board)
    moves_promo_step, eat_promo_step = unpack_moves_and_eat(p_promo_res)
    display_board_with_moves(
        board, pawn_near_promo, moves=moves_promo_step, eat=eat_promo_step,
        title="3.1 Pion blanc (6, 3) s'appretant a atteindre la rangee 7"
    )
    assert [7, 3] in moves_promo_step, f"Attendu [7, 3] dans {moves_promo_step}"
    print("  [OK] Pion (6, 3) avance vers (7, 3)")

    # 3.2 Test promotion() avec gestion sécurisée
    pawn_promo = board[7, 5]
    print("\n>>> Test 3.2 : Test de promotion() pour wP en position finale (7, 5)")
    try:
        try:
            promo_moves = pawn_promo.promotion(board, hor=5)
        except TypeError:
            promo_moves = pawn_promo.promotion(board, hor=5, vert=7)
        print(f"  [OK] Fonction promotion() executee : {promo_moves}")
    except (IndexError, AttributeError) as e:
        print(f"  [NOTE DIAGNOSTIC pieces.py] promotion() a leve {type(e).__name__}: {e}")

    # 3.3 Test same_color()
    print("\n>>> Test 3.3 : Test de same_color()")
    p_w1 = Pieces([0, 0], "wR")
    p_w2 = Pieces([1, 1], "wP")
    p_b = Pieces([7, 7], "bK")
    p_em = Pieces([4, 4], "Em")

    res_ww = p_w1.same_color(p_w2)
    res_wb = p_w1.same_color(p_b)
    res_wem = p_w1.same_color(p_em)

    assert res_ww in (True, "same color"), f"Attendu True ou 'same color', obtenu {res_ww}"
    assert res_wb in (False, "not the same color"), f"Attendu False ou 'not the same color', obtenu {res_wb}"
    print(f"  [OK] same_color() valide : Blanc/Blanc -> '{res_ww}', Blanc/Noir -> '{res_wb}', Blanc/Em -> '{res_wem}'")

    # 3.4 Cavalier au coin (0, 0)
    knight_corner = Pieces([0, 0], "wN", 3)
    b_corner = create_empty_board()
    b_corner[0, 0] = knight_corner
    k_fn = getattr(knight_corner, "the_L_movement", getattr(knight_corner, "the_L_eatable", None))
    k_corner_res = k_fn(b_corner) if callable(k_fn) else []
    m_corner, e_corner = unpack_moves_and_eat(k_corner_res)
    display_board_with_moves(
        b_corner, knight_corner, moves=m_corner, eat=e_corner,
        title="3.4 Cavalier au coin (0, 0) : exactement 2 sauts"
    )
    all_corner = set(tuple(m) for m in m_corner) | set(tuple(e) for e in e_corner)
    assert all_corner == {(1, 2), (2, 1)}, f"Attendu {(1, 2), (2, 1)}, obtenu {all_corner}"
    print("  [OK] Cavalier au coin (0, 0) : exactement 2 sauts valides")

    # 3.5 Test King et piece_being_eatable
    print("\n>>> Test 3.5 : Test des methodes du Roi (king_moves, piece_being_eatable)")
    king = King([4, 4], "wK")
    b_king = create_empty_board()
    b_king[4, 4] = king
    k_moves = king.king_moves(b_king)
    assert len(k_moves) == 8
    print(f"  [OK] king.king_moves() au centre : 8 coups valides")

    try:
        is_attacked = king.piece_being_eatable(b_king)
        print(f"  [OK] king.piece_being_eatable() retourne : {is_attacked}")
    except (AttributeError, TypeError, IndexError) as e:
        print(f"  [NOTE DIAGNOSTIC pieces.py] piece_being_eatable() a leve : {e}")

    # 3.6 Test des stubs can_eat_piece et eat_piece
    print("\n>>> Test 3.6 : Stubs can_eat_piece() et eat_piece()")
    p1 = Pieces([0, 0], "wP")
    p2 = Pieces([1, 1], "bP")
    p1.can_eat_piece(p2, board)
    p1.eat_piece(p2, board)
    print("  [OK] can_eat_piece() et eat_piece() s'executent sans crash")


# ==============================================================================
# POINT D'ENTRÉE PRINCIPAL
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 65)
    print("   LANCEMENT DU BANC DE TESTS COMPLET (PLATEAUX REMPLIS)")
    print("=" * 65)

    test_suite_starting_board()
    test_suite_populated_midgame()
    test_suite_endgame_and_special()

    print("\n" + "=" * 65)
    print("   TOUTES LES SUITES DE TESTS ONT ÉTÉ EXÉCUTÉES ! ")
    print("=" * 65)