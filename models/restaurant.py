from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_X, ST_Y
from sqlalchemy import func
from sqlalchemy.event import listens_for
from sqlalchemy.orm import column_property

from . import db


SRID = 4326


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    cuisine = db.Column(db.String)
    address = db.Column(db.String)
    zip = db.Column(db.String)
    city = db.Column(db.String)
    coordinates = db.Column(Geometry(srid=SRID))
    lat = column_property(ST_Y(coordinates))
    lng = column_property(ST_X(coordinates))


@listens_for(Restaurant, 'before_insert')
def do_stuff(mapper, connect, target):
    target.coordinates = func.ST_GeomFromText('POINT({lng} {lat})'.format(lng=target.lng, lat=target.lat), SRID)
