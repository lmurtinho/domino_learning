from random_player import RandomPlayer
from round import Round

class Game():
    """
    Game class for dominos.
    """

    def __init__(self, n_players=2, n_tiles=7, max_number=6,
                 n_points=100, player_names=[], player_types=[]):
        """
        Initialize game.
        n_players (int): Number of players.
        n_tiles (int): Number of tiles in each player's starting hand.
        max_number (int): Largest value in any side of a tile.
        n_points (int): Points to be reached for a game to be over.
        player_names (list of strings): List of strings with player's names.
        player_types (list of Player objects): List of player types that
        will play the game.
        """
        player_names.extend(['Anon{}'.format(i)
                            for i in range(n_players - len(player_names))])
        player_types.extend([RandomPlayer
                            for i in range(n_players - len(player_types))])
        self.players = [player_types[i](name=player_names[i]) 
                        for i in range(n_players)]
        self.n_points = n_points
        self.n_tiles = n_tiles
        self.max_number = max_number
        self.history = []
    
    def __repr__(self):
        strings = ["Dominos Game.",
                   "Number of players: {}".format(len(self.players)),
                   "Initial number of tiles per player: {}".format(self.n_tiles),
                   "\nScore:"]
        strings.extend(self.str_game_score())
        return '\n'.join(strings)        
    
    def str_game_score(self):
        """
        String with the game score (helper function for __repr__)
        """
        ans = ['{0}: {1}'.format(player, player.get_score())
                for player in self.players]
        return ans

    def game_score(self):
        """
        Return the current score per player.
        """
        return {player: player.get_score() for player in self.players}
    
    def play_game(self):
        """
        Play a game.
        - Start score as game_score (usually 0)
        - New rounds while no player reaches max_score        
        - If winner on round, winner's score is updated
        - History of game is updated with each round's result
            (winner and score of round)
        Return game winner and list of rounds results
        """
        score = self.game_score()
        while max(score.values()) < self.n_points:
            new_round = Round(self.players, self.n_tiles, self.max_number)
            winner, score, _ = new_round.play_round()
            try:
                winner.update_score(score)
            except AttributeError:
                pass
            self.history.append({'winner': str(winner), 'score': score})
            score = self.game_score()
            print self.str_game_score()
            print
        winner = [str(player) for player in self.players 
                  if player.get_score() == max(score.values())][0]
        return winner, self.history
    