
### This scrip takes the modified CSV file that has planting information; name of the plots, trials,... please read the "readme" that I created to help you with it.
### Atena Haghighattalab
import argparse
import os
from os.path import basename
import math
from lib.csvfile import Csvfile
from lib.xmlbuilder import XmlKmlBuilder
from lib.timer import Timer

def add_style_to_folder(f_main, xml):
    # add `Style` attribute to Main `Folder`
    s = xml.create_el_style(f_main)

    # add `IconStyle` into `Style` with `scale`
    ics = xml.create_el_icon_style(s)
    xml.create_el_scale(ics, '0.0')

    # add `LabelStyle` into `Style` with `scale`
    lbs = xml.create_el_label_style(s)
    xml.create_el_scale(lbs, '0.5')

    # add `PolyStyle` into `Style` with `fill`
    lbs = xml.create_el_poly_style(s)
    xml.create_el_fill(lbs, '0')


def addstyle_map_to_folder(f_main, xml):

    # create `StyleMap`
    sm = xml.create_el_style_map(f_main)

    # create `Pair` inside `StyleMap` with `key`
    p = xml.create_el_pair(sm)
    xml.create_el_key(p, 'normal')
    xml.create_el_styleurl(p, '#s_ylw-pushpin')


def main(x1, y1, x2, y2, input_file):

    # TODO: make this as a helper function
    name = os.path.splitext(basename(input_file))[0]

    csvfile = Csvfile(input_file)

    x1o = x1
    width = abs(x1 - x2)
    height = abs(y1 - y2)

    print(width)
    print(height)

    xml = XmlKmlBuilder()
    d = xml.create_el_document()

    # Main `Folder` with name
    f_main = xml.create_el_folder(d)
    xml.create_el_name(f_main, name)

    # `Folder` with name (OriginPoints)
    f_origin_points = xml.create_el_folder(d)
    xml.create_el_name(f_origin_points, name + '-Puntos de Origen')

    # `Folder` with name (Points)
    f_points = xml.create_el_folder(d)
    xml.create_el_name(f_points, name + '-Puntos')

    add_style_to_folder(f_main, xml)
    addstyle_map_to_folder(f_main, xml)

    # left-top `Placemark`
    pm = xml.create_el_placemark(f_origin_points)
    xml.create_el_name(pm, 'Punto 1')
    pt = xml.create_el_point(pm)
    xml.create_el_coordinates(pt, str(x1) + "," + str(y1) + ",0")

    # bottom-right `Placemark`
    pm = xml.create_el_placemark(f_origin_points)
    xml.create_el_name(pm, 'Punto 2')
    pt = xml.create_el_point(pm)
    xml.create_el_coordinates(pt, str(x2) + "," + str(y2) + ",0")

    # ------------------- ------------------- ------------------- ------------------- -------------------

    # count sum of rows in first column
    hm = 0.0
    for row in range(0, csvfile.rows_count()):
        if csvfile.is_number(0, row):
            hm += csvfile.get_number(0, row)

    # count sum of cols in first row
    wm = 0.0
    for col in range(0, csvfile.cols_count()):
        if csvfile.is_number(col, 0):
            wm += csvfile.get_number(col, 0)

    not_empty_elements = []

    for row in range(1, csvfile.rows_count()):
        with Timer() as t:
            for col in range(1, csvfile.cols_count()):

                id_val = str(csvfile.get(col, row))

                # `porcentajex` is how many GEO points in current column number
                if csvfile.is_number(col, 0) and wm != 0:
                    porcentajex = csvfile.get_number(col, 0) / wm
                else:
                    porcentajex = 0

                if csvfile.is_number(0, row) and hm != 0:
                    porcentajey = csvfile.get_number(0, row) / hm
                else:
                    porcentajey = 0

                # 1st point (left-top)
                x = x1
                y = y1
                coord = format(x, '.12f') + "," + format(y, '.12f') + ",0 "
                coord_point = ""

                # 2nd point (right-top)
                x = x1 + (width * porcentajex)
                coord_point += format(x1 + (width * porcentajex / 2), '.12f') + ","
                coord += format(x, '.12f') + "," + format(y, '.12f') + ",0 "

                yempty = 0
                for in_row in range(row, csvfile.rows_count()):
                    if csvfile.get(in_row, col) == "-":
                        not_empty_elements.append(str(in_row) + '-' + str(col))
                        yempty += csvfile.get(in_row, 0) / hm
                    else:
                        break

                coord_point += format(y1 - (height * (porcentajey + yempty) / 2), '.12f') + ",0"

                # 3rd (right-bottom)
                y = y1 - (height * (porcentajey + yempty))
                coord += format(x, '.12f') + "," + format(y, '.12f') + ",0 "

                # 4rd (left-bottom)
                x = x1
                coord += format(x, '.12f') + "," + format(y, '.12f') + ",0 "

                # 1st point again
                y = y1
                coord += format(x, '.12f') + "," + format(y, '.12f') + ",0"

                x1 = x1 + (width * porcentajex)

                if (str(row) + '-' + str(col)) not in not_empty_elements and id_val != "" and id_val != "-":

                    # add placemark
                    pm = xml.create_el_placemark(f_main)
                    xml.create_el_name(pm, id_val)
                    xml.create_el_description(pm, id_val)
                    xml.create_el_styleurl(pm, '#m_ylw-pushpin')

                    pl = xml.create_el_polygon(pm)
                    xml.create_el_tessellate(pl, '1')
                    obi = xml.create_el_outer_boundary_is(pl)
                    lr = xml.create_el_linear_ring(obi)
                    xml.create_el_coordinates(lr, coord)

                    # Add placemark
                    pm = xml.create_el_placemark(f_points)
                    xml.create_el_styleurl(pm, '#m_ylw-pushpin')
                    xml.create_el_name(pm, id_val)
                    p = xml.create_el_point(pm)
                    xml.create_el_coordinates(p, coord_point)

                # if cell is empty, but next one has something -> this is horizontal gap
                # if "" == csvfile.get(col, row) and "" != csvfile.get(col+1, row):
                #
                #     x1 += csvfile.get_number(col, 0) * porcentajex
                #
                #     print(porcentajex)
                #     print(width * porcentajex)
                #     print(csvfile.get_number(col, 0) * porcentajex)
                #     print(col)
                #     print(row)
                #     exit()

        print "=> elasped lpush: %s s" % t.secs

        print(str(math.floor(float(row) / float(csvfile.rows_count()) * 100)) + "% completed")

        x1 = x1o
        y1 = y1 - (height * porcentajey)

    # ------------------- ------------------- ------------------- ------------------- -------------------

    # output
    xml.save('output.kml')


#   Input variables:
#   --y1
#   --x1
#   --y2
#   --x2
#   -f --input-file
if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-y1', type=float, required=True, help="")
    parser.add_argument('-x1', type=float, required=True, help="")
    parser.add_argument('-y2', type=float, required=True, help="")
    parser.add_argument('-x2', type=float, required=True, help="")
    parser.add_argument('-f', '--input-file', type=str, required=True, help="")

    args = parser.parse_args()

    main(args.x1, args.y1, args.x2, args.y2, args.input_file)