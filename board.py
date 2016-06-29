class Board():
    
    def __init__(self, initial_tile):
        self.tiles = [initial_tile]
    
    def get_borders(self):
        """
        Return board borders (where new tiles can go).
        """
        return (self.tiles[0][0], self.tiles[-1][-1])

    def connections(self, tile):
        """
        Return tuple of booleans: wether tile can connect at
        begin or end of board.
        """
        borders = self.get_borders()
        return (tile[0] in borders, tile[1] in borders)
    
    def add_tile(self, tile, begin):
        """
        Add tile to begin or end of board.
        """
        if begin:
            connection = self.tiles[0][0]
            self.adjust_tile(tile, connection, begin)
            self.tiles = tile + self.tiles
        else:
            connection = self.tiles[-1][-1]
            self.adjust_tile(tile, connection, begin)
            self.tiles += tile
    
    def adjust_tile(tile, connection, begin):
        """
        Position tile correctly to connect to desired position
        (begin if begin=True, end if begin=False).
        """
        if begin and tile[1] != connection:
            tile.reverse()
        elif tile[0] != connection:
            tile.reverse()