from flask import Blueprint, session, redirect, url_for, render_template, request, jsonify
from models.models import Order, OrderItem, Product
from configs.database import db

order_blueprint = Blueprint('order', __name__, url_prefix='/order')

@order_blueprint.before_request
def check_user():
  if 'user_id' not in session:
    return redirect(url_for('login'))
  

@order_blueprint.route('/my_orders')
def user_orders():
    orders = Order.query.filter_by(user_id=session['user_id']).all()
    return render_template('orders.html', orders=orders)


@order_blueprint.route('/place_order', methods=['POST'])
def place_order():
    cart_items = request.json.get('cart', [])
    
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400
    
    total_price = 0
    order = Order(user_id=session['user_id'], total_price=0)
    db.session.add(order)
    
    for item in cart_items:
        product = Product.query.get(item['product_id'])
        
        if not product or product.quantity < item['quantity']:
            db.session.rollback()
            return jsonify({'error': f'Insufficient stock for {product.name}'}), 400
        
        product.quantity -= item['quantity']
        
        order_item = OrderItem(
            order_id=order.id, 
            product_id=item['product_id'], 
            quantity=item['quantity'], 
            price=product.price * item['quantity']
        )
        total_price += order_item.price
        
        db.session.add(order_item)
    
    order.total_price = total_price
    db.session.commit()
    
    return jsonify({
        'message': 'Order placed successfully', 
        'order_id': order.id
    }), 201
