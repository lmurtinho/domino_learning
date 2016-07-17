from player import Player
import random

class RandomPlayer(Player):
    
    def select_tile(self, board, stack):
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
        random.choice([True, False])