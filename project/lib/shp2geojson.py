import json
import shapefile

def Shapefile2GeoJSON(SHP_PATH):
    shp = shapefile.Reader(SHP_PATH)
    fields = shp.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []

    for sr in shp.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr)) 

    data = SHP_PATH.split('shapefiles/')
    DEST_GEO_PATH = data[0] + 'geojson/' + data[1].split('.shp')[0] + '.json'

    geojson = open(DEST_GEO_PATH, "w")
    geojson.write(json.dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
    geojson.close()

    return DEST_GEO_PATH