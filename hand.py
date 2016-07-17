class Hand():
    
    def __init__(self, tiles=[]):
        self.tiles = tiles
    
    def __repr__(self):
        return str(self.tiles)
    
    def __len__(self):
        return len(self.tiles)
    
    def result(self):
        return sum([item for sublist in self.tiles for item in sublist])
    
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