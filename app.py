import os
from flask import Flask
from flask_cors import CORS

import models, views


def create_app():
    app = Flask(os.getenv('APPLICATION_NAME'), instance_relative_config=True)
    app.config.from_envvar('SETTINGS')
    CORS(app, resources={r"/*": {"origins": "*"}})

    models.init_app(app)
    views.init_app(app)

    return app
