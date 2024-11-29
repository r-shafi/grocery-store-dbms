from flask import Flask
from configs.config import Config
from routes import init_routes
from configs.database import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

from flask import session

@app.context_processor
def user():
    return {'username': session.get('username', None)}

init_routes(app)

if __name__ == "__main__":
    with app.app_context():
        from configs.init_db import init_db
        init_db()
    app.run(debug=True)
