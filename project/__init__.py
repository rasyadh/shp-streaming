from flask import Flask
import config

APP_SETTINGS = config.DevelopmentConfig

app = Flask(__name__)

# use this for windows
app.config.from_object(APP_SETTINGS)

# use this for linux
# app.config.from_object(os.environ['APP_SETTINGS'])

if __name__ == '__main__':
    app.run()

from project.views.main import main
from project.views.data import data

app.register_blueprint(main)
app.register_blueprint(data)