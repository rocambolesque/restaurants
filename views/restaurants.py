import json

from flask import Blueprint, current_app, request

from .api_response import ApiResponse
from .exceptions import RestaurantBadRequest, RestaurantNotFound, RestaurantServerError
from models import db
from models.restaurant import Restaurant
from models.visit import Visit
from schemas.restaurant import CreateRestaurantSchema, GetRestaurantsSchema, RestaurantSchema


restaurant_bp = Blueprint('restaurant', __name__)


@restaurant_bp.route('')
def get_restaurants():
    '''Restaurant list
    ---
    x-extension: metadata
    get:
        responses:
            200:
                description: List of restaurants
            400:
                description: Validation error
    '''
    schema = GetRestaurantsSchema()
    data, errors = schema.load(request.args)
    if errors:
        return RestaurantBadRequest(errors=errors)

    restaurants = Restaurant.query
    filters = []

    if data.get('name'):
        filters.append(Restaurant.name == data['name'])
    if data.get('cuisine'):
        filters.append(Restaurant.cuisine == data['cuisine'])
    if data.get('min_rating'):
        restaurants = restaurants.join(Visit)
        filters.append(Visit.rating >= data['min_rating'])

    restaurants = restaurants.filter(*filters)
    restaurants = restaurants.all()

    return ApiResponse([RestaurantSchema().dump(item).data for item in restaurants])


@restaurant_bp.route('/geojson')
def get_restaurants_geojson():
    '''Restaurant list
    ---
    x-extension: metadata
    get:
        responses:
            200:
                description: List of features in GeoJSON format
            400:
                description: Validation error
    '''
    schema = GetRestaurantsSchema()
    data, errors = schema.load(request.args)
    if errors:
        return RestaurantBadRequest(errors=errors)
    restaurants = Restaurant.query.all()
    restaurant_schema = RestaurantSchema()
    restaurant_schema.context = {'geojson': True}
    geojson = {
        'type': 'FeatureCollection',
        'features': [restaurant_schema.dump(item).data for item in restaurants],
    }
    return ApiResponse(geojson)


@restaurant_bp.route('', methods=['POST'])
def create_restaurant():
    '''Create a restaurant
    ---
    x-extension: metadata
    get:
        responses:
            201:
                description: Restaurant created
            400:
                description: Validation error
    '''
    schema = CreateRestaurantSchema()
    data, errors = schema.load(request.get_json(force=True))
    if errors:
        return RestaurantBadRequest(errors)

    restaurant = Restaurant()
    restaurant.name = data['name']
    restaurant.cuisine = data['cuisine']
    restaurant.address = data['address']
    restaurant.zip = data['zip']
    restaurant.city = data['city']
    restaurant.lat = data['lat']
    restaurant.lng = data['lng']

    visit = Visit()
    visit.visited_at = data['visited_at']
    visit.rating = data['rating']
    visit.restaurant = restaurant

    try:
        db.session.add(restaurant)
        db.session.add(visit)
        db.session.commit()
    except Exception as err:
        import pdb;pdb.set_trace() # DEBUG
        db.session.rollback()
        return RestaurantServerError(
            description='Error inserting restaurant',
            error_code='restaurant_insert_error',
            errors=str(err)
        )

    return ApiResponse(RestaurantSchema().dump(restaurant))
