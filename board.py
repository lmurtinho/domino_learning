from collections import Counter

class Board():
    """
    Board class for dominos.
    """
    
    def __init__(self, tiles):
        self.tiles = tiles
        self.open = True
    
    def __repr__(self):
        return str(self.tiles)

    def get_borders(self):
        """
        Return board borders (where new tiles can go).
        """
        return (self.tiles[0][0], self.tiles[-1][-1])
    
    def connections(self, tile):
        """
        Return tuple of booleans: whether tile can connect at
        begin or end of board.
        """
        borders = self.get_borders()
        border_start = tile[0] == borders[0] or tile[1] == borders[0]
        border_end = tile[0] == borders[1] or tile[1] == borders[1]
        return (border_start, border_end)
    
    def add_tile(self, tile, begin):
        """
        Add tile to begin or end of board.
        """
        if begin:
            connection = self.tiles[0][0]
            self.adjust_tile(tile, connection, begin)
            self.tiles = [tile] + self.tiles
        else:
            connection = self.tiles[-1][-1]
            self.adjust_tile(tile, connection, begin)
            self.tiles += [tile]
    
    def adjust_tile(self, tile, connection, begin):
        """
        Position tile correctly to connect to desired position
        (begin if begin=True, end if begin=False).
        """
        if begin:
            if tile[1] != connection:
                tile.reverse()
        elif tile[0] != connection:
            tile.reverse()
    
    def check_open(self, n_faces):
        """
        Check if any tile not yet on board can be
        added to it.
        """
        count_used = Counter([item for sublist in self.tiles
                                for item in sublist
                                if item in self.get_borders()])
        if min(count_used.values()) == n_faces:
            self.open = False