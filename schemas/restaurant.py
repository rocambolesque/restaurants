from marshmallow import Schema, fields, MarshalResult, validates, validates_schema, ValidationError

from models.restaurant import Restaurant
from .utils import CsvList
from .visit import VisitSchema


class RestaurantSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'address_full', 'coordinates', 'cuisine', 'visits', 'rating')

    address_full = fields.Function(lambda x: '{}, {} {}'.format(x.address, x.zip, x.city))
    coordinates = fields.Function(lambda x: {'lat': x.lat, 'lng': x.lng} if x.lat and x.lng else None)
    visits = fields.Nested(VisitSchema, many=True)
    rating = fields.Function(lambda x: sum([visit.rating for visit in x.visits])/len(x.visits))

    def dump(self, obj, many=None, update_fields=True, **kwargs):
        result = super().dump(obj, many, update_fields, **kwargs)
        if not self.context.get('geojson'):
            return result
        geojson = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [result.data['coordinates']['lng'], result.data['coordinates']['lat']],
            },
            'properties': {key: value for key, value in result.data.items() if key != 'coordinates'}
        }
        geojson_result = MarshalResult(geojson, result.errors)
        return geojson_result


class GetRestaurantsSchema(Schema):
    name = fields.String(description='Name of a restaurant')
    cuisine = fields.String(description='Cuisine type')


class CreateRestaurantSchema(Schema):
    name = fields.String(required=True)
    address = fields.String(required=True)
    zip = fields.String(required=True)
    city = fields.String(required=True)
    visited_at = fields.Date(required=True)
    cuisine = fields.String(required=True)
    rating = fields.Integer(required=True)
    lat = fields.Decimal(required=True)
    lng = fields.Decimal(required=True)
