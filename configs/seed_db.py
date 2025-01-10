from werkzeug.security import generate_password_hash
from datetime import datetime
from configs.database import db
from models.Cart import Cart
from models.Category import Category
from models.Order import Order, OrderStatus
from models.OrderItem import OrderItem
from models.Product import Product
from models.User import Users


def seed_demo_data():
    categories = [
        "Fruits", "Vegetables", "Dairy", "Bakery", "Meat",
        "Fish", "Snacks", "Spices", "Beverages", "Desserts"
    ]

    for cat in categories:
        if not Category.query.filter_by(name=cat).first():
            db.session.add(Category(name=cat))

    db.session.commit()
    category_map = {cat.name: cat.id for cat in Category.query.all()}

    products = [
        {"name": "Apple", "image": "https://static.libertyprim.com/files/familles/pomme-large.jpg",
            "price": 260, "quantity": 100, "description": "Fresh red apples", "category": "Fruits"},
        {"name": "Banana", "image": "https://static.wixstatic.com/media/53e8bb_a1e88e551162485eb4ff962437300872~mv2.jpeg/v1/crop/x_0,y_105,w_1024,h_919/fill/w_560,h_560,al_c,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/Banana.jpeg",
            "price": 25, "quantity": 150, "description": "Ripe bananas", "category": "Fruits"},
        {"name": "Carrot", "image": "https://evergreenfoods.co.uk/wp-content/uploads/2019/06/carrot-600x600.png",
            "price": 30, "quantity": 200, "description": "Fresh carrots", "category": "Vegetables"},
        {"name": "Potato", "image": "https://m.media-amazon.com/images/I/41QKCkQ2A5L.jpg",
            "price": 70, "quantity": 300, "description": "Organic potatoes", "category": "Vegetables"},
        {"name": "Milk", "image": "https://as1.ftcdn.net/v2/jpg/01/06/68/88/1000_F_106688812_rVoRFXazgIMEUJdvffG9p0XvP8Lntf0a.jpg",
            "price": 100, "quantity": 50, "description": "Whole milk", "category": "Dairy"},
        {"name": "Cheese", "image": "https://cdn.usdairy.com/optimize/getmedia/b5108b6f-59c3-4cc4-b1d5-4b9b0d1e0c54/swiss.jpg.jpg.aspx?format=webp",
            "price": 500, "quantity": 30, "description": "Cheddar cheese", "category": "Dairy"},
        {"name": "Bread", "image": "https://assets.bonappetit.com/photos/5c62e4a3e81bbf522a9579ce/16:9/w_4000,h_2250,c_limit/milk-bread.jpg",
            "price": 60, "quantity": 80, "description": "Whole wheat bread", "category": "Bakery"},
        {"name": "Croissant", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoPD4zUoTBei_LVLmT5uIoM4gXcYoz135AGw&s",
            "price": 70, "quantity": 40, "description": "Buttery croissants", "category": "Bakery"},
        {"name": "Chicken", "image": "https://cdn.britannica.com/18/137318-050-29F7072E/rooster-Rhode-Island-Red-roosters-chicken-domestication.jpg",
            "price": 150, "quantity": 25, "description": "Fresh chicken", "category": "Meat"},
        {"name": "Beef", "image": "https://embed.widencdn.net/img/beef/melpznnl7q/800x600px/Top%20Sirloin%20Steak.psd?keep=c&u=7fueml",
            "price": 750, "quantity": 20, "description": "Ground beef", "category": "Meat"},
        {"name": "Salmon", "image": "https://www.vicsmeat.com.au/cdn/shop/products/ora-king-mid-cut-salmon-160-180g-x-2-pieces-868760.jpg?v=1689745024",
            "price": 800, "quantity": 15, "description": "Atlantic salmon", "category": "Fish"},
        {"name": "Shrimp", "image": "https://media.istockphoto.com/id/1366270800/photo/pile-of-boiled-peeled-shrimps.jpg?s=612x612&w=0&k=20&c=DgObKS5XZMKVeTtSkdg65Y-fcopDhqvF7g-Ays4HbYU=",
            "price": 900, "quantity": 10, "description": "Fresh shrimp", "category": "Fish"},
        {"name": "Chips", "image": "https://img.freepik.com/free-photo/potato-chips-isolated-white_93675-129934.jpg",
            "price": 20, "quantity": 100, "description": "Potato chips", "category": "Snacks"},
        {"name": "Biscuits", "image": "https://t4.ftcdn.net/jpg/02/24/40/43/360_F_224404329_KrZ69DD38fjb4zYKL01AKCy46zALlkWv.jpg",
            "price": 50, "quantity": 120, "description": "Butter biscuits", "category": "Snacks"},
        {"name": "Salt", "image": "https://t3.ftcdn.net/jpg/01/99/90/94/360_F_199909433_VWfq94a6BYtepSIJczsxykqAYuFVEX1Z.jpg",
            "price": 38, "quantity": 300, "description": "Sea salt", "category": "Spices"},
        {"name": "Pepper", "image": "https://images.immediate.co.uk/production/volatile/sites/30/2020/02/Red-peppers-afa27f8.jpg?resize=700%2C366",
            "price": 12, "quantity": 150, "description": "Black pepper", "category": "Spices"},
        {"name": "Coke", "image": "https://media.istockphoto.com/id/530428650/photo/cola-glass-with-ice-cubes.jpg?s=612x612&w=0&k=20&c=keqH2KNWHO1sFxtsBfx5EZjyep1CRBHIqwe_ZwxszHc=",
            "price": 25, "quantity": 60, "description": "Coca-Cola", "category": "Beverages"},
        {"name": "Juice", "image": "https://cdn.pixabay.com/photo/2023/04/13/21/14/ai-generated-7923488_640.jpg",
            "price": 15, "quantity": 40, "description": "Orange juice", "category": "Beverages"},
        {"name": "Cake", "image": "https://img.freepik.com/premium-photo/chocolate-fudge-birthday-cake-white-background-birthday-cake-jpg-format_1075459-8582.jpg",
            "price": 500, "quantity": 15, "description": "Chocolate cake", "category": "Desserts"},
        {"name": "Ice Cream", "image": "https://thumbs.dreamstime.com/b/chocolate-vanilla-strawberry-ice-cream-cone-white-background-clipping-path-42006740.jpg",
            "price": 30, "quantity": 25, "description": "Vanilla ice cream", "category": "Desserts"}
    ]

    for prod in products:
        if not Product.query.filter_by(name=prod["name"]).first():
            db.session.add(Product(
                name=prod["name"],
                image=prod["image"],
                price=prod["price"],
                quantity=prod["quantity"],
                description=prod["description"],
                category_id=category_map[prod["category"]]
            ))

    db.session.commit()

    users = [
        {"name": "John Doe", "email": "john@gmail.com",
            "password": "password1", "is_admin": False},
        {"name": "Jane Doe", "email": "jane@gmail.com",
            "password": "password2", "is_admin": False},
        {"name": "Md Karim", "email": "karim@yahoo.com",
            "password": "password3", "is_admin": False},
        {"name": "Md Rahim", "email": "rahim@outlook.com",
            "password": "password4", "is_admin": False}
    ]

    for user in users:
        if not Users.query.filter_by(email=user["email"]).first():
            hashed_password = generate_password_hash(user["password"])
            db.session.add(Users(
                name=user["name"],
                email=user["email"],
                password=hashed_password,
                is_admin=user["is_admin"]
            ))

    db.session.commit()

    for i in range(10):
        user = Users.query.filter_by(
            is_admin=False).order_by(db.func.random()).first()
        products_in_order = Product.query.order_by(
            db.func.random()).limit(3).all()

        total_price = sum(prod.price for prod in products_in_order)

        order = Order(user_id=user.id, total_price=total_price,
                      status=OrderStatus.PENDING)
        db.session.add(order)
        db.session.commit()

        for prod in products_in_order:
            order_item = OrderItem(
                order_id=order.id, product_id=prod.id, quantity=1, price=prod.price)
            db.session.add(order_item)

        db.session.commit()

    print("Demo data seeded successfully!")
