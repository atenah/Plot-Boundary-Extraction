class ConfigFile:
    def print_values(self):
        print "Plot size:"               , self.plot_size
        print "Distance between columns:", self.col_dist
        print "Distance between rows:"   , self.row_dist
        print "Special columns:"         , self.special_cols
        print "Special gap:"             , self.special_gap
        print "Coordinate of first plot:", self.first_coord
        print "Coordinate of last plot:" , self.last_coord

    def scale(self, (fx, fy)):
        self.plot_size    = fx * self.plot_size[0], fy * self.plot_size[1]
        self.col_dist    *= fx
        self.row_dist    *= fy
        self.special_gap *= fx
