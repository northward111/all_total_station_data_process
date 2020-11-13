from osgeo import ogr
from pyproj import CRS
from pyproj import Transformer

crs_4326 = CRS.from_epsg(4326)
crs_4547 = CRS.from_epsg(4547)
transformer = Transformer.from_crs(crs_4326, crs_4547)


def geojson2txt(geojson_file_name, txt_file_name):
    json_driver = ogr.GetDriverByName('GeoJSON')
    json_ds = json_driver.Open(geojson_file_name)
    cs = json_ds.GetLayerByIndex(0)
    with open(txt_file_name, "w") as txt_file:
        for row in cs:
            name = row.GetField(row.GetFieldIndex("Name"))
            point_num = int(name.replace('ref_', ''))
            geometry = row.geometry()
            out_coords = transformer.transform(geometry.GetY(), geometry.GetX())
            txt_file.write("{},{},{},\n".format(point_num, out_coords[1], out_coords[0]))


if __name__ == "__main__":
    geojson2txt("data/ref_points.geojson", "data/reference.txt")
