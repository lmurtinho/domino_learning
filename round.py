from itertools import combinations
from random import shuffle
from hand import Hand
from board import Board

class Round():

    def __init__(self, players, draw, n_tiles, max_number):
        """
        Initializes new round.
        """
        self.players = players
        self.draw = draw
        self.n_tiles = n_tiles
        self.max_number = max_number
        self.history = []
            
    def create_stack(self):
        """
        Creates a new shuffled stack.
        """
        faces = range(self.max_number + 1)
        self.stack = [list(item) for item in combinations(faces, 2)] + \
                     [[i, i] for i in range(self.max_number + 1)]
        if (len(self.stack) / len(self.players)) < self.n_tiles:
            raise ValueError(u'Not enough tiles for all players!')
        else:
            shuffle(self.stack)

    def giveout(self):
        """
        Distributes tiles to players.
        """
        for player in self.players:
            new_hand = self.stack[:self.n_tiles]
            self.stack = self.stack[self.n_tiles:]
            player.get_hand(Hand(new_hand))
    
    def find_initial_tile(self):
        """
        """
        tiles = [item for sublist in 
                    [player.retrieve_hand().retrieve_tiles() 
                     for player in self.players]
                 for item in sublist]
        try:
            max_double = max([tile[0] for tile in tiles if tile[0]==tile[1]])
            max_tile = [max_double, max_double]
        except ValueError:
            max_tiles = [tile for tile in tiles 
                         if sum(tile) == max([sum(tile_) for tile_ in tiles])]
            largest_value = max(value for tile in max_tiles for value in tile)
            max_tile = [tile for tile in max_tiles if largest_value in tile][0]
        return max_tile

    def rotate_players(self):
        """
        Changes player position in player list.
        """
        self.players.append(self.players.pop(0))
    
    def initialize_board(self):
        """
        Find initial tile and use it to initialize board.
        """
        initial_tile = self.find_initial_tile()        
        for player in self.players:
            try:
                player.hand.remove_tile(initial_tile)
                self.history.append((player, initial_tile))
                break
            except ValueError:
                continue
        self.board = Board(initial_tile)
    
    def position_players(self):
        """
        Position as first player to play the player after the one
        who played the first tile.
        """
        while len(self.players[0].retrieve_hand().retrieve_tiles()) \
        == self.n_tiles:
            self.rotate_players()
        self.rotate_players()
    
    def play_round(self):
        self.create_stack()
        self.giveout()
        self.initialize_board()
        self.position_players()