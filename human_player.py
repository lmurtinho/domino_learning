from player import Player
import random

class HumanPlayer(Player):
    """
    A domino player that selects tiles and tile position
    according to inputs from a human.
    """
    
    def select_tile(self):
        """
        Selec tile to play next.
        """
        board = self.round.board
        stack = self.round.stack
        print "\nBoard: {}".format(board)
        for player in self.round.players:
            if player != self:
                print "Player {} has {} tiles.".format(str(player),
                                                       len(player.hand))
        print "There are {} tiles on the stack.".format(len(self.round.stack))
        print "Hand: {}".format(self.hand)
        possible_tiles = self.hand.check_possibles(board)
        if possible_tiles:
            return self.pick_tile(possible_tiles)
        else:
            while stack:
                print "No tiles to play! Buying from stack."
                self.add_tile(stack.pop(0))
                possible_tiles = self.hand.check_possibles(board)
                if possible_tiles:
                    return self.pick_tile(possible_tiles)
            print "No tiles to play! You must pass your turn."
            return None

    def pick_tile(self, possible_tiles):
        if len(possible_tiles) == 1:
            print "Only one tile to play: {}".format(possible_tiles[0])
            return possible_tiles[0]
        else:
            print "Pick the number of your tile from 1 to {}:".\
                format(len(possible_tiles))
            for i in range(len(possible_tiles)):
                print "{}: {}".format(i + 1, possible_tiles[i])
            idx_picked = raw_input()
            while idx_picked not in [str(i) for i in 
                                     range(1, len(possible_tiles) + 1)]:
                print "Invalid choice! Pick a number from 1 to {}".\
                    format(len(possible_tiles))
                idx_picked = raw_input()
            return possible_tiles[int(idx_picked) - 1]

    def pick_position(self, tile, board):
        borders = board.get_borders()
        if borders[0] == borders[1]:
            return random.choice([True, False])
        print 
        pos = raw_input("Type l to add tile to the left, r to the right.\n")
        while pos not in ('l', 'r', 'left', 'right'):
            print "Invalid choice!"
            pos = raw_input("Type l to add tile to the left, r to the right.\n")
        return pos[0] == 'l'