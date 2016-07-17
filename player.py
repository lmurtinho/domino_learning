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
    
    def play(self, board, stack):
        """
        Check if player's hand has tile and if tile can be connected
        to board.
        Gets where to connect tile and passes tile to board.
        """
        tile = self.select_tile(board, stack)
        if tile:
            connections = board.connections(tile)
            if all(connections):
                begin = self.pick_position(tile, board)
            elif any(connections):
                begin = True if connections[0] else False
            else:
                raise ValueError(u'Tile cannot be played.')
            board.add_tile(tile, begin)
            self.hand.remove_tile(tile)

    def add_tile(self, tile):
        """
        Add tile to player hand.
        """
        self.hand.add_tile(tile)
    
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