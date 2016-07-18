from player import Player
import random

class RandomPlayer(Player):
    """
    A domino player that picks tiles at random.
    """
    
    def select_tile(self):
        """
        Randomly select a tile to play.
        - Select playable tiles from player's hand
        - If there are playable tiles, randomly select one
        - If there are no playable tiles and stack is not empty,
            draw tiles from stack until a playable tile is drawn,
            and select this file
        - If there are no playable tiles and stack is empty,
            pass the player's turn
        Return selected tile (None if player must pass its turn).
        """
        board = self.round.board
        stack = self.round.stack
        possible_tiles = self.hand.check_possibles(board)
        if possible_tiles:
            return random.choice(possible_tiles)
        else:
            while stack:
                self.add_tile(stack.pop(0))
                possible_tiles = self.hand.check_possibles(board)
                if possible_tiles:
                    return possible_tiles[0]
            return None

    def pick_position(self, tile, board):
        """
        Randomly select the position at which the tile should be added
        to the board.
        """
        random.choice([True, False])