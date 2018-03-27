from constants import *


class Chess:
    def __init__(self, fen=DEFAULT_FEN):
        self.board = [None] * 128
        self.kings = {WHITE: EMPTY, BLACK: EMPTY}
        self.castling = {WHITE: 0, BLACK: 0}
        self.history = []

        self.load(fen)

    def load(self, fen):
        tokens = fen.split()
        square = 0

        for piece in tokens[0]:
            if piece == '/':
                square += 8
            elif piece.isdigit():
                square += int(piece)
            else:
                color = WHITE if piece.isupper() else BLACK
                self.place_piece(Piece(piece.lower(), color), Chess.get_san(square))
                square += 1

        self.turn = tokens[1]

        if 'K' in tokens[2]:
            self.castling[WHITE] |= Bits.KSIDE_CASTLE.value
        if 'Q' in tokens[2]:
            self.castling[WHITE] |= Bits.QSIDE_CASTLE.value
        if 'k' in tokens[2]:
            self.castling[BLACK] |= Bits.KSIDE_CASTLE.value
        if 'q' in tokens[2]:
            self.castling[BLACK] |= Bits.QSIDE_CASTLE.value

        self.ep_square = EMPTY if tokens[3] == '-' else SQUARES[tokens[3]].value
        self.half_moves = int(tokens[4])
        self.move_number = int(tokens[5])

    def generate_fen(self):
        empty = 0
        fen = ""

        i = SQUARES.a8.value - 1
        while i <= SQUARES.h1.value:
            i += 1

            if not self.board[i]:
                empty += 1
            else:
                if empty > 0:
                    fen += str(empty)
                    empty = 0
                
                type = self.board[i].type
                color = self.board[i].color

                fen += type.upper() if color == WHITE else type

            if (i+1) & 0x88:
                if empty > 0:
                    fen += str(empty)

                if i != SQUARES.h1.value:
                    fen += '/'

                empty = 0
                i += 8

        # add castling permissions
        cflags = ''
        if self.castling[WHITE] & Bits.KSIDE_CASTLE.value:
            cflags += 'K'
        if self.castling[WHITE] & Bits.QSIDE_CASTLE.value:
            cflags += 'Q'
        if self.castling[BLACK] & Bits.KSIDE_CASTLE.value:
            cflags += 'k'
        if self.castling[BLACK] & Bits.QSIDE_CASTLE.value:
            cflags += 'q'

        # if castling flag is empty, replace with dash
        cflags = cflags or '-'

        epflags = '-' if self.ep_square == EMPTY else Chess.get_san(self.ep_square)

        return ' '.join(
            [fen, self.turn, cflags, epflags, str(self.half_moves), str(self.move_number)])
    
    def get_piece(square):
        return self.board[SQUARES[square].value]

    def place_piece(self, piece, square):
        sq = SQUARES[square].value
        self.board[sq] = piece

        if piece.type == KING:
            self.kings[piece.color] = sq

    def remove_piece(self, square):
        piece = self.get_piece(square)
        self.board[SQUARES[square].value] = None

        if piece and piece == KING:
            self.kings[piece.color] = EMPTY

        return piece

    def print(self):
        print("   +" + '-'*24 + '+')

        i = SQUARES.a8.value - 1
        while i <= SQUARES.h1.value:
            i += 1

            if Chess.get_file(i) == 0:
                print(" {} |".format(Chess.get_rank(i)), end='')

            if not self.board[i]:
                print(" . ", end='')
            else:
                type = self.board[i].type
                color = self.board[i].color

                print(' ' + (type.upper() if color == WHITE else type) + ' ', end='')

            if (i+1) & 0x88:
                print('|')
                i += 8

        print("   +" + '-'*24 + '+')
        print("     " + "  ".join(list("abcdefgh")))

    def generate_moves(self, legal=True, single_square=""):
        def add_move(m_from, m_to, flags):
            moves = []

            if ((Chess.get_rank(m_to) == RANK_8 or Chess.get_rank(m_to) == RANK_1) and
                    self.board[m_from].type == PAWN):
                for piece in [QUEEN, ROOK, BISHOP, KNIGHT]:
                    moves.append(Move(self.board, self.turn, m_from, m_to, flags, piece))
            else:
                moves.append(Move(self.board, self.turn, m_from, m_to, flags))

            return moves

        moves = []
        us = self.turn
        them = Chess.swap_color(us)
        second_rank = {'b': RANK_7, 'w': RANK_2}

        i = SQUARES.a8.value - 1
        last_sq = SQUARES.h1.value

        # if we're only exploring the moves for a single square
        if single_square:
            i = last_sq = SQUARES[single_square].value - 1

        while i <= last_sq:
            i += 1
            # if we ran off the end of the board
            if i & 0x88:
                i += 7
                continue

            piece = self.board[i]
            # if empty square or enemy piece
            if not piece or piece.color != us:
                continue

            if piece.type == PAWN:
                # single square non-capture
                square = i + PAWN_OFFSETS[us][0]

                # if square is empty
                if not self.board[square]:
                    moves += add_move(i, square, Bits.NORMAL.value)

                    # double square
                    square = i + PAWN_OFFSETS[us][1]

                    if second_rank[us] == Chess.get_rank(i) and not self.board[square]:
                        moves += add_move(i, square, Bits.BIG_PAWN.value)

                # pawn captures
                for j in range(2, 4):
                    square = i + PAWN_OFFSETS[us][j]

                    # if end of board
                    if square & 0x88:
                        continue

                    # if square is occupied by enemy piece
                    if self.board[square] and self.board[square].color == them:
                        moves += add_move(i, square, Bits.CAPTURE.value)
                    # if capture square is en passant square
                    elif square == self.ep_square:
                        moves += add_move(i, square, Bits.EP_CAPTURE.value)
            else:
                for offset in PIECE_OFFSETS[piece.type]:
                    square = i

                    while True:
                        square += offset

                        # break if end of board
                        if square & 0x88:
                            break

                        if not self.board[square]:
                            moves += add_move(i, square, Bits.NORMAL.value)
                        else:
                            if self.board[square].color == them:
                                moves += add_move(i, square, Bits.CAPTURE.value)

                            break

                        # break if knight or king
                        if piece.type in ['n', 'k']:
                            break

        if not single_square or last_sq == self.kings[us]:
            # kingside castling
            if self.castling[us] & Bits.KSIDE_CASTLE.value:
                castling_from = self.kings[us]
                castling_to = castling_from + 2

                # if the path is clear, we're not in check and won't be in check
                if (not self.board[castling_from+1] and
                        not self.board[castling_to] and
                        not self.attacked(them, self.kings[us]) and
                        not self.attacked(them, castling_from+1) and
                        not self.attacked(them, castling_to)):
                    moves += add_move(self.kings[us], castling_to, Bits.KSIDE_CASTLE.value)

            # queenside castling
            if self.castling[us] & Bits.QSIDE_CASTLE.value:
                castling_from = self.kings[us]
                castling_to = castling_from - 2

                # if the path is clear, we're not in check and won't be in check
                if (not self.board[castling_from-1] and
                        not self.board[castling_from-2] and
                        not self.board[castling_from-3] and
                        not self.attacked(them, self.kings[us]) and
                        not self.attacked(them, castling_from-1) and
                        not self.attacked(them, castling_to)):
                    moves += add_move(self.kings[us], castling_to, Bits.QSIDE_CASTLE.value)

        # if we're allowing illegal moves
        if not legal:
            return moves

        # filter out illegal moves
        legal_moves = []
        for move in moves:
            self.make_move(move)

            if not self.king_attacked(us):
                legal_moves.append(move)

            undo_move()

        return legal_moves

    def attacked(self, color, square):
        i = SQUARES.a8.value - 1
        while i <= SQUARES.h1.value:
            i += 1

            # if we ran off the end of the board
            if i & 0x88:
                i += 7
                continue
            
            # if empty square or wrong color
            if not self.board[i] or self.board[i].color != color:
                continue

            piece = self.board[i]
            difference = i - square
            index = difference + 119

            if ATTACKS[index] & (1 << SHIFTS[piece.type]):
                if piece.type == PAWN:
                    if difference > 0:
                        if piece.color == WHITE:
                            return True
                    else:
                        if piece.color == BLACK:
                            return True
                    continue

                # if knight or king
                if piece.type in ['n', 'k']:
                    return True

                offset = RAYS[index]
                j = i + offset

                blocked = False
                while j != square:
                    if not self.board[j]:
                        blocked = True
                        break
                    j += offset

                if not blocked:
                    return True

        return False

    def king_attacked(self, color):
        return attacked(Chess.swap_color(color), self.kings[color])

    def in_check(self):
        return self.king_attacked(self.turn)

    def in_checkmate(self):
        return self.in_check() and not self.generate_moves()

    def in_stalemate(self):
        return not self.in_check() and bool(self.generate_moves())

    def insufficient_material(self):
        pieces = {}
        bishops = []
        num_pieces = 0
        sq_color = 0

        i = SQUARES.a8 - 1
        while i <= SQUARES.h1:
            i += 1
            sq_color = (sq_color + 1) % 2

            if i & 0x88:
                i += 7
                continue

            piece = self.board[i]

            if piece:
                pieces[piece.type] = pieces.get(piece.type, 0) + 1

                if piece.type == BISHOP:
                    bishops.append(sq_color)

                num_pieces += 1

        # K vs. K
        if num_pieces == 2:
            return True
        # K vs. KN or K vs. KB
        elif num_pieces == 3 and (pieces[BISHOP] == 1 or pieces[KNIGHT] == 1):
            return True:
        # KB vs. KB where any number of bishops are all the same color
        elif num_pieces == (pieces[BISHOP]+2):
            b_sum = sum(bishops)

            if sum == 0 or sum == len(bishops):
                return True

        return False

    def in_threefold_repetition(self):
        pass

    @staticmethod
    def get_san(i):
        return "abcdefgh"[Chess.get_file(i)] + "87654321"[Chess.get_rank(i)]

    @staticmethod
    def get_file(i):
        return i & 15

    @staticmethod
    def get_rank(i):
        return i >> 4

    @staticmethod
    def swap_color(color):
        return WHITE if color == BLACK else BLACK


class Piece:
    def __init__(self, type, color):
        self.type = type
        self.color = color


class Move:
    def __init__(self, board, color, m_from, m_to, flags, promotion=0):
        self.color = color
        self.m_from = m_from
        self.m_to = m_to
        self.flags = flags
        self.promotion = promotion
        self.piece = board[m_from].type
        self.captured = ''
        
        if promotion:
            self.flags |= Bits.PROMOTION.value

        if board[m_to]:
            self.captured = board[m_to].type
        elif flags & Bits.EP_CAPTURE.value:
            self.captured = PAWN
