from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import BadRequest, InternalServerError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


def init_db():
    db.create_all()


with app.app_context():
    init_db()


@app.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        return jsonify({'error': str(e)}), InternalServerError.code


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(email=email).first()

        if user and user.password == password:
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            if not name:
                raise BadRequest('Name is required')
            email = request.form.get('email')
            if not email:
                raise BadRequest('Email is required')
            password = request.form.get('password')
            if not password:
                raise BadRequest('Password is required')

            new_user = Users(name=name, email=email,
                             password=password)

            db.session.add(new_user)
            db.session.commit()

            return jsonify({'message': 'User registered successfully'}), 201

        except BadRequest as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'An unexpected error occurred'}), InternalServerError.code

    return render_template("register.html")


@app.route("/test")
def test():
    try:
        users = Users.query.all()
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        return jsonify({'error': str(e)}), InternalServerError.code


def to_dict(self):
    return {column.name: getattr(self, column.name) for column in self.__table__.columns}


if __name__ == "__main__":
    app.run(debug=True)
