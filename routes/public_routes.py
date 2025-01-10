from flask import Blueprint, render_template, request, jsonify
from models.Category import Category
from models.Product import Product

public_blueprint = Blueprint('public', __name__)


@public_blueprint.route("/")
def index():
    try:
        categories = Category.query.all()
        products = Product.query.all()
        return render_template("index.html", products=products, categories=categories)
    except Exception as e:
        return render_template("error.html", error=f"An error occurred: {str(e)}")


@public_blueprint.route('/products/category/<int:category_id>')
def products_by_category(category_id):
    try:
        category = Category.query.get_or_404(category_id)
        products = Product.query.filter_by(category_id=category_id).all()
        categories = Category.query.all()
        return render_template(
            'index.html',
            products=products,
            categories=categories,
            selected_category=category
        )
    except Exception as e:
        return render_template("error.html", error=f"An error occurred: {str(e)}")


@public_blueprint.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get('query', '').strip()
        products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
        categories = Category.query.all()
        return render_template(
            'index.html',
            products=products,
            categories=categories,
            search_query=query
        )
    except Exception as e:
        return render_template("error.html", error=f"An error occurred: {str(e)}")


@public_blueprint.route('/product/<int:product_id>')
def product_details(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        return render_template('product_details.html', product=product)
    except Exception as e:
        return render_template("error.html", error=f"An error occurred: {str(e)}")


@public_blueprint.route('/api/categories', methods=['GET'])
def api_categories():
    try:
        categories = Category.query.all()
        return jsonify([{'id': c.id, 'name': c.name} for c in categories])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
