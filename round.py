from itertools import combinations
from random import shuffle
from hand import Hand
from board import Board

class Round():
    """
    Class for a round of dominos.
    """

    def __init__(self, players, n_tiles, max_number):
        """
        Initialize new round.
        - players (Player objects): players that will play the round
        - n_tiles (int): number of tiles in each player's starting hand
        - max_number (int): the highest number in any side of any tile
        """
        self.players = players
        self.n_tiles = n_tiles
        self.max_number = max_number
        self.history = []
            
    def create_stack(self):
        """
        Create a new shuffled stack of tiles.
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
        Distribute tiles to players.
        """
        for player in self.players:
            new_hand = self.stack[:self.n_tiles]
            self.stack = self.stack[self.n_tiles:]
            player.get_hand(Hand(new_hand))
    
    def find_initial_tile(self):
        """
        Find tile that will be placed first in the board
        (the highest double tile in a player's hand, or the first tile
        with the largest value).
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
        Change player position in player list.
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
                break
            except ValueError:
                continue
        self.board = Board([initial_tile])
    
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
        """
        Play a round.
        - Pass the round for each Player object in player list
        - Create shuffled stack and distribute tiles to players
        - Initialize the board and correctly position the players in the
            players list
        - Create first item in round history
        - While all players have tiles in their hands and either the board
            is open or the stack is not empty:
                - Update round history
                - Pick next player and get it to play
                - Rotate players to get the next one to play
                - Check if board remains open
        - Return the winner of the round and the round score
        """
        for player in self.players:
            player.get_round(self)        
        self.create_stack()
        self.giveout()
        self.initialize_board()
        self.position_players()
        self.history.append(self.get_history())
        
        while all([player.hand for player in self.players]) and\
                (self.board.open or self.stack):
            next_player = self.players[0]
            next_player.play()
            self.rotate_players()
            self.board.check_open(self.n_tiles + 1)
            self.history.append(self.get_history())
            
        winner = self.define_winner()
        score = self.define_score(winner)
        print "{} has won {} points!".format(winner, score)
        print        
        return winner, score, self.history
    
    def define_winner(self):
        """
        Return the winner of a round:
            - The player with and empty hand
            - If all players have tiles, the player with 
                the smallest hand value
            - If two players are tied in hand value, no one wins
        """
        points_per_player = {player: player.hand.result()
                                for player in self.players}
        winner = [player for player in points_per_player.keys()
                  if points_per_player[player] == min(points_per_player.values())]
        if len(winner) > 1:
            return None
        else:
            return winner[0]
    
    def define_score(self, winner):
        """
        Return the score of a round:
            - 0 if no winner
            - The sum of the tiles in the hands of non-winners if there
                is a winner
        """
        if not winner:
            return 0
        return sum([player.hand.result() 
                    for player in self.players 
                    if player != winner])
                        
    def get_history(self):
        """
        Return the current history of the round:
            - Tiles on board
            - Number of tiles in each player's hands
            - Number of tiles in stack
        """
        board = list(self.board.tiles)
        n_hands = {str(player): len(player.hand) for player in self.players}
        n_stack = len(self.stack)
        return board, n_hands, n_stack