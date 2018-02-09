import lib.configfile
import xml.etree.ElementTree

class XMLConfigFile(lib.configfile.ConfigFile):
    def tupleize_floats(self, first, second):
        return (float(first), float(second))


    def tupleize_column(self, columnElement):
        n = int(columnElement.text)
        return (n - 1, n)

        
    def find_plots(self, plotsElement):
        sizeElement    = plotsElement.find("size")
        self.plot_size = self.tupleize_floats(
            sizeElement.findtext("horizontalMeters"),
            sizeElement.findtext("verticalMeters"  ))

        requiredGapsElement = plotsElement.find("requiredGaps")
        self.col_dist = float(requiredGapsElement.findtext("horizontalMeters"))
        self.row_dist = float(requiredGapsElement.findtext("verticalMeters"  ))


    def find_sections(self, sectionsElement):
        self.special_gap  = 0.0
        self.special_cols = []

        if sectionsElement != None:
            optionalGapsElement = sectionsElement.find("optionalGaps")
            horizontalMetersText = optionalGapsElement.findtext(
                "horizontalMeters")
            if horizontalMetersText != None:
                self.special_gap = float(horizontalMetersText)

            startsElement = sectionsElement.find("starts")
            horizontalElement = startsElement.find("horizontal")
            if horizontalElement != None:
                for columnElement in horizontalElement.findall("./column"):
                    self.special_cols.append(
                        self.tupleize_column(columnElement))


    def find_coordinates(self, coordinatesElement):
        firstElement     = coordinatesElement.find("first")
        self.first_coord = self.tupleize_floats(
            firstElement.findtext("longitudeDecimalDegrees"),
            firstElement.findtext("latitudeDecimalDegrees" ))

        lastElement     = coordinatesElement.find("last")
        self.last_coord = self.tupleize_floats(
            lastElement.findtext("longitudeDecimalDegrees"),
            lastElement.findtext("latitudeDecimalDegrees" ))


    def __init__(self, filename):
        elementTree = xml.etree.ElementTree.parse(filename)

        self.find_plots      (elementTree.find("plots"      ))
        self.find_sections   (elementTree.find("sections"   ))
        self.find_coordinates(elementTree.find("coordinates"))

        self.input_filename = elementTree.findtext("inputFileName")
        
        self.print_values()
