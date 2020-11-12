from pyproj import CRS
from pyproj import Transformer

crs_4326 = CRS.from_epsg(4326)
crs_4547 = CRS.from_epsg(4547)
transformer = Transformer.from_crs(crs_4547, crs_4326)

with open("input.txt", "r") as input_file, open("output.txt", "w") as output_file:
    for line in input_file.readlines():
        items = line.split(",")
        if len(items) > 2:
            out_coords = transformer.transform(items[2], items[1])
            output_file.write("{},{},{},\n".format(items[0], out_coords[1], out_coords[0]))
