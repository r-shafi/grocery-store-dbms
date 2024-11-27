from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dbms'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'is_admin': self.is_admin
        }


def init_db():
    with app.app_context():
        db.create_all()
        admin = Users.query.filter_by(email='admin@example.com').first()
        if not admin:
            admin = Users(
                name='Admin',
                email='admin@example.com',
                password='admin123',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()


@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(email=email, password=password).first()

        if user:
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin

            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('index'))

        return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')

            if not name or not email or not password:
                return jsonify({'error': 'All fields are required'}), 400

            existing_user = Users.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({'error': 'Email already registered'}), 400

            new_user = Users(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({'message': 'User registered successfully'}), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return render_template("register.html")


@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    products = Product.query.all()
    users = Users.query.all()
    return render_template('admin_dashboard.html', products=products, users=users)


@app.route('/admin/add_product', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        image = request.form.get('image')

        if not all([name, price, quantity]):
            return jsonify({'error': 'All fields are required'}), 400

        new_product = Product(
            name=name,
            price=float(price),
            quantity=int(quantity),
            image=image
        )
        db.session.add(new_product)
        db.session.commit()

        return jsonify({'message': 'Product added successfully'}), 201

    return render_template('add_product.html')


@app.route('/admin/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))

    user = Users.query.get_or_404(user_id)

    if user.is_admin:
        return jsonify({'error': 'Cannot delete admin account'}), 400

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
