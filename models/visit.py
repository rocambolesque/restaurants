from . import db


class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visited_at = db.Column(db.Date, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    restaurant = db.relationship('Restaurant', backref='visits')
