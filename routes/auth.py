import re
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import Users
from configs.database import db

auth_blueprint = Blueprint('auth', __name__)

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email)

def is_valid_password(password):
    regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(regex, password)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('public.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            return render_template('login.html', error='Email and password are required')

        if not is_valid_email(email):
            return render_template('login.html', error='Invalid email format')

        user = Users.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.name
            session['is_admin'] = user.is_admin

            return redirect(url_for('admin.admin_dashboard' if user.is_admin else '/'))

        return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('public.index'))
    
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()

            if not name or not email or not password:
                return jsonify({'error': 'All fields are required'}), 400

            if len(name) < 3 or len(name) > 50:
                return jsonify({'error': 'Name must be between 3 and 50 characters'}), 400

            if not is_valid_email(email):
                return jsonify({'error': 'Invalid email format'}), 400

            if not is_valid_password(password):
                return jsonify({'error': 'Password must be at least 8 characters, include one letter, one number, and one special character'}), 400

            existing_user = Users.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({'error': 'Email already registered'}), 400

            hashed_password = generate_password_hash(password)
            new_user = Users(name=name, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id
            session['is_admin'] = new_user.is_admin

            return redirect(url_for('index'))

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    return render_template('register.html')


@auth_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
