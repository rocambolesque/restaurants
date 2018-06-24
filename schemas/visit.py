from marshmallow import Schema

class VisitSchema(Schema):
    class Meta:
        fields = ('id', 'visited_at', 'rating')
