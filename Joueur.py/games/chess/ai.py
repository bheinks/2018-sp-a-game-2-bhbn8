# This is where you build your AI for the Chess game.

from random import choice
from time import sleep

# local imports
from joueur.base_ai import BaseAI
from games.chess.board import Board, Player, Move

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
# <<-- /Creer-Merge: imports -->>

class AI(BaseAI):
    """ The basic AI functions that are the same between games. """

    def get_name(self):
        """ This is the name you send to the server so your AI will control the player named this string.

        Returns
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "Chess Python Player" # REPLACE THIS WITH YOUR TEAM NAME
        # <<-- /Creer-Merge: get-name -->>

    def start(self):
        """ This is called once the game starts and your AI knows its playerID and game. You can initialize your AI here.
        """
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        
        # our local board representation
        self.board = Board(self.game.fen)

        # our local player representation
        self.local_player = Player(self.board, self.player.color)

        # True when we ditch a new board state, False otherwise
        self.rerun = False

        # <<-- /Creer-Merge: start -->>

    def game_updated(self):
        """ This is called every time the game's state updates, so if you are tracking anything you can update it here.
        """
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic
        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why you won or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your end logic
        # <<-- /Creer-Merge: end -->>
    def run_turn(self):
        """ This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
        """
        # <<-- Creer-Merge: runTurn -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.

        # if we're not evaluating a new state, don't update local board again
        if len(self.game.moves) > 0 and not self.rerun:
            self.update_last_move()

        # create new board state and player
        new_board = Board(self.board.board2fen())
        new_local_player = Player(new_board, self.player.color)

        # select a random move from all possible moves
        local_move = choice(new_local_player.get_all_moves())

        return self.simulate_move(new_board, new_local_player, local_move)

        # <<-- /Creer-Merge: runTurn -->>

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.

    def simulate_move(self, board, local_player, local_move):
        piece = local_move.piece
        promotion_type = local_move.promotion
        x, y = local_move.x, local_move.y

        possible_moves = piece.get_moves()
        old_coord = piece.x, piece.y
        old_type = piece.type

        piece.move(local_move)

        # discard state if we end up in check
        for p in local_player.pieces.values():
            if p.type == 'King' and p.in_check():
                self.rerun = True
                return False

        # otherwise it's a valid move. find remote piece and move
        for p in self.player.pieces:
            if Board.fr2coord(p.file, p.rank) == old_coord:
                p.move(*Board.coord2fr(x, y), promotion_type)
                break

        # update board state and player
        self.board = board
        self.local_player = local_player

        print("Available moves:")
        for move in possible_moves:
            old_file, old_rank = Board.coord2fr(*old_coord)

            print("{} {} from {}{} to {}".format(
                piece.color,
                old_type,
                old_file, old_rank,
                move))

        print()

        print("Selected move:")
        print("{} {} from {}{} to {}".format(
            piece.color,
            old_type,
            old_file, old_rank,
            local_move))

        print('-'*24)
        print()

        assert self.game.fen == board.board2fen()

        self.rerun = False
        return True

    def update_last_move(self):
        #move = self.game.moves[-1]
        #from_x, from_y = Board.fr2coord(move.from_file, move.from_rank)
        #to_x, to_y = Board.fr2coord(move.to_file, move.to_rank)
        #piece = self.board.get_piece(from_x, from_y)

        #piece.move(Move(piece, to_x, to_y, move.promotion))
        self.board = Board(self.game.fen)
        self.local_player = Player(self.board, self.player.color)

    def print_current_board(self):
        """Prints the current board using pretty ASCII art
        Note: you can delete this function if you wish
        """

        # iterate through the range in reverse order
        for r in range(9, -2, -1):
            output = ""
            if r == 9 or r == 0:
                # then the top or bottom of the board
                output = "   +------------------------+"
            elif r == -1:
                # then show the ranks
                output = "     a  b  c  d  e  f  g  h"
            else:  # board
                output = " " + str(r) + " |"
                # fill in all the files with pieces at the current rank
                for file_offset in range(0, 8):
                    # start at a, with with file offset increasing the char
                    f = chr(ord("a") + file_offset)
                    current_piece = None
                    for piece in self.game.pieces:
                        if piece.file == f and piece.rank == r:
                            # then we found the piece at (file, rank)
                            current_piece = piece
                            break

                    code = "."  # default "no piece"
                    if current_piece:
                        # the code will be the first character of their type
                        # e.g. 'Q' for "Queen"
                        code = current_piece.type[0]

                        if current_piece.type == "Knight":
                            # 'K' is for "King", we use 'N' for "Knights"
                            code = "N"

                        if current_piece.owner.id == "1":
                            # the second player (black) is lower case.
                            # Otherwise it's uppercase already
                            code = code.lower()

                    output += " " + code + " "

                output += "|"
            print(output)

    # <<-- /Creer-Merge: functions -->>
