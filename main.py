from osgeo import ogr
from osgeo import osr


def create_shp(coord_file_name):
    driver = ogr.GetDriverByName("ESRI Shapefile")
    data_source = driver.CreateDataSource("lane_point_84.shp")

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)

    layer = data_source.CreateLayer("lane_point_84", srs, ogr.wkbPoint)

    field_name = ogr.FieldDefn("PointNum", ogr.OFTString)
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
                feature.SetField("PointNum", items[0])
                feature.SetField("x", items[1])
                feature.SetField("y", items[2])
                wkt = 'POINT({} {})'.format(items[1], items[2])
                point = ogr.CreateGeometryFromWkt(wkt)
                feature.SetGeometry(point)
                layer.CreateFeature(feature)
                feature = None
    data_source = None


if __name__ == '__main__':
    create_shp("coords.txt")
