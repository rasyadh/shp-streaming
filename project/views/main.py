import os
import json
from flask import (
    Blueprint,
    render_template,
    url_for,
    jsonify
)
from project import app

main = Blueprint('main', __name__)
GEOJSON_PATH = app.root_path + '/static/geojson/'

@main.route('/')
@main.route('/index')
@main.route('/peta/')
def index():
    default_geojson, geojson = [], []
    
    for f in os.listdir(GEOJSON_PATH):
        if os.path.isfile(os.path.join(GEOJSON_PATH, f)):
            if f == 'Surabaya.json' or f == 'KecamatanSurabaya.json':
                default_geojson.append(f)
            else:
                geojson.append(f)
    geojson.sort(reverse=True)

    return render_template('index.html', default=default_geojson, geojson=geojson)

@main.route('/geodata/<string:geo>')
def geodata(geo):
    geojson = GEOJSON_PATH + geo
    with open(geojson, "r") as output:
        data = json.load(output)
        output.close()
        
    return jsonify(data)