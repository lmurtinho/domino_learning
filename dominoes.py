# -*- coding: utf-8 -*-
"""
Created on Tue May 17 15:49:19 2016

@author: zsj7
"""

from itertools import combinations
from random import shuffle

class Game():
    """
    Game class for dominoes.
    """

    def __init__(self, n_players=4, n_tiles=7, max_number=6, 
                 n_points=100, draw=True, player_names=[]):
        """
        Initializes a Game object.
        """
        player_names.extend(['Anon{}'.format(i)
                            for i in range(n_players - len(player_names))])
        self.players = [Player(name=player_names[i]) 
                        for i in range(n_players)]
        self.n_points = n_points
        self.n_tiles = n_tiles
        self.max_number = max_number
        self.draw = draw
        self.history = []
    
    def __repr__(self):
        strings = ["Dominoes Game.",
                   "Number of players: {}".format(len(self.players)),
                   "Initial number of tiles per player: {}".format(self.n_tiles),
                   "\nScore:"]
        strings.extend(self.str_game_score())
        return '\n'.join(strings)        
    
    def str_game_score(self):
        ans = ['{0}: {1}'.format(player, player.get_score())
                for player in self.players]
        return ans

    def game_score(self):
        return [player.get_score() for player in self.players]
    
    def play_game(self):
        """
        Plays a game.
        Starts score as game_score and, while the maximum score
        is smaller than max_points, keeps looping:
        - plays new round
        - gets result from new round
        - winner from new round takes points from new round
        - round history appended to game history
        - score updated.
        returns dict with winner and game score
        """
        score = self.game_score()
        while max(score) < self.n_points:
            new_round = Round(self.players, self.draw, 
                              self.n_tiles, self.max_number)
            result = new_round.play_round()
            result['winner'].update_score(result['score'])
            self.history.append(result['history'])
            score = self.game_score()
        winner = max(self.score, key=lambda x: self.score[x])
        return {'winner': winner, 'score': score}
    

class Player():
    """
    """
    def __init__(self, points=0, name="Anon"):
        """
        Initializes a player with the given number of points.
        """
        self.score = points
        self.name = name
    
    def __repr__(self):
        """
        """
        return self.name
        
    def update_score(self, points):
        """
        Adds points to player score.
        """
        self.score += points
    
    def get_score(self):
        """
        Returns current player score.
        """
        return self.score
    
    def play_tile(self, tile, board):
        """
        Check if player's hand has tile and if tile can be connected
        to board.
        Gets where to connect tile and passes tile to board.
        """
        if self.hand.has_tile(tile):
            connections = board.connections(tile)
            if all(connections):
                begin = self.pick_position()
            elif any(connections):
                if connections.index(True):
                    begin = False
                else:
                    begin = True
            else:
                raise ValueError(u'Tile cannot be played.')
            board.add_tile(tile, begin)
        else:
            raise ValueError(u'Tile is not in hand.')
    
    def add_tile(self, tile):
        """
        Add tile to player hand.
        """
        self.hand.get_tile(tile)
    
    def retrieve_hand(self):
        """
        Return player hand.
        """
        return self.hand
    
    def get_hand(self, new_hand):
        """
        Initialize player hand.
        """
        self.hand = new_hand

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
        while len(r.players[0].retrieve_hand().retrieve_tiles()) == r.n_tiles:
            r.rotate_players()
        r.rotate_players()
    
    def play_round(self):
        self.create_stack()
        self.giveout()
        self.initialize_board()
        self.position_players()
    
class Hand():
    
    def __init__(self, tiles=[]):
        self.tiles = tiles
    
    def __repr__(self):
        return str(self.tiles)
        
    def add_tile(self, tile):
        """
        Append tile to hand.
        """
        self.tiles.append(tile)
    
    def has_tile(self, tile):
        """
        Check if hand has tile.
        """
        return (tile in self.tiles) or (tile.reverse() in self.tiles)
    
    def remove_tile(self, tile):
        """
        Remove tile from hand.
        """
        self.tiles.remove(tile)
    
    def check_possibles(self, board):
        return [tile for tile in self.tiles
                if any(board.connections(tile))]   
    
    def retrieve_tiles(self):
        return self.tiles

class Board():
    
    def __init__(self, initial_tile):
        self.tiles = [initial_tile]
    
    def get_borders(self):
        """
        Return board borders (where new tiles can go).
        """
        return (self.tiles[0][0], self.tiles[-1][-1])

    def connections(self, tile):
        """
        Return tuple of booleans: wether tile can connect at
        begin or end of board.
        """
        borders = self.get_borders()
        return (tile[0] in borders, tile[1] in borders)
    
    def add_tile(self, tile, begin):
        """
        Add tile to begin or end of board.
        """
        if begin:
            connection = self.tiles[0][0]
            self.adjust_tile(tile, connection, begin)
            self.tiles = tile + self.tiles
        else:
            connection = self.tiles[-1][-1]
            self.adjust_tile(tile, connection, begin)
            self.tiles += tile
    
    def adjust_tile(tile, connection, begin):
        """
        Position tile correctly to connect to desired position
        (begin if begin=True, end if begin=False).
        """
        if begin and tile[1] != connection:
            tile.reverse()
        elif tile[0] != connection:
            tile.reverse()

g = Game()

r = Round(g.players, g.draw, g.n_tiles, g.max_number)
r.play_round()