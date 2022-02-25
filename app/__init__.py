from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


db = SQLAlchemy()
migrate = Migrate(db)
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app_context = app.app_context()
    app_context.push()
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)

    from app.views import bp
    app.register_blueprint(bp)
    from errors import blueprint
    app.register_blueprint(blueprint)
    return app