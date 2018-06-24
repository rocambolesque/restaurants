from .api_response import ApiResponse


STATUS_NOT_FOUND = 404
STATUS_SERVER_ERROR = 500
STATUS_BAD_REQUEST = 400


class ApiException(ApiResponse):
    description = 'Unknown error'
    error_code = 'unknown_error'
    code = STATUS_SERVER_ERROR

    def __init__(self, description=None, error_code=None, errors=None):
        response = {
            'description': description or self.description,
            'error_code': error_code or self.error_code,
        }
        if errors:
            response['errors'] = errors
        super().__init__(
            response=response,
            status=self.code,
        )


class RestaurantNotFound(ApiException):
    description = 'Restaurant not found'
    error_code = 'restaurant_not_found'
    code = STATUS_NOT_FOUND


class RestaurantBadRequest(ApiException):
    description = 'Restaurant bad request'
    error_code = 'restaurant_bad_request'
    code = STATUS_BAD_REQUEST


class RestaurantServerError(ApiException):
    description = 'Restaurant server error'
    error_code = 'restaurant_server_error'
    code = STATUS_SERVER_ERROR
