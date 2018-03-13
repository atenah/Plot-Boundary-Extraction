from lib.csvfile import InputFile
from lib.xmlconfigfile import XMLConfigFile
import sys
from lib.xmlbuilder import XmlKmlBuilder
from math import cos, radians

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

def record_cell(xml, f_main, f_points, coords, coord_pt, id_val):
    pm = xml.create_el_placemark(f_main)
    xml.create_el_name(pm, id_val)
    xml.create_el_description(pm, id_val)
    xml.create_el_styleurl(pm, '#m_ylw-pushpin')
    
    pl = xml.create_el_polygon(pm)
    xml.create_el_tessellate(pl, '1')
    obi = xml.create_el_outer_boundary_is(pl)
    lr = xml.create_el_linear_ring(obi)
    xml.create_el_coordinates(lr, coords)

    # Add placemark
    pm = xml.create_el_placemark(f_points)
    xml.create_el_styleurl(pm, '#m_ylw-pushpin')
    xml.create_el_name(pm, id_val)
    p = xml.create_el_point(pm)
    xml.create_el_coordinates(p, coord_pt)


#formulas from https://en.wikipedia.org/wiki/Geographic_coordinate_system#Expressing_latitude_and_longitude_as_linear_units
def dec_degrees_to_meters((x1, y1), (x2, y2)):
    mean_lat = radians((y1 + y2) * 0.5)
    xdist = abs((x2 - x1) * (111412.84 * cos(mean_lat) - 93.5 * cos(3*mean_lat) + 0.118 * cos(5*mean_lat)))
    ydist = abs((y2 - y1) * (111132.92 - 558.92 * cos(2*mean_lat) + 1.175 * cos(4*mean_lat) - 0.0023 * cos(6*mean_lat)))
    return xdist, ydist


#formulas from https://en.wikipedia.org/wiki/Geographic_coordinate_system#Expressing_latitude_and_longitude_as_linear_units
def meters_to_dec_degrees((dx, dy), mean_lat):
    mean_lat = radians(mean_lat)
    xdist = abs(dx / (111412.84 * cos(mean_lat) - 93.5 * cos(3*mean_lat) + 0.118 * cos(5*mean_lat)))
    ydist = abs(dy / (111132.92 - 558.92 * cos(2*mean_lat) + 1.175*cos(4*mean_lat) - 0.0023 * cos(6*mean_lat)))
    return xdist, ydist
    

def get_coords(x, y, (dx, dy), (xdir, ydir)):
    coord_pt =  format(x + 0.5*dx*xdir, ".12f") + "," + format(y+0.5*dy*ydir, ".12f") + ",0"    
    coord =  format(x, ".12f") + "," + format(y, ".12f") + ",0 "
    coord += format(x+dx*xdir, ".12f") + "," + format(y, ".12f") + ",0 "
    coord += format(x+dx*xdir, ".12f") + "," + format(y+dy*ydir, ".12f") + ",0 "
    coord += format(x, ".12f") + "," + format(y+dy*ydir, ".12f") + ",0 "
    coord += format(x, ".12f") + "," + format(y, ".12f") + ",0 "    
    return coord, coord_pt

