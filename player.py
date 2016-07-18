class Player():
    """
    Basic class of domino player.
    """
    
    def __init__(self, points=0, name="Anon"):
        """
        Initialize a player with the given number of points and name.
        """
        self.score = points
        self.name = name

    def __repr__(self):
        return self.name
        
    def get_round(self, round_):
        """
        Initialize the round the player is playing.
        """
        self.round = round_
    
    def update_score(self, points):
        """
        Add points to player score.
        """
        self.score += points
    
    def get_score(self):
        """
        Return current player score.
        """
        return self.score
    
    def play(self):
        """
        - Use select_tile method (defined Player subclasses)
            to select a tile to play.
        - If tile can be played at both ends, use pick_position method
            (defined in Player subclasses) to pick where to play it 
        - If tile can be played at only one end of board, automatically pick
            where to play tile
        - Raise a ValueError if tile cannot be played
        - If tile is playable, add it to board at predefined position
            and remove it from player's hand
        """
        board = self.round.board
        tile = self.select_tile()
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