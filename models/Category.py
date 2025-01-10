from datetime import datetime
from configs.database import db
from sqlalchemy.orm import validates


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    products = db.relationship('Product', backref='category', lazy=True)

    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Name cannot be empty")
        return value
