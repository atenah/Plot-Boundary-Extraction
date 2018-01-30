
from xml.dom import minidom

class XmlKmlBuilder:

    def __init__(self):
        self.doc = minidom.Document()
        self.kml = self.doc.createElement('kml')
        self.kml.setAttribute('xmlns', 'http://www.opengis.net/kml/2.2')
        self.doc.appendChild(self.kml)

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(self.doc.toprettyxml(indent="  "))
            f.close()

    def create_el_document(self):
        return self._create_empty_el(self.kml, 'Document')

    def create_el_folder(self, parent_el):
        return self._create_empty_el(parent_el, 'Folder')

    def create_el_name(self, parent_el, name):
        return self._create_text_el(parent_el, 'name', name)

    def create_el_description(self, parent_el, description):
        return self._create_text_el(parent_el, 'description', description)

    def create_el_style(self, parent_el):
        el = self._create_empty_el(parent_el, 'Style')
        el.setAttribute('id', 's_ylw-pushpin')
        return el

    def create_el_style_map(self, parent_el):
        el = self._create_empty_el(parent_el, 'StyleMap')
        el.setAttribute('id', 'm_ylw-pushpin')
        return el

    def create_el_icon_style(self, parent_el):
        return self._create_empty_el(parent_el, 'IconStyle')

    def create_el_label_style(self, parent_el):
        return self._create_empty_el(parent_el, 'LabelStyle')

    def create_el_poly_style(self, parent_el):
        return self._create_empty_el(parent_el, 'PolyStyle')

    def create_el_pair(self, parent_el):
        return self._create_empty_el(parent_el, 'Pair')

    def create_el_placemark(self, parent_el):
        return self._create_empty_el(parent_el, 'Placemark')

    def create_el_point(self, parent_el):
        return self._create_empty_el(parent_el, 'Point')

    def create_el_polygon(self, parent_el):
        return self._create_empty_el(parent_el, 'Polygon')

    def create_el_outer_boundary_is(self, parent_el):
        return self._create_empty_el(parent_el, 'outerBoundaryIs')

    def create_el_linear_ring(self, parent_el):
        return self._create_empty_el(parent_el, 'LinearRing')

    def create_el_scale(self, parent_el, scale):
        return self._create_text_el(parent_el, 'scale', scale)

    def create_el_fill(self, parent_el, fill):
        return self._create_text_el(parent_el, 'fill', fill)

    def create_el_key(self, parent_el, key):
        return self._create_text_el(parent_el, 'key', key)

    def create_el_tessellate(self, parent_el, tessellate):
        return self._create_text_el(parent_el, 'tessellate', tessellate)

    def create_el_styleurl(self, parent_el, styleurl):
        return self._create_text_el(parent_el, 'styleUrl', styleurl)

    def create_el_coordinates(self, parent_el, coordinates):
        return self._create_text_el(parent_el, 'coordinates', coordinates)

    def _create_empty_el(self, parent_el, tag):
        el = self.doc.createElement(tag)
        parent_el.appendChild(el)
        return el

    def _create_text_el(self, parent_el, tag, text):
        el = self._create_empty_el(parent_el, tag)
        txt = self.doc.createTextNode(text)
        el.appendChild(txt)
        return el



