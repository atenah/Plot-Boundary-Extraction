import csv
import math

def meters_val(x):
    return float(x.split(" ")[0])

def col_pairs(x):
    return tuple([int(i) for i in x.replace('"', "").split(",")])
        
class ConfigFile:
    def __init__(self, filename):
        with open(filename, 'rU') as csvfile:
            streamreader = csv.reader(csvfile, delimiter=',', lineterminator="\n", quotechar="\"")
            for row in streamreader:
                if "plot_size" in row:
                    ind = row.index("plot_size")
                    self.plot_size = (meters_val(row[ind+2]), meters_val(row[ind+1]))
                if "distance between columns" in row:
                    ind = row.index("distance between columns")
                    self.col_dist = meters_val(row[ind+1])
                if "distance between rows" in row:
                    ind = row.index("distance between rows")
                    self.row_dist = meters_val(row[ind+1])
                if "gap between some specified columns" in row:
                    ind = row.index("gap between some specified columns")
                    self.special_gap = meters_val(row[ind+1])
                if "column numbers with gap" in row:
                    ind = row.index("column numbers with gap")
                    self.special_cols = []
                    for i in range(ind+1, len(row)):
                        if len(row[i]):
                            self.special_cols.append(col_pairs(row[i]))

                if "coordinate of first plot" in row:
                    ind = row.index("coordinate of first plot")
                    self.first_coord = tuple(map(float, row[ind+1].split()[0:2]))
                if "coordinate of last plot" in row:
                    ind = row.index("coordinate of last plot")
                    self.last_coord = tuple(map(float, row[ind+1].split()[0:2]))
                if "plot labels" in row:
                    ind = row.index("plot labels")
                    self.inputFileName = row[ind+1]

        print "Plot size:", self.plot_size
        print "Distance between columns:", self.col_dist
        print "Distance between rows:", self.row_dist
        print "Special columns:", self.special_cols
        print "Special gap:", self.special_gap
        print "Coordinate of first plot:", self.first_coord
        print "Coordinate of last plot:", self.last_coord        

    def scale(self, (fx, fy)):
        self.plot_size = fx * self.plot_size[0], fy * self.plot_size[1]
        self.col_dist *= fx
        self.row_dist *= fy
        self.special_gap *= fx
