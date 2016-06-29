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