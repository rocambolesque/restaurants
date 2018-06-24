search_bp = Blueprint('search', __name__)


@search_bp.route('')
def get_searchs():
    '''Restaurant list
    ---
    x-extension: metadata
    get:
        responses:
            200:
                description: List of searchs
            400:
                description: Validation error
    '''
    schema = GetRestaurantsSchema()
    data, errors = schema.load(request.args)
    if errors:
        return RestaurantBadRequest(errors=errors)
    searchs = Restaurant.query.all()
    return ApiResponse([RestaurantSchema().dump(item).data for item in searchs])

