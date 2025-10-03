from datetime import datetime
from . import db


class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self) -> str:
        return f"<Product {self.product_id}>"


class Location(db.Model):
    __tablename__ = 'location'
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=True)

    def __repr__(self) -> str:
        return f"<Location {self.location_id}>"


class ProductMovement(db.Model):
    __tablename__ = 'product_movement'
    movement_id = db.Column(db.String(64), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    from_location = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=True)
    to_location = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    product = db.relationship('Product')
    from_loc = db.relationship('Location', foreign_keys=[from_location])
    to_loc = db.relationship('Location', foreign_keys=[to_location])

    def __repr__(self) -> str:
        return f"<Movement {self.movement_id} {self.product_id} {self.qty}>"



