import os
import json
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    jsonify
)
from project import app
from project.lib.shp2geojson import Shapefile2GeoJSON

data = Blueprint('data', __name__)
SHAPEFILES_PATH = app.root_path + '\\static\shapefiles\\'
GEOJSON_PATH = app.root_path + '\\static\geojson\\'

@data.route('/data_peta/')
def index():
    shapefiles = [f for f in os.listdir(SHAPEFILES_PATH) if f.endswith(".shp")]
    geojson = [f.split(".json")[0] for f in os.listdir(GEOJSON_PATH) if os.path.isfile(os.path.join(GEOJSON_PATH, f))]
    shapefiles.sort(reverse=True)
    geojson.sort(reverse=True)

    data = []
    for shp in shapefiles:
        temp = {}
        temp['shp'] = shp

        if shp.split(".shp")[0] in geojson:
            temp['geojson'] = shp.split(".shp")[0] + ".json"
        else:
            temp['geojson'] = ""
        
        data.append(temp)

    return render_template('data.html', result=data)

@data.route('/data_peta/konversi_shp_geojson/<string:shapefile>/')
def convert_shp2geojson(shapefile):
    shp = SHAPEFILES_PATH + shapefile
    result = Shapefile2GeoJSON(shp)

    return redirect(url_for('data.index'))

@data.route('/data_peta/<string:geojson>/')
def show_geojson(geojson):
    with open(GEOJSON_PATH + geojson) as output:
        data = json.load(output)
        output.close()
    
    return jsonify(data)