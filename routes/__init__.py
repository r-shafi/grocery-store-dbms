from .auth import auth_blueprint
from .public import public_blueprint
from .admin import admin_blueprint
from .order import order_blueprint

def init_routes(app):
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(public_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(order_blueprint)
