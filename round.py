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
        while all([player.hand for player in self.players]) and \
                self.board.open:
            next_player = self.players[0]
            next_player.play(self.board, self.stack)
            self.rotate_players()
            self.board.check_open(self.n_tiles + 1)
            print 'board', self.board
            print self.players[0], self.players[0].hand
            print self.players[1], self.players[1].hand
            print 'stack', self.stack
            print
        winner = self.define_winner()
        score = self.define_score(winner)
        return {'winner': winner, 'score': score}
    
    def define_winner(self):
        points_per_player = {player: player.hand.result()
                                for player in self.players}
        winner = [player for player in points_per_player.keys()
                  if points_per_player[player] == min(points_per_player.values())]
        if len(winner) > 1:
            return None
        else:
            return winner[0]
    
    def define_score(self, winner):
        if not winner:
            return 0
        return sum([player.hand.result() 
                    for player in self.players 
                    if player != winner])