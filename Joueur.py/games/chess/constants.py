from enum import Enum

BLACK = 'b'
WHITE = 'w'

EMPTY = -1

PAWN = 'p'
KNIGHT = 'n'
BISHOP = 'b'
ROOK = 'r'
QUEEN = 'q'
KING = 'k'

SYMBOLS = "pnbrqkPNBRQK"

DEFAULT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

POSSIBLE_RESULTS = ['1-0', '0-1', '1/2-1/2', '*']

PAWN_OFFSETS = {
    'b': [16, 32, 17, 15],
    'w': [-16, -32, -17, -15]
}

PIECE_OFFSETS = {
    'n': [-18, -33, -31, -14,  18, 33, 31,  14],
    'b': [-17, -15,  17,  15],
    'r': [-16,   1,  16,  -1],
    'q': [-17, -16, -15,   1,  17, 16, 15,  -1],
    'k': [-17, -16, -15,   1,  17, 16, 15,  -1]
}

ATTACKS = [
    20, 0, 0, 0, 0, 0, 0, 24,  0, 0, 0, 0, 0, 0,20, 0,
     0,20, 0, 0, 0, 0, 0, 24,  0, 0, 0, 0, 0,20, 0, 0,
     0, 0,20, 0, 0, 0, 0, 24,  0, 0, 0, 0,20, 0, 0, 0,
     0, 0, 0,20, 0, 0, 0, 24,  0, 0, 0,20, 0, 0, 0, 0,
     0, 0, 0, 0,20, 0, 0, 24,  0, 0,20, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0,20, 2, 24,  2,20, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 2,53, 56, 53, 2, 0, 0, 0, 0, 0, 0,
    24,24,24,24,24,24,56,  0, 56,24,24,24,24,24,24, 0,
     0, 0, 0, 0, 0, 2,53, 56, 53, 2, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0,20, 2, 24,  2,20, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0,20, 0, 0, 24,  0, 0,20, 0, 0, 0, 0, 0,
     0, 0, 0,20, 0, 0, 0, 24,  0, 0, 0,20, 0, 0, 0, 0,
     0, 0,20, 0, 0, 0, 0, 24,  0, 0, 0, 0,20, 0, 0, 0,
     0,20, 0, 0, 0, 0, 0, 24,  0, 0, 0, 0, 0,20, 0, 0,
    20, 0, 0, 0, 0, 0, 0, 24,  0, 0, 0, 0, 0, 0,20
]

RAYS = [
     17,  0,  0,  0,  0,  0,  0, 16,  0,  0,  0,  0,  0,  0, 15, 0,
      0, 17,  0,  0,  0,  0,  0, 16,  0,  0,  0,  0,  0, 15,  0, 0,
      0,  0, 17,  0,  0,  0,  0, 16,  0,  0,  0,  0, 15,  0,  0, 0,
      0,  0,  0, 17,  0,  0,  0, 16,  0,  0,  0, 15,  0,  0,  0, 0,
      0,  0,  0,  0, 17,  0,  0, 16,  0,  0, 15,  0,  0,  0,  0, 0,
      0,  0,  0,  0,  0, 17,  0, 16,  0, 15,  0,  0,  0,  0,  0, 0,
      0,  0,  0,  0,  0,  0, 17, 16, 15,  0,  0,  0,  0,  0,  0, 0,
      1,  1,  1,  1,  1,  1,  1,  0, -1, -1,  -1,-1, -1, -1, -1, 0,
      0,  0,  0,  0,  0,  0,-15,-16,-17,  0,  0,  0,  0,  0,  0, 0,
      0,  0,  0,  0,  0,-15,  0,-16,  0,-17,  0,  0,  0,  0,  0, 0,
      0,  0,  0,  0,-15,  0,  0,-16,  0,  0,-17,  0,  0,  0,  0, 0,
      0,  0,  0,-15,  0,  0,  0,-16,  0,  0,  0,-17,  0,  0,  0, 0,
      0,  0,-15,  0,  0,  0,  0,-16,  0,  0,  0,  0,-17,  0,  0, 0,
      0,-15,  0,  0,  0,  0,  0,-16,  0,  0,  0,  0,  0,-17,  0, 0,
    -15,  0,  0,  0,  0,  0,  0,-16,  0,  0,  0,  0,  0,  0,-17
]

SHIFTS = {
    'p': 0,
    'n': 1,
    'b': 2,
    'r': 3,
    'q': 4,
    'k': 5
}

FLAGS = {
    "NORMAL": 'n',
    "CAPTURE": 'c',
    "BIG_PAWN": 'b',
    "EP_CAPTURE": 'e',
    "PROMOTION": 'p',
    "KSIDE_CASTLE": 'k',
    "QSIDE_CASTLE": 'q'
}

class Bits(Enum):
    NORMAL = 1
    CAPTURE = 2
    BIG_PAWN = 4
    EP_CAPTURE = 8
    PROMOTION = 8
    KSIDE_CASTLE = 32
    QSIDE_CASTLE = 64

RANK_1 = 7
RANK_2 = 6
RANK_3 = 5
RANK_4 = 4
RANK_5 = 3
RANK_6 = 2
RANK_7 = 1
RANK_8 = 0

class SQUARES(Enum):
    a8 = 0
    b8 = 1
    c8 = 2
    d8 = 3
    e8 = 4
    f8 = 5
    g8 = 6
    h8 = 7

    a7 = 16
    b7 = 17
    c7 = 18
    d7 = 19
    e7 = 20
    f7 = 21
    g7 = 22
    h7 = 23

    a6 = 32
    b6 = 33
    c6 = 34
    d6 = 35
    e6 = 36
    f6 = 37
    g6 = 38
    h6 = 39

    a5 = 48
    b5 = 49
    c5 = 50
    d5 = 51
    e5 = 52
    f5 = 53
    g5 = 54
    h5 = 55

    a4 = 64
    b4 = 65
    c4 = 66
    d4 = 67
    e4 = 68
    f4 = 69
    g4 = 70
    h4 = 71

    a3 = 80
    b3 = 81
    c3 = 82
    d3 = 83
    e3 = 84
    f3 = 85
    g3 = 86
    h3 = 87

    a2 = 96
    b2 = 97
    c2 = 98
    d2 = 99
    e2 = 100
    f2 = 101
    g2 = 102
    h2 = 103

    a1 = 112
    b1 = 113
    c1 = 114
    d1 = 115
    e1 = 116
    f1 = 117
    g1 = 118
    h1 = 119

ROOKS = {
    'w': [{"square": SQUARES.a1.value, "flag": Bits.QSIDE_CASTLE.value},
          {"square": SQUARES.h1.value, "flag": Bits.KSIDE_CASTLE.value}],
    'b': [{"square": SQUARES.a8.value, "flag": Bits.QSIDE_CASTLE.value},
          {"square": SQUARES.h8.value, "flag": Bits.KSIDE_CASTLE.value}]
}
