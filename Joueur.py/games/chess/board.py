from string import ascii_lowercase


class Board:
    """Represents a local board instance."""

    # default starting FEN string
    DEFAULT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    # map FEN characters to piece types
    FEN_PIECE_MAP = {
        'p': "Pawn",
        'n': "Knight",
        'b': "Bishop",
        'r': "Rook",
        'q': "Queen",
        'k': "King"
    }

    def __init__(self, fen=DEFAULT_FEN):
        """Initializes a board instance.

        Args:
            fen: The FEN string we're parsing.

        Returns:
            A fully initialized board instance.
        """

        # split FEN on whitespace to separate the board from other fields
        fen = fen.split()

        # represent our board as a 2d list, pieces as a dictionary
        self._board, self.pieces = self.fen2board(fen[0])

        # other FEN fields
        self.turn = fen[1]
        self.castle = fen[2]
        self.en_passant = fen[3]
        self.halfmove_clock = int(fen[4])
        self.fullmove_counter = int(fen[5])

    def get_piece(self, x, y):
        """Retrieves a piece from the board.

        Args:
            x: The x coordinate.
            y: The y coordinate.

        Returns:
            (Piece|None): The object at board location x, y.

        Raises:
            IndexError: If x or y are outside the bounds of the board.
        """

        if 0 <= x < 8 and 0 <= y < 8:
            return self._board[y][x]

        raise IndexError

    def set_piece(self, x, y, piece):
        """Sets a piece's location on the board.

        Args:
            x: The x coordinate.
            y: The y coordinate.
            piece: The piece that we're setting the location of.
        """

        # remove our piece from original position
        self._board[piece.y][piece.x] = None

        # remove enemy piece if captured
        enemy_piece = self.get_piece(x, y)
        if enemy_piece:
            self.remove_piece(x, y, enemy_piece)

        # update board to new piece position
        self._board[y][x] = piece

        # update piece x and y values
        piece.x, piece.y = x, y

    def remove_piece(self, x, y, piece):
        """Removes a piece from the board.

        Args:
            x: The x coordinate.
            y: The y coordinate.
            piece: The piece that we're removing.
        """

        # remove from board
        self._board[piece.y][piece.x] = None

        # remove from pieces
        del self.pieces[piece.color][piece.id]

    def print(self):
        """Prints a board to the screen."""

        print("   +" + '-'*24 + '+')

        for i, rank in enumerate(self._board):
            print(" {} |".format(8-i), end='')

            for piece in rank:
                print(" {} ".format(piece or '.'), end='')

            print('|')

        print("   +" + '-'*24 + '+')
        print("     " + "  ".join(list(ascii_lowercase)[:8]))

    def fen2board(self, fen):
        """Converts a FEN string to a board instance.

        Args:
            fen: A valid FEN string.

        Returns:
            (list, dict): A 2d list and dictionary representing the board and
                pieces, respectively.
        """

        board = []
        pieces = {"White": {}, "Black": {}}
        fen = fen.split('/')

        # unique piece ID
        id = 0

        for y in range(len(fen)):
            rank = []

            for piece in fen[y]:
                # if digit, add that number in None objects to rank
                if piece.isdigit():
                    rank.extend([None for _ in range(int(piece))])
                # otherwise, add new Piece object
                else:
                    # if uppercase, piece is white
                    if piece.isupper():
                        color = "White"
                        enemy_color = "Black"

                        # piece has moved if outside of starting rank
                        if piece == "P":
                            has_moved = y != 6
                        else:
                            has_moved = y != 7
                    # black otherwise
                    else:
                        color = "Black"
                        enemy_color = "White"

                        # piece has moved if outside of starting rank
                        if piece == "P":
                            has_moved = y != 1
                        else:
                            has_moved = y != 0

                    # create piece
                    piece = Piece(self, id, len(rank), y,
                        Board.FEN_PIECE_MAP[piece.lower()],
                        color, enemy_color, has_moved)

                    rank.append(piece)
                    pieces[color][id] = piece
                    id += 1

            board.append(rank)

        return board, pieces

    def board2fen(self):
        """Converts a board instance to a FEN string.

        Returns:
            str: A FEN string representing the board instance.
        """

        fen = []

        for row in self._board:
            # keep count of empty squares
            counter = 0
            section = ""

            for p in row:
                if p:
                    if counter > 0:
                        section += str(counter)
                        counter = 0

                    section += str(p)
                else:
                    counter += 1

            if counter > 0:
                section += str(counter)

            fen.append(section)

        return "{} {} {} {} {} {}".format(
            '/'.join(fen),
            self.turn,
            self.castle,
            self.en_passant,
            self.halfmove_clock,
            self.fullmove_counter)

    def get_new_state(self):
        """Generates a new board state.

        Returns:
            Board: The new state.
        """

        return Board(self.board2fen())

    @staticmethod
    def coord2fr(x, y):
        """Converts x, y coordinates to file and rank.

        Args:
            x: The x coordinate.
            y: The y coordinate.

        Returns:
            (str, str): The file and rank respectively.
        """

        return ascii_lowercase[x], str(8-y)

    @staticmethod
    def fr2coord(file, rank):
        """Converts file and rank to x, y coordinates.

        Args:
            file: The file.
            rank: The rank.

        Returns:
            (int, int): The x and y coordinates respectively.
        """

        return ord(file)-97, 8-rank


