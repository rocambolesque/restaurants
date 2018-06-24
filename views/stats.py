import json

from flask import Blueprint, current_app, request
from sqlalchemy import func

from .api_response import ApiResponse
from .exceptions import RestaurantBadRequest, RestaurantNotFound, RestaurantServerError
from models import db
from models.restaurant import Restaurant
from models.visit import Visit


stats_bp = Blueprint('stats', __name__)


@stats_bp.route('/visits_by_year')
def by_year():
    '''Visits by year
    ---
    x-extension: metadata
    get:
        responses:
            200:
                description: Visits by year
    '''
    column = func.date_trunc('year', Visit.visited_at)
    visits_by_year = db.session.query(
        column, func.count(Visit.visited_at)
    ).group_by(
        column
    ).order_by(
        column
    )
    items = [{'visited_at': item[0].year, 'count': item[1]} for item in visits_by_year.all()]
    return ApiResponse(items)


@stats_bp.route('/restaurants_by_cuisine')
def by_cuisine():
    '''Restaurants by cuisine
    ---
    x-extension: metadata
    get:
        responses:
            200:
                description: Restaurants by cuisine
    '''
    column = Restaurant.cuisine
    restaurants_by_cuisine = db.session.query(
        column, func.count(column)
    ).group_by(
        column
    ).order_by(
        func.count(column)
    )
    items = [{'cuisine': item[0], 'count': item[1]} for item in restaurants_by_cuisine.all()]
    return ApiResponse(items)
