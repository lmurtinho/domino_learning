from player import Player

class LearningPlayer(Player):
    
    def __init__ (self, points=0, name='Anon'):
        super(LearningPlayer, self).__init__(points, name)
        self.qvals = {}
    
    def select_tile(self):
        raw_state = self.get_raw_state()
        board = round_.board
        hand = self.hand
        on_board = Counter([item 
                            for sublist in board.tiles 
                            for item in sublist])
        n_opp = [len(player.hand) for player in round_.players
                    if player != self][0]
        n_stack = len(round_.stack)
    
    def get_raw_state(self, round_):

        board_tiles = round_.board.tiles
        borders = round_.board.get_borders()
        n_tiles = round_.n_tiles
        player_hand = self.hand.tiles
        
        on_board = self.count_from_list(board_tiles)
        held = self.count_from_list(player_hand)
        
        is_border = {i: 1 if i in borders else 0
                        for i in range(n_tiles + 1)}
        n_opp = [len(player.hand) for player in round_.players
                    if player != self][0]
        n_stack = len(round_.stack)
    def count_from_list(self, lst):
        return Counter(item for sublist in lst for item in sublist)
    
    def check_border(self, borders, n_tiles):
        return {i: 1 if i in borders else 0 for i in range(n_tiles)}