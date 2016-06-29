from player import Player
from round import Round

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