from apispec import APISpec
from flask import json

from app import create_app

# Create spec
spec = APISpec(
    title='Restaurant API',
    version='0.1.0',
    info=dict(
        description='You know, for devs'
    ),
    plugins=[
        'apispec.ext.flask',
        'apispec.ext.marshmallow'
    ]
)

# Reference your schemas definitions
from schemas.restaurant import RestaurantSchema

spec.definition('Restaurant', schema=RestaurantSchema)
# ...

# Now, reference your routes.
from views.restaurants import get_restaurants, get_restaurant

# We need a working context for apispec introspection.
app = create_app()

with app.test_request_context():
    spec.add_path(view=get_restaurants)
    spec.add_path(view=get_restaurant)
    # ...

# We're good to go! Save this to a file for now.
with open('swagger.json', 'w') as f:
    json.dump(spec.to_dict(), f)
