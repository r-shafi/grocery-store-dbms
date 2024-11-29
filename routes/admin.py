from flask import Blueprint, session, redirect, url_for, render_template, request, jsonify
from models.models import Product, Users, Order, Category, OrderStatus
from configs.database import db
from werkzeug.security import generate_password_hash

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@admin_blueprint.before_request
def check_admin():
  if 'user_id' not in session or not session.get('is_admin'):
    return redirect(url_for('auth.login'))

@admin_blueprint.route('/dashboard')
def admin_dashboard():
    total_products = Product.query.count()
    total_users = Users.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_price)).scalar() or 0
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    products = Product.query.all()
    users = Users.query.all()
    return render_template('admin/dashboard.html', 
                           products=products, 
                           users=users, 
                           recent_orders=recent_orders,
                           total_products=total_products,
                           total_users=total_users,
                           total_orders=total_orders,
                           total_revenue="{:.2f}".format(total_revenue))


@admin_blueprint.route('/product', methods=['GET', 'POST'])
def add_product():
    categories = Category.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        description = request.form.get('description')
        category_id = request.form.get('category')
        image = request.form.get('image')
        if not all([name, price, quantity]):
            return jsonify({'error': 'All fields are required'}), 400
        new_product = Product(
            name=name, 
            price=float(price), 
            quantity=int(quantity),
            description=description,
            category_id=category_id,
            image=image
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully'}), 201
    return render_template('admin/product.html', categories=categories)


@admin_blueprint.route('/update_order/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    status = request.form.get('status')
    order = Order.query.get_or_404(order_id)
    order.status = status
    db.session.commit()
    
    return redirect(url_for('admin_orders'))


@admin_blueprint.route('/orders')
def admin_orders():
    orders = Order.query.all()
    return render_template('admin_orders.html', orders=orders, statuses=vars(OrderStatus))

@admin_blueprint.route('/create_category', methods=['POST'])
def create_category():
    name = request.form.get('name')
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category created successfully'}), 201

@admin_blueprint.route('/user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        from .auth import is_valid_email, is_valid_password
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')


        if not all([name, email, password]):
            return jsonify({'error': 'All fields are required'}), 400

        if not is_valid_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if not is_valid_password(password):
            return jsonify({'error': 'Password must be at least 8 characters, include one letter, one number, and one special character'}), 400

        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400
        
        hashed_password = generate_password_hash(password)
        new_user = Users(name=name, email=email, password=hashed_password, is_admin=role == 'admin')
        
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User added successfully'}), 201

    return render_template('admin/user.html')

@admin_blueprint.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200

@admin_blueprint.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200
