from datetime import datetime
from configs.database import db
from sqlalchemy.orm import validates


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    image = db.Column(db.String(128))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    unit = db.Column(db.String(16))
    description = db.Column(db.Text)
    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    orders = db.relationship('OrderItem', backref='product', lazy=True)
    cart_items = db.relationship('Cart', backref='product', lazy=True)

    @validates('name', 'price', 'quantity')
    def validate_product_fields(self, key, value):
        if key == 'name' and not value:
            raise ValueError("Name cannot be empty")
        if key == 'price' and value <= 0:
            raise ValueError("Price must be greater than 0")
        if key == 'quantity' and value < 0:
            raise ValueError("Quantity cannot be negative")
        return value
