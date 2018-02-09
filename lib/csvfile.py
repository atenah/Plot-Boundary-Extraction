import csv

class InputFile:
    def __init__(self, filename):
        self.index = {}
        self.rownums = set()
        self.colnums = set()
        with open(filename, 'rU') as csvfile:
            streamreader=csv.reader(csvfile, delimiter=',', lineterminator="\n")
            streamreader.next() # skip first line (title row)
            
            for row in streamreader:
                self.rownums.add(int(row[0]))
                self.colnums.add(int(row[1]))
                self.index[(int(row[0]), int(row[1]))] = row[2]
        self.max_row = max(self.rownums)
        self.min_row = min(self.rownums)
        self.max_col = max(self.colnums)
        self.min_col = min(self.colnums)

        self.nrows = len(self.rownums)
        self.ncols = len(self.colnums)
        
    def get_zi(self, row, col):
        if (row + self.min_row, col + self.min_col) in self.index:
            return str(row + self.min_row) + "/" + str(col + self.min_col) + "/" + self.index[(row + self.min_row, col + self.min_col)]
        else:
            return "NONE"
