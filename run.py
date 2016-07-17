from game import Game
from round import Round

g = Game()

r = Round(g.players, g.draw, g.n_tiles, g.max_number)
print r.play_round()
p1, p2 = r.players