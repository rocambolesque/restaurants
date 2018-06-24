from flask import json

from .restaurants import restaurant_bp
from .stats import stats_bp


def init_app(app):
    app.register_blueprint(restaurant_bp, url_prefix='/restaurants')
    app.register_blueprint(stats_bp, url_prefix='/stats')
