from osgeo import ogr
from osgeo import osr
import datetime


def create_shp(coord_file_name, layer_name):
    driver = ogr.GetDriverByName("ESRI Shapefile")
    data_source = driver.CreateDataSource(
        "data/output/{}_{}.shp".format(layer_name, datetime.datetime.now().strftime('%Y%m%d%H%M%S')))

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)

    layer = data_source.CreateLayer(layer_name, srs, ogr.wkbPoint)

    field_name = ogr.FieldDefn("name", ogr.OFTString)
    field_name.SetWidth(24)
    layer.CreateField(field_name)

    field_name = ogr.FieldDefn("x", ogr.OFTReal)
    # field_name.SetWidth(12)
    # field_name.SetPrecision(8)
    layer.CreateField(field_name)

    field_name = ogr.FieldDefn("y", ogr.OFTReal)
    # field_name.SetWidth(12)
    # field_name.SetPrecision(8)
    layer.CreateField(field_name)

    with open(coord_file_name, "r") as file:
        for line in file.readlines():
            items = line.split(",")
            if len(items) > 2:
                print("Point Num {}".format(items[0]))
                feature = ogr.Feature(layer.GetLayerDefn())
                feature.SetField("name", items[0])
                feature.SetField("x", items[1])
                feature.SetField("y", items[2])
                wkt = 'POINT({} {})'.format(items[1], items[2])
                point = ogr.CreateGeometryFromWkt(wkt)
                feature.SetGeometry(point)
                layer.CreateFeature(feature)
                feature = None
    data_source = None


if __name__ == '__main__':
    create_shp("data/coords.txt", "lane_point_84")
