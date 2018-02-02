import csv

class ConfigFile:
    def trim_convert(self, x):
        return float(x.split(" ")[0])

    def tupleize_gap(self, x):
        return tuple([int(i) for i in x.replace('"', "").split(",")])

    def tupleize_coordinate(self, x):
        return tuple(map(float, x.split()[0:2]))

    def print_values(self):
        print "Plot size:"               , self.plot_size
        print "Distance between columns:", self.col_dist
        print "Distance between rows:"   , self.row_dist
        print "Special columns:"         , self.special_cols
        print "Special gap:"             , self.special_gap
        print "Coordinate of first plot:", self.first_coord
        print "Coordinate of last plot:" , self.last_coord

    def __init__(self, filename):
        with open(filename, 'rU') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', lineterminator="\n", quotechar="\"")
            for line in reader:
                if "plot_size" in line:
                    index          = line.index("plot_size")
                    self.plot_size = (self.trim_convert(line[index+2]), self.trim_convert(line[index+1]))

                if "distance between columns" in line:
                    index         = line.index("distance between columns")
                    self.col_dist = self.trim_convert(line[index+1])
                if "distance between rows" in line:
                    index         = line.index("distance between rows")
                    self.row_dist = self.trim_convert(line[index+1])

                if "gap between some specified columns" in line:
                    index            = line.index("gap between some specified columns")
                    self.special_gap = self.trim_convert(line[index+1])
                if "column numbers with gap" in line:
                    index             = line.index("column numbers with gap")
                    self.special_cols = []
                    for i in range(index+1, len(line)):
                        if len(line[i]) > 0:
                            self.special_cols.append(self.tupleize_gap(line[i]))

                if "coordinate of first plot" in line:
                    index            = line.index("coordinate of first plot")
                    self.first_coord = self.tupleize_coordinate(line[index+1])
                if "coordinate of last plot" in line:
                    index           = line.index("coordinate of last plot")
                    self.last_coord = self.tupleize_coordinate(line[index+1])

                if "plot labels" in line:
                    index              = line.index("plot labels")
                    self.input_filename = line[index+1]
        self.print_values()

    def scale(self, (fx, fy)):
        self.plot_size    = fx * self.plot_size[0], fy * self.plot_size[1]
        self.col_dist    *= fx
        self.row_dist    *= fy
        self.special_gap *= fx
