from collections import Counter
from game import Game
from high_tile_player import HighTilePlayer
from human_player import HumanPlayer
from random_player import RandomPlayer
import pandas as pd
from round import Round

def run_sim(max_points):
    return Game(player_names = ["Random", "HighTile"],
                player_types = [RandomPlayer, HighTilePlayer],
                n_points = max_points).play_game()

def run_sims(n_sims, max_points):
    winners = []
    histories = []
    for i in range(n_sims):
        winner, history = run_sim(max_points)
        winners.append(winner)
        histories.append(history)
    return winners, histories

# winners, histories = run_sims(1000, 1000)
# print Counter(winners)

g = Game(player_names = ['Lucas', 'HighTile'],
         player_types = [HumanPlayer, HighTilePlayer],
         n_points = 100)
g.play_game()
# g = run_sims(100, 100)
#result = Round([HighTilePlayer(name='HT'), RandomPlayer(name='RP')], 
#                True, 7, 6).play_round()

#print winner
#df = pd.DataFrame.from_dict(history)
#print r.play_round()
#p1, p2 = r.players