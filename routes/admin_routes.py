import os
from werkzeug.utils import secure_filename
from flask import flash, redirect, request, render_template, url_for
from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from configs.database import db
from werkzeug.security import generate_password_hash
from datetime import datetime
from models.Product import Product
from models.Category import Category
from models.Order import Order
from models.User import Users


admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@admin_blueprint.before_request
def check_admin():
    if 'user_id' not in session or not session.get('is_admin'):
        flash("You don't have permission to access the admin panel.", "danger")
        return redirect(url_for('auth.login'))


@admin_blueprint.route('/dashboard')
def admin_dashboard():
    total_products = Product.query.count()
    total_users = Users.query.count()
    total_orders = Order.query.count()

    total_revenue = db.session.query(
        db.func.sum(Order.total_price)).scalar() or 0
    recent_orders = Order.query.order_by(
        Order.created_at.desc()).limit(10).all()

    products = Product.query.all()
    users = Users.query.all()

    return render_template(
        'admin/dashboard.html',
        total_products=total_products,
        total_users=total_users,
        total_orders=total_orders,
        total_revenue=total_revenue,
        recent_orders=recent_orders,
        products=products,
        users=users
    )


@admin_blueprint.route('/products', methods=['GET'])
def manage_products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)


@admin_blueprint.route('/product', methods=['GET', 'POST'])
@admin_blueprint.route('/product/<int:product_id>', methods=['GET', 'POST'])
def add_or_edit_product(product_id=None):
    categories = Category.query.all()
    product = Product.query.get_or_404(product_id) if product_id else None

    if request.method == 'POST':
        name = request.form.get('name').strip()
        price = request.form.get('price').strip()
        quantity = request.form.get('quantity').strip()
        unit = request.form.get('unit').strip()
        description = request.form.get('description').strip()
        category_id = request.form.get('category')
        image = request.form.get('image')

        if not all([name, price, quantity, unit, category_id]):
            flash(
                "All fields (Name, Price, Quantity, Unit, and Category) are required.", "danger")
            return redirect(request.url)

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            flash("Price must be a number and Quantity must be an integer.", "danger")
            return redirect(request.url)

        category = Category.query.get(category_id)
        if not category:
            flash("Invalid category selected.", "danger")
            return redirect(request.url)

        if product:
            product.name = name
            product.price = price
            product.quantity = quantity
            product.unit = unit
            product.description = description
            product.category_id = category_id
            product.image = image
            message = "Product updated successfully!"
        else:
            product = Product(
                name=name, price=price, quantity=quantity, unit=unit,
                description=description, category_id=category_id, image=image
            )
            db.session.add(product)
            message = "Product added successfully!"

        try:
            db.session.commit()
            flash(message, "success")
            return redirect(url_for('admin.manage_products'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")

    return render_template('admin/product.html', categories=categories, product=product)


@admin_blueprint.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully.", "success")
    return redirect(url_for('admin.manage_products'))


@admin_blueprint.route('/categories', methods=['GET', 'POST'])
def manage_categories():
    if request.method == 'POST':
        name = request.form.get('name')
        if not name or len(name) < 3:
            flash("Category name must be at least 3 characters long.", "danger")
            return redirect(url_for('admin.manage_categories'))

        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash("Category added successfully.", "success")

    categories = Category.query.all()
    return render_template('admin/category.html', categories=categories)


@admin_blueprint.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash("Category deleted successfully.", "success")
    return redirect(url_for('admin.manage_categories'))


@admin_blueprint.route('/orders', methods=['GET'])
def manage_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)


@admin_blueprint.route('/update_order/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    status = request.form.get('status')
    order = Order.query.get_or_404(order_id)
    if status not in ['Pending', 'Processing', 'Shipped', 'Delivered', 'Canceled']:
        flash("Invalid order status.", "danger")
        return redirect(url_for('admin.manage_orders'))

    order.status = status
    db.session.commit()
    flash("Order status updated successfully.", "success")
    return redirect(url_for('admin.manage_orders'))


@admin_blueprint.route('/users', methods=['GET'])
def manage_users():
    users = Users.query.all()
    return render_template('admin/users.html', users=users)


@admin_blueprint.route('/user', methods=['GET', 'POST'])
@admin_blueprint.route('/user/<int:user_id>', methods=['GET', 'POST'])
def add_or_edit_user(user_id=None):
    user = Users.query.get(user_id) if user_id else None

    if request.method == 'POST':
        from .user_routes import is_valid_email, is_valid_password
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        if not all([name, email, password]):
            flash("All fields (Name, Email, Password) are required.", "danger")
            return redirect(request.url)

        if not is_valid_email(email):
            flash("Invalid email format.", "danger")
            return redirect(request.url)

        if not is_valid_password(password):
            flash("Password does not meet complexity requirements.", "danger")
            return redirect(request.url)

        hashed_password = generate_password_hash(password)
        if user:
            user.name = name
            user.email = email
            user.password = hashed_password
            user.is_admin = role == 'admin'
            flash("User updated successfully.", "success")
        else:
            new_user = Users(name=name, email=email,
                             password=hashed_password, is_admin=(role == 'admin'))
            db.session.add(new_user)
            flash("User added successfully.", "success")

        db.session.commit()
        return redirect(url_for('admin.manage_users'))

    return render_template('admin/user.html', user=user)


@admin_blueprint.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully.", "success")
    return redirect(url_for('admin.manage_users'))
