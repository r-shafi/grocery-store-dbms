from flask import Blueprint, session, redirect, url_for, render_template, request, jsonify
from models.models import Order, OrderItem, Product, Cart, Users
from configs.database import db
from datetime import datetime

order_blueprint = Blueprint('order', __name__, url_prefix='/order')


@order_blueprint.before_request
def check_user():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))


@order_blueprint.route('/my_orders', methods=['GET'])
def user_orders():
    orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders)


@order_blueprint.route('/place_order', methods=['POST'])
def place_order():
    cart_items = Cart.query.filter_by(user_id=session['user_id']).all()
    
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400
    
    total_price = 0
    order = Order(user_id=session['user_id'], total_price=0)
    db.session.add(order)
    db.session.flush()  

    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        
        if not product or product.quantity < cart_item.quantity:
            db.session.rollback()
            return jsonify({'error': f'Insufficient stock for {product.name}' if product else "Product not found"}), 400
        
        product.quantity -= cart_item.quantity
        
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=product.price * cart_item.quantity
        )
        total_price += order_item.price
        
        db.session.add(order_item)
        db.session.delete(cart_item)
    
    order.total_price = total_price
    order.updated_at = datetime.now()
    db.session.commit()
    
    return jsonify({
        'message': 'Order placed successfully',
        'order_id': order.id
    }), 201


@order_blueprint.route('/cart', methods=['GET'])
def view_cart():
    cart_items = Cart.query.filter_by(user_id=session['user_id']).all()
    total_price = sum(item.quantity * item.product.price for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@order_blueprint.route('/cart/add', methods=['POST'])
def add_to_cart():
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity', 1)
    
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    if product.quantity < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    cart_item = Cart.query.filter_by(user_id=session['user_id'], product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id=session['user_id'], product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    return jsonify({'message': 'Product added to cart'}), 200


@order_blueprint.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    product_id = request.json.get('product_id')
    
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400
    
    cart_item = Cart.query.filter_by(user_id=session['user_id'], product_id=product_id).first()
    
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Product removed from cart'}), 200
    
    return jsonify({'error': 'Product not found in cart'}), 404


@order_blueprint.route('/cancel/<int:order_id>', methods=['POST'])
def cancel_order(order_id):
    order = Order.query.filter_by(id=order_id, user_id=session['user_id']).first()
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    if order.status != 'Pending':
        return jsonify({'error': 'Only pending orders can be canceled'}), 400
    
    for item in order.order_items:
        product = Product.query.get(item.product_id)
        product.quantity += item.quantity  
    
    order.status = 'Canceled'
    order.updated_at = datetime.now()
    db.session.commit()
    
    return jsonify({'message': 'Order canceled successfully'}), 200