def main(conf, inputFile):
    widthInMeters, heightInMeters = dec_degrees_to_meters(conf.first_coord, conf.last_coord)

    
    print "Width:", widthInMeters, "m"
    print "Height:", heightInMeters, "m"

    plots_size = inputFile.ncols * conf.plot_size[0] + (inputFile.ncols - 1 - len(conf.special_cols)) * conf.col_dist + len(conf.special_cols) * conf.special_gap, inputFile.nrows * conf.plot_size[1] + (inputFile.nrows - 1) * conf.row_dist
    print "Size based on plot input file", plots_size

    scaling_factor = widthInMeters/plots_size[0], heightInMeters/plots_size[1]

    conf.scale(scaling_factor)
    
    plots_size = inputFile.ncols * conf.plot_size[0] + (inputFile.ncols - 1 - len(conf.special_cols)) * conf.col_dist + len(conf.special_cols) * conf.special_gap, inputFile.nrows * conf.plot_size[1] + (inputFile.nrows - 1) * conf.row_dist
    print "Scaled size based on plot input file", plots_size

    
    plot_size_degs = meters_to_dec_degrees(conf.plot_size, 0.5*(conf.first_coord[1] + conf.last_coord[1]))
    plot_gap_degs = meters_to_dec_degrees((conf.col_dist, conf.row_dist), 0.5*(conf.first_coord[1] + conf.last_coord[1]))
    special_gap_degs = meters_to_dec_degrees((conf.special_gap, conf.row_dist), 0.5*(conf.first_coord[1] + conf.last_coord[1]))
    

    
    xml = XmlKmlBuilder()
    d = xml.create_el_document()

    # Main `Folder` with name
    f_main = xml.create_el_folder(d)
    xml.create_el_name(f_main, "main")

    # `Folder` with name (OriginPoints)
    f_origin_points = xml.create_el_folder(d)
    xml.create_el_name(f_origin_points,  'main-Puntos de Origen')

    # `Folder` with name (Points)
    f_points = xml.create_el_folder(d)
    xml.create_el_name(f_points, 'main-Puntos')

    add_style_to_folder(f_main, xml)
    addstyle_map_to_folder(f_main, xml)

    # left-top `Placemark`
    pm = xml.create_el_placemark(f_origin_points)
    xml.create_el_name(pm, 'Punto 1')
    pt = xml.create_el_point(pm)
    xml.create_el_coordinates(pt, ",".join(map(str, conf.first_coord)) + ",0")

    # bottom-right `Placemark`
    pm = xml.create_el_placemark(f_origin_points)
    xml.create_el_name(pm, 'Punto 2')
    pt = xml.create_el_point(pm)
    xml.create_el_coordinates(pt, ",".join(map(str, conf.first_coord)) + ",0")


    not_empty_elements = []


    xs = conf.first_coord[0], conf.last_coord[0]
    ys = conf.first_coord[1], conf.last_coord[1]        
    
    x0, y0 = conf.first_coord
    xlim, ylim = conf.last_coord

    x = x0
    y = y0

    col_ind = 0
    row_ind = 0

    cell_id = 0

    if xlim > x0:
        xdir = 1
    else:
        xdir = -1
    if ylim > y0:
        ydir = 1
    else:
        ydir = -1

    print x0, xlim, x0 + plot_gap_degs[0] * xdir

    x_m = 0
    y_m = 0
    
    while (y0 <= y + plot_gap_degs[1] * ydir < ylim) or (y0 >= y + plot_gap_degs[1] * ydir > ylim):
        x = x0
        x_m = 0
        col_ind = 0
        while (x0 <= x + plot_gap_degs[0] * xdir < xlim) or (x0 >= x+ plot_gap_degs[0] * xdir > xlim):
#            print x_m, y_m
 #           print x, xlim
            coords, coord_pt = get_coords(x, y, plot_size_degs, (xdir, ydir))
            record_cell(xml, f_main, f_points, coords, coord_pt, inputFile.get_zi(row_ind, col_ind))
            
            col_ind += 1
            x += plot_size_degs[0] * xdir
            x_m += conf.plot_size[0]
            cell_id += 1
            if (col_ind, col_ind +1) in conf.special_cols:
#                print "SPECIAL COL"
                x += special_gap_degs[0] * xdir
                x_m += conf.special_gap
            else:
                x += plot_gap_degs[0] * xdir
                x_m += conf.col_dist
        row_ind +=1 
        y += plot_gap_degs[1] * ydir + plot_size_degs[1] * ydir
        y_m += conf.plot_size[1] + conf.row_dist

    # ------------------- ------------------- ------------------- ------------------- -------------------

    # output
    xml.save('output.kml')
    print col_ind, "columns"
    print row_ind, "rows"

#   Input variables:
#   --y1
#   --x1
#   --y2
#   --x2
#   -f --input-file
if __name__ == "__main__":

    conf = XMLConfigFile(sys.argv[1])
    inputFile = InputFile(conf.input_filename)
    main(conf, inputFile)
