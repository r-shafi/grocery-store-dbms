from flask import Blueprint, render_template, request
from models.models import Product, Category

public_blueprint = Blueprint('public', __name__)

@public_blueprint.route("/")
def index():
    categories = Category.query.all()
    products = Product.query.all()
    return render_template("index.html", products=products, categories=categories)


@public_blueprint.route('/products/category/<int:category_id>')
def products_by_category(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id).all()
    categories = Category.query.all()
    return render_template('index.html', products=products, categories=categories, selected_category=category)

@public_blueprint.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    categories = Category.query.all()
    return render_template('index.html', products=products, categories=categories, search_query=query)