class Piece:
    """Represents a chess piece instance."""

    # options for pawn promotion
    PROMOTION_OPTIONS = ("Knight", "Bishop", "Rook", "Queen")

    def __init__(self, board, id, x, y, type, color, enemy_color, has_moved):
        """Initializes a piece instance.

        Args:
            board: The board instance.
            id: A unique id.
            x: The piece's x coordinate.
            y: The piece's y coordinate.
            type: The piece's type (pawn, rook, knight, etc.).
            color: Player color (White or Black).
            enemy_color: Enemy color (White or Black).
            has_moved: Whether or not the piece has moved from its starting location.

        Returns:
            A fully initialized piece instance.
        """

        self.board = board
        self.id = id
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.enemy_color = enemy_color
        self.has_moved = has_moved

    def __str__(self):
        if self.type == "Knight":
            code = 'N'
        else:
            code = self.type[0]

        return code.lower() if self.color == "Black" else code.upper()

    def __repr__(self):
        return str(self)

    def _get_diagonal_moves(self, start_x, end_x, step_x, start_y, end_y, step_y):
        legal_moves = []
        board = self.board

        # for every diagonal x and y coordinate
        for x, y in zip(range(start_x, end_x, step_x), range(start_y, end_y, step_y)):
            move = x, y

            try:
                piece = board.get_piece(*move)

                # if square is empty
                if not piece:
                    legal_moves.append(Move(self, *move))

                # else if square has an enemy piece
                elif self.is_enemy(piece):
                    legal_moves.append(Move(self, *move))
                    return legal_moves

                # else square has a friendly piece
                else:
                    return legal_moves

            except IndexError:
                pass

        return legal_moves

    def _get_horizontal_moves(self, start, end, step):
        legal_moves = []
        board = self.board

        for x in range(start, end, step):
            move = x, self.y

            try:
                piece = board.get_piece(*move)

                # if square is empty
                if not piece:
                    legal_moves.append(Move(self, *move))

                # else if square has an enemy piece
                elif self.is_enemy(piece):
                    legal_moves.append(Move(self, *move))
                    return legal_moves

                # else square has a friendly piece
                else:
                    return legal_moves

            except IndexError:
                pass

        return legal_moves

    def _get_vertical_moves(self, start, end, step):
        legal_moves = []
        board = self.board

        for y in range(start, end, step):
            move = self.x, y

            try:
                piece = board.get_piece(*move)

                # if square is empty
                if not piece:
                    legal_moves.append(Move(self, *move))

                # else if square has an enemy piece
                elif self.is_enemy(piece):
                    legal_moves.append(Move(self, *move))
                    return legal_moves

                # else square has a friendly piece
                else:
                    return legal_moves

            except IndexError:
                pass

        return legal_moves

    # TODO: implement en passant
    def _get_pawn_moves(self):
        legal_moves = []
        board = self.board
        x, y = self.x, self.y

        if self.color == "White":
            # check movement north 1
            move = x, y-1

            try:
                if not board.get_piece(*move):
                    if y-1 == 0:
                        for promotion in Piece.PROMOTION_OPTIONS:
                            legal_moves.append(Move(self, *move, promotion))
                    else:
                        legal_moves.append(Move(self, *move))

                        # if pawn has not yet moved, check movement north 2
                        if not self.has_moved:
                            move = x, y-2
                            
                            try:
                                if not board.get_piece(*move):
                                    en_passant = ''.join(Board.coord2fr(x, y-1))
                                    legal_moves.append(Move(self, *move, en_passant=en_passant))
                            except IndexError:
                                pass

            except IndexError:
                pass

            possible_captures = (
                (x-1, y-1), # west 1, north 1
                (x+1, y-1)  # east 1, north 1
            )

            # check possible captures
            for move in possible_captures:
                try:
                    piece = board.get_piece(*move)

                    if piece and self.is_enemy(piece):
                        if y-1 == 0:
                            for promotion in Piece.PROMOTION_OPTIONS:
                                legal_moves.append(Move(self, *move, promotion))
                        else:
                            legal_moves.append(Move(self, *move))
                    elif self.board.en_passant == ''.join(Board.coord2fr(*move)):
                        legal_moves.append(Move(self, *move))

                except IndexError:
                    pass
        else:
            # check movement south 1
            move = x, y+1

            try:
                if not board.get_piece(*move):
                    if y+1 == 7:
                        for promotion in Piece.PROMOTION_OPTIONS:
                            legal_moves.append(Move(self, *move, promotion))
                    else:
                        legal_moves.append(Move(self, *move))

                        # if pawn has not yet moved, check movement south 2
                        if not self.has_moved:
                            move = x, y+2
                            
                            try:
                                if not board.get_piece(*move):
                                    en_passant = ''.join(Board.coord2fr(x, y+1))
                                    legal_moves.append(Move(self, *move, en_passant=en_passant))
                            except IndexError:
                                pass

            except IndexError:
                pass

            possible_captures = (
                (x-1, y+1), # west 1, south 1
                (x+1, y+1)  # east 1, south 1
            )

            # check possible captures
            for move in possible_captures:
                try:
                    piece = board.get_piece(*move)

                    if piece and self.is_enemy(piece):
                        if y+1 == 7:
                            for promotion in Piece.PROMOTION_OPTIONS:
                                legal_moves.append(Move(self, *move, promotion))
                        else:
                            legal_moves.append(Move(self, *move))
                    elif self.board.en_passant == ''.join(Board.coord2fr(*move)):
                        legal_moves.append(Move(self, *move))

                except IndexError:
                    pass

        return legal_moves

    def _get_knight_moves(self):
        legal_moves = []
        board = self.board
        x, y = self.x, self.y

        possible_moves = (
            (x+1, y-2), # east 1, north 2
            (x+2, y-1), # east 2, north 1
            (x+2, y+1), # east 2, south 1
            (x+1, y+2), # east 1, south 2
            (x-1, y+2), # west 1, south 2
            (x-2, y+1), # west 2, south 1
            (x-2, y-1), # west 2, north 1
            (x-1, y-2)  # west 1, north 2
        )

        # check possible moves
        for move in possible_moves:
            try:
                piece = board.get_piece(*move)
     
                if not piece or self.is_enemy(piece): 
                    legal_moves.append(Move(self, *move))

            except IndexError:
                pass

        return legal_moves

    def _get_bishop_moves(self):
        legal_moves = []
        x, y = self.x, self.y

        # check northeast
        legal_moves.extend(self._get_diagonal_moves(x+1, 8, 1, y-1, -1, -1))

        # check southeast
        legal_moves.extend(self._get_diagonal_moves(x+1, 8, 1, y+1, 8, 1))

        # check southwest
        legal_moves.extend(self._get_diagonal_moves(x-1, -1, -1, y+1, 8, 1))

        # check northwest
        legal_moves.extend(self._get_diagonal_moves(x-1, -1, -1, y-1, -1, -1))

        return legal_moves

    def _get_rook_moves(self):
        legal_moves = []
        x, y = self.x, self.y

        # check east
        legal_moves.extend(self._get_horizontal_moves(x+1, 8, 1))

        # check south
        legal_moves.extend(self._get_vertical_moves(y+1, 8, 1))

        # check west
        legal_moves.extend(self._get_horizontal_moves(x-1, -1, -1))

        # check north
        legal_moves.extend(self._get_vertical_moves(y-1, -1, -1))

        return legal_moves

    def _get_queen_moves(self):
        # queen moves are just bishop + rook moves
        return self._get_bishop_moves() + self._get_rook_moves()

    # TODO: implement castling
    def _get_king_moves(self):
        legal_moves = []
        
        # check adjacent squares (+2 because range upper bound is exclusive)
        for y in range(self.y-1, self.y+2):
            for x in range(self.x-1, self.x+2):
                # if not the square we're in
                if not (x == self.x and y == self.y):
                    move = x, y

                    try:
                        piece = self.board.get_piece(*move)

                        if not piece or self.is_enemy(piece):
                            legal_moves.append(Move(self, *move))

                    except IndexError:
                        pass

        return legal_moves

    def in_check(self):
        # for every enemy piece
        for p in self.board.pieces[self.enemy_color].values():
            # if an enemy can move to king location, we're in check
            if any(self.x == m.x and self.y == m.y for m in p.get_moves()):
                return True

        return False

    def get_moves(self):
        PIECE_MOVE_MAP = {
            'Pawn': self._get_pawn_moves,
            'Knight': self._get_knight_moves,
            'Bishop': self._get_bishop_moves,
            'Rook': self._get_rook_moves,
            'Queen': self._get_queen_moves,
            'King': self._get_king_moves
        }

        return PIECE_MOVE_MAP[self.type]()

    def move(self, move):
        if (move.piece.type == "Pawn" and self.board.en_passant == ''.join(
                Board.coord2fr(move.x, move.y))):
            x, y = Board.fr2coord(*list(self.en_passant))
            self.board.remove_piece(x, y)
            print("EN PASSANT")

        self.board.set_piece(move.x, move.y, self)
        self.has_moved = True

        if move.promotion:
            self.type = move.promotion

        self.board.en_passant = move.en_passant or "-"

    def is_enemy(self, other):
        return self.color != other.color


class Player:
    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.pieces = board.pieces[color]

    def get_all_moves(self):
        #return [m for m in p.get_moves() for p in self.pieces.values()]
        return [m for p in self.pieces.values() for m in p.get_moves()]


class Move:
    def __init__(self, piece, x, y, promotion="", en_passant=""):
        self.piece = piece
        self.x = x
        self.y = y
        self.promotion = promotion
        self.en_passant = en_passant

    def __str__(self):
        file, rank = Board.coord2fr(self.x, self.y)
        promotion = ""

        if self.promotion:
            promotion = ", promotion to " + self.promotion

        return file + str(rank) + promotion

    def __repr__(self):
        return str(self)
