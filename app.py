from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)


def init_db():
    db.create_all()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

with app.app_context():
    init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/main")
def main():
    return "This is the main page"


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        new_user = Users(name=name, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

    return render_template("register.html")


@app.route("/test")
def test():
    users = db.session.execute(db.select(Users))

    users = [user._asdict() for user in result.scalars()]
    print(jsonify(users))

    return jsonify(users)


if __name__ == "__main__":
    app.run(debug=True)
