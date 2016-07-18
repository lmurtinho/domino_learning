from random_player import RandomPlayer
import random

class HighTilePlayer(RandomPlayer):
    """
    A domino player that always plays the
    tile with the highest value.
    """
    
    def select_tile(self):
        """
        Select a tile to play.
        - If there are tiles to be played in player's hand,
            plays the tile with the highest value
        - If there are no tiles to be played and stack is not empty,
            draws tiles from stack and plays the first playable draw
        - If there are no playable tiles and stack is empty,
            passes
        Return tile to be played (None if no playable tiles)
        """
        board = self.round.board
        stack = self.round.stack
        possible_tiles = self.hand.check_possibles(board)
        if possible_tiles:
            sum_tiles = [sum(tile) for tile in possible_tiles]
            high_tiles = [possible_tiles[i] 
                            for i in range(len(possible_tiles))
                            if sum_tiles[i] == max(sum_tiles)]
            return random.choice(high_tiles)
        else:
            while stack:
                self.add_tile(stack.pop(0))
                possible_tiles = self.hand.check_possibles(board)
                if possible_tiles:
                    return possible_tiles[0]
            return None