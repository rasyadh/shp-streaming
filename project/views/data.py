import os
import json
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    jsonify,
    request
)
from werkzeug.utils import secure_filename
from project import app
from project.lib.shp2geojson import Shapefile2GeoJSON

data = Blueprint('data', __name__)
SHAPEFILES_PATH = app.root_path + '/static/shapefiles/'
GEOJSON_PATH = app.root_path + '/static/geojson/'
app.config['UPLOAD_FOLDER'] = SHAPEFILES_PATH
ALLOWED_EXTENSIONS = set(['shp', 'dbf'])

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@data.route('/data_peta/upload_data', methods=['POST'])
def upload_data():
    if request.method == 'POST':
        try:
            file_shp = request.files['shp']
            file_dbf = request.files['dbf']

            if file_shp and allowed_file(file_shp.filename) and file_dbf and allowed_file(file_dbf.filename):
                filename_shp = secure_filename(file_shp.filename)
                filename_dbf = secure_filename(file_dbf.filename)

                file_shp.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_shp))
                file_dbf.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_dbf))
        except Exception as e:
            print(e)

        return redirect(url_for('data.index'))

    return redirect(url_for('data.index'))

@data.route('/data_peta/hapus/<string:shp>')
def delete_data(shp):
    try :
        os.remove(SHAPEFILES_PATH + shp)
        os.remove(SHAPEFILES_PATH + shp.split('.')[0] + '.dbf')
        os.remove(GEOJSON_PATH + shp.split('.')[0] + '.json')
    except Exception as e:
        print(e)

    return redirect(url_for('data.index'))