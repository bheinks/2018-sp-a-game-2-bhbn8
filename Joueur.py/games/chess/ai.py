# This is where you build your AI for the Chess game.

from random import choice
from time import sleep

# local imports
from joueur.base_ai import BaseAI
from games.chess.board import Board

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

        # represents whether or not we want minimax to return high or low
        self.color_code = 1 if self.player.color == "White" else -1

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

        if len(self.game.moves) > 0:
            self.update_last_move()

        move = self.minimax_root(3, self.board, True)
        piece = move.piece
        promotion_type = move.promotion
        old_coord = piece.x, piece.y

        print(f"Moving {piece} from {old_coord} to {move.x}, {move.y}")

        move.piece.move(move)

        for p in self.player.pieces:
            if Board.fr2coord(p.file, p.rank) == old_coord:
                p.move(*Board.coord2fr(move.x, move.y), promotion_type)
                break

        print("Local board:")
        self.board.print()
        print()
        print("Remote board:")
        self.print_current_board()
        print(f"I am {self.player.color}")

        return True

        # <<-- /Creer-Merge: runTurn -->>

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.

    def simulate_move(self, board, local_move):
        piece = local_move.piece
        #promotion_type = local_move.promotion
        #x, y = local_move.x, local_move.y

        # cannot castle when in check
        if piece.type == "King" and local_move.castling and piece.in_check():
            return False

        piece.move(local_move)

        # discard state if we end up in check
        for p in board.get_pieces():
            if p.type == "King" and p.in_check():
                piece.undo()
                return False

        # otherwise it's a valid move. find remote piece and move
        #for p in self.player.pieces:
        #    if Board.fr2coord(p.file, p.rank) == old_coord:
        #        p.move(*Board.coord2fr(x, y), promotion_type)
        #        break

        #print("Remote board:")
        #self.print_current_board()
        #print()
        #print("Board value: {}".format(self.board.value))
        #print()

        return True

    def minimax_root(self, depth, game, is_max_player):
        best_value = -9999
        best_move = None

        for move in game.get_all_moves(self.player.color):
            if not self.simulate_move(game, move):
                continue

            value = self.minimax(depth-1, game, not is_max_player)
            move.piece.undo()

            #print(f"Value: {value}")
            #print(f"Best value: {best_value}")
            if value >= best_value:
                best_value = value
                best_move = move

        print(f"Best value: {best_value}")

        return best_move

    def minimax(self, depth, game, is_max_player):
        if depth == 0:
            return self.board.value

        if is_max_player:
            best_value = -9999

            for move in game.get_all_moves(self.player.color):
                if not self.simulate_move(game, move):
                    continue

                best_value = max(best_value, self.minimax(depth-1, game, not is_max_player))
                move.piece.undo()
        else:
            best_value = 9999

            for move in game.get_all_moves(self.player.color):
                if not self.simulate_move(game, move):
                    continue

                best_value = min(best_value, self.minimax(depth-1, game, not is_max_player))
                move.piece.undo()

        return best_value

    def update_last_move(self):
        #move = self.game.moves[-1]
        #from_x, from_y = Board.fr2coord(move.from_file, move.from_rank)
        #to_x, to_y = Board.fr2coord(move.to_file, move.to_rank)
        #piece = self.board.get_piece(from_x, from_y)

        #piece.move(Move(piece, to_x, to_y, move.promotion))
        self.board = Board(self.game.fen)

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
