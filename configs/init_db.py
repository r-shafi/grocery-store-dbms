from werkzeug.security import generate_password_hash
from configs.database import db
from .seed_db import seed_demo_data
from models.Category import Category
from models.User import Users


def init_db():
    db.create_all()

    admin = Users.query.filter_by(email='admin@admin.com').first()

    if not admin:
        hashed_password = generate_password_hash('admin123')
        admin = Users(name='Admin User', email='admin@admin.com',
                      password=hashed_password, is_admin=True)
        db.session.add(admin)

    categories = ['Fruits', 'Vegetables', 'Dairy', 'Bakery',
                  'Meat', 'Fish', 'Snacks', 'Spices', 'Beverages', 'Desserts']

    for cat_name in categories:
        if not Category.query.filter_by(name=cat_name).first():
            db.session.add(Category(name=cat_name))

    db.session.commit()

    if Users.query.count() == 1:
        seed_demo_data()
